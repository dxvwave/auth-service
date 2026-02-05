from db import db_session_manager
from services.auth.auth_service import auth_service_instance
from interfaces.grpc.gen import auth_pb2, auth_pb2_grpc


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    async def ValidateToken(self, request, context):
        async with db_session_manager.sessionmaker() as session:
            is_valid = await auth_service_instance.validate_token_and_user(
                request.token,
                session,
            )
        return auth_pb2.ValidateResponse(is_valid=is_valid)
