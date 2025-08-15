# app/core/custom_exceptions.py

class UserNotFound(Exception):
    pass

class ProxyQuotaExceeded(Exception):
    pass

class UnauthorizedAccess(Exception):
    pass
