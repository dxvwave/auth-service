import logging
import asyncio

import uvicorn
import grpc
from fastapi import FastAPI

from interfaces.grpc.auth_server import AuthService
from interfaces.grpc.gen import auth_pb2_grpc


async def run_grpc_server():
    server = grpc.aio.server()
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50051")
    logging.info("Auth gRPC server started on port 50051")
    await server.start()
    await server.wait_for_termination()


async def run_http_server():
    app = FastAPI()
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    logging.info("HTTP server started on port 8000")
    await server.serve()


async def main():
    await asyncio.gather(
        run_grpc_server(),
        run_http_server(),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass