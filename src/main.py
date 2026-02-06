import logging

from fastapi.concurrency import asynccontextmanager
import uvicorn
import grpc
from fastapi import FastAPI

from contracts.gen import auth_pb2_grpc
from interfaces.grpc.auth_server import AuthService
from interfaces.api.auth_routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    grpc_server = grpc.aio.server()
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), grpc_server)
    grpc_server.add_insecure_port("[::]:50051")
    await grpc_server.start()
    logging.info("gRPC server started via Lifespan")
    
    yield
    
    await grpc_server.stop(5)
    logging.info("gRPC server stopped")


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)
