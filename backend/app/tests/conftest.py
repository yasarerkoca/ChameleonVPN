import os
from pathlib import Path
from dotenv import dotenv_values

# Load test environment before importing application modules
env_path = Path(__file__).resolve().parents[3] / ".env.test"
os.environ.update(dotenv_values(env_path))

import asyncio
from asgi_lifespan import LifespanManager
from fastapi_limiter import FastAPILimiter
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config.database import Base, get_db

# ---------------------------------------------------------------------------
# Environment setup
# ---------------------------------------------------------------------------
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# ---------------------------------------------------------------------------
# Pytest options
# ---------------------------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--reuse-db",
        action="store_true",
        default=False,
        help="Reuse database and Redis containers between test runs.",
    )


# ---------------------------------------------------------------------------
# Dockerised services
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def postgres_container(request):
    if not shutil.which("docker"):
        pytest.skip("Docker is required for database tests")

    reuse = request.config.getoption("--reuse-db")
    container_name = os.getenv("POSTGRES_CONTAINER", "test-postgres")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    db_name = os.getenv("POSTGRES_DB", "postgres")
    host_port = os.getenv("POSTGRES_PORT", "5432")

    if reuse:
        subprocess.run(
            ["docker", "start", container_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--name",
                container_name,
                "-e",
                f"POSTGRES_USER={user}",
                "-e",
                f"POSTGRES_PASSWORD={password}",
                "-e",
                f"POSTGRES_DB={db_name}",
                "-p",
                f"{host_port}:5432",
                "postgres:14",
            ],
            check=True,
        )

    # wait for Postgres to be ready
    for _ in range(30):
        try:
            tmp_engine = create_engine(
                f"postgresql+psycopg2://{user}:{password}@localhost:{host_port}/{db_name}"
            )
            with tmp_engine.connect():
                break
        except Exception:
            time.sleep(1)

    yield

    if not reuse:
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


@pytest.fixture(scope="session", autouse=True)
def redis_container(request):
    if not shutil.which("docker"):
        pytest.skip("Docker is required for Redis tests")

    reuse = request.config.getoption("--reuse-db")
    container_name = os.getenv("REDIS_CONTAINER", "test-redis")
    port = os.getenv("REDIS_PORT", "6379")

    if reuse:
        subprocess.run(
            ["docker", "start", container_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--name",
                container_name,
                "-p",
                f"{port}:6379",
                "redis:7-alpine",
            ],
            check=True,
        )

    time.sleep(1)
    yield

    if not reuse:
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


@pytest.fixture(scope="session", autouse=True)
def setup_database(postgres_container, request):
    Base.metadata.create_all(bind=engine)
    yield
    if not request.config.getoption("--reuse-db"):
        Base.metadata.drop_all(bind=engine)


# ---------------------------------------------------------------------------
# Async client fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _startup_limiter(redis_container):
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis = await aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    redis = await aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)
    yield


@pytest_asyncio.fixture()
async def client(_startup_limiter):
    async with LifespanManager(app):
        async with AsyncClient(base_url="http://localhost:8000") as ac:
            yield ac
