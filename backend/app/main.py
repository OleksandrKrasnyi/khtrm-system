"""Main FastAPI application for KHTRM System."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import settings
from .database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    await create_tables()
    print("🚀 KHTRM System backend started successfully")

    yield

    # Shutdown
    print("⏹️ KHTRM System backend shutting down")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="KHTRM System - Kharkiv Transport Resource Management",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )

    # Exception handlers
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """Handle HTTP exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "status_code": exc.status_code,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Handle validation errors with Ukrainian messages."""
        errors = []
        for error in exc.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            message = error["msg"]

            # Convert common validation messages to Ukrainian
            if "field required" in message:
                message = "Поле обов'язкове для заповнення"
            elif "ensure this value has at least" in message:
                message = f"Мінімальна довжина: {error['ctx']['limit_value']} символів"
            elif "ensure this value has at most" in message:
                message = f"Максимальна довжина: {error['ctx']['limit_value']} символів"
            elif "value is not a valid email address" in message:
                message = "Невірний формат email адреси"
            elif "string does not match regex" in message:
                message = "Невірний формат даних"

            errors.append(
                {
                    "field": field,
                    "message": message,
                    "type": error["type"],
                }
            )

        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "message": "Помилка валідації даних",
                "details": errors,
                "status_code": 422,
            },
        )

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "message": "KHTRM System працює коректно",
        }

    # Root endpoint
    @app.get("/")
    async def read_root() -> dict[str, str]:
        """Root endpoint."""
        return {
            "message": "Ласкаво просимо до KHTRM System",
            "description": "Business Resource Management для транспортного парку",
            "version": settings.app_version,
            "docs": "/docs",
            "redoc": "/redoc",
        }

    # API v1 routes (will be added when routers are created)
    # from .routers import auth, users, vehicles
    # app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
    # app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    # app.include_router(vehicles.router, prefix="/api/v1/vehicles", tags=["vehicles"])

    # Dispatcher routes
    from .routers import dispatcher

    app.include_router(dispatcher.router, prefix="/api/dispatcher", tags=["dispatcher"])

    return app


# Create the FastAPI app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )
