"""
Middleware для приложения core.
"""
from .admin_jwt_middleware import AdminJWTMiddleware

__all__ = ['AdminJWTMiddleware']

