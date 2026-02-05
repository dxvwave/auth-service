from services.auth import auth_service_instance, AuthService


def get_auth_service() -> AuthService:
    return auth_service_instance
