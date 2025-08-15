# app.events.__init__.py
"""
Uygulama başlatma ve durdurma olayları için modül içeriği.
"""
from .startup_events import register_startup_events
from .shutdown_events import register_shutdown_events

__all__ = ["register_startup_events", "register_shutdown_events"]
