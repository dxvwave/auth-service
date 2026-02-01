import grpc
from concurrent import futures
from gen import auth_pb2, auth_pb2_grpc


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def ValidateToken(self, request, context):
        is_valid = len(request.token) > 5
        print(f"Validating token: {request.token} -> {is_valid}")
        return auth_pb2.ValidateResponse(is_valid=is_valid)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50051")
    print("Auth gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
