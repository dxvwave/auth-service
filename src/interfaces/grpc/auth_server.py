from interfaces.grpc.gen import auth_pb2, auth_pb2_grpc


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    async def ValidateToken(self, request, context):
        is_valid = len(request.token) > 5
        # Debug statement
        print(f"Validating token: {request.token} -> {is_valid}")
        return auth_pb2.ValidateResponse(is_valid=is_valid)
