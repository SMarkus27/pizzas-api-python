# Third-Party Libraries
import logging

from decouple import config
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from uvicorn import run

from src.domain.exceptions import (
    AppError,
    InvalidIngredientError,
    InvalidNameError,
    InvalidPriceError,
)
from src.infrastructure.http import register_routes


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Pizzas API",
        description="API para gerenciar pizzas, pedidos e estoque.",
        version="2.0.0",
    )

    # --- CORS ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError):
        """Converte erros de domínio em respostas HTTP padronizadas."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.message, "status_code": exc.status_code},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception):
        """Captura qualquer exceção não tratada para evitar leaks de stack trace."""
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Internal server error",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
        )

    @app.exception_handler(InvalidPriceError)
    async def invalid_price_handler(_: Request, exc: InvalidPriceError):
        return JSONResponse(
            status_code=400,
            content={"result": None, "message": str(exc), "status_code": 400},
        )

    @app.exception_handler(InvalidNameError)
    async def invalid_name_handler(_: Request, exc: InvalidNameError):
        return JSONResponse(
            status_code=400,
            content={"result": None, "message": str(exc), "status_code": 400},
        )

    @app.exception_handler(InvalidIngredientError)
    async def invalid_ingredient_handler(_: Request, exc: InvalidIngredientError):
        return JSONResponse(
            status_code=400,
            content={"result": None, "message": str(exc), "status_code": 400},
        )

    # --- Routes ---
    register_routes(app)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(config("APPLICATION_PORT"))
    host = config("APPLICATION_HOST")
    run(
        "main:app",
        host=host,
        access_log=True,
        port=port,
        reload=True,
    )
