import logging

import uvicorn
import grpc
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from contracts.gen import auth_pb2_grpc
from core.logging_config import setup_logging
from interfaces.grpc.auth_server import AuthGrpcServicer
from interfaces.api.auth_routes import router as auth_router
from interfaces.api.user_routes import router as user_router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for the FastAPI application."""
    # Startup
    logger.info("Starting auth service...")

    grpc_server = grpc.aio.server()
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthGrpcServicer(), grpc_server)
    grpc_server.add_insecure_port("[::]:50051")
    await grpc_server.start()
    logger.info("gRPC server started on port 50051")

    yield

    # Shutdown
    logger.info("Shutting down auth service...")
    await grpc_server.stop(5)
    logger.info("gRPC server stopped")


app = FastAPI(
    title="Auth Service",
    description="Authentication and Authorization Service for Microservices",
    version="0.1.0",
    root_path="/api/v1/auth",
    lifespan=lifespan,
)

# Include routers with tags
app.include_router(auth_router, tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
