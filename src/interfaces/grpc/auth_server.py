import grpc
from contracts.gen import auth_pb2, auth_pb2_grpc

from core.utils import provide_session
from services.auth.auth_service import auth_service_instance


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    @provide_session
    async def ValidateToken(self, request, context, session):
        user = await auth_service_instance.validate_token_and_user(
            request.token,
            session,
        )
        if not user:
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")

        user_proto = auth_pb2.User(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            is_verified=user.is_verified,
        )

        return auth_pb2.ValidateResponse(is_valid=True, user=user_proto)
