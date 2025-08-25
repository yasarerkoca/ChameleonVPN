import os
import importlib.util
from pathlib import Path

import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configure minimal environment for importing application modules
os.environ.setdefault(
    "DATABASE_URL",
    os.getenv("DATABASE_URL", "postgresql+psycopg2://user:pass@localhost/test")
)
os.environ.setdefault("SECRET_KEY", "x" * 16)
os.environ.setdefault("SESSION_SECRET_KEY", "y" * 16)

# Dynamically load the webhook routes module to avoid heavy package imports
spec = importlib.util.spec_from_file_location(
    "webhook_routes", Path(__file__).resolve().parents[1] / "routers/payment/webhook_routes.py"
)
webhook_routes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(webhook_routes)

# Local SQLAlchemy models for isolated testing
Base = declarative_base()


class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    plan_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(32), default="pending")


class BillingHistory(Base):
    __tablename__ = "billing_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    transaction_id = Column(String(128), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(64), default="pending")


# Patch the module to use the local models
webhook_routes.Payment = Payment
webhook_routes.BillingHistory = BillingHistory
_handle_stripe_event = webhook_routes._handle_stripe_event
_handle_iyzico_event = webhook_routes._handle_iyzico_event


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_handle_stripe_event_updates_payment_and_history(db_session):
    payment = Payment(user_id=1, plan_id=1, amount=100, status="pending")
    db_session.add(payment)
    db_session.commit()
    db_session.refresh(payment)

    event = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "sess_123",
                "metadata": {"payment_id": str(payment.id)},
            }
        },
    }

    _handle_stripe_event(event, db_session)

    updated = db_session.query(Payment).filter_by(id=payment.id).first()
    assert updated.status == "completed"

    history = db_session.query(BillingHistory).filter_by(transaction_id="sess_123").first()
    assert history is not None
    assert history.user_id == payment.user_id


def test_handle_iyzico_event_updates_payment_and_history(db_session):
    payment = Payment(user_id=2, plan_id=1, amount=50, status="pending")
    db_session.add(payment)
    db_session.commit()
    db_session.refresh(payment)

    event = {
        "iyz_event_type": "payment.succeeded",
        "paymentId": str(payment.id),
    }

    _handle_iyzico_event(event, db_session)

    updated = db_session.query(Payment).filter_by(id=payment.id).first()
    assert updated.status == "completed"

    history = db_session.query(BillingHistory).filter_by(transaction_id=str(payment.id)).first()
    assert history is not None
    assert history.user_id == payment.user_id

