"""ChameleonVPN backend app package."""

from .main import app
# The FastAPI application instance lives in ``app.main``.
# Importing it at package import time would execute middleware and
# startup hooks during test collection.  Modules should import the app
# explicitly from ``app.main`` when needed.
__all__: list[str] = []
