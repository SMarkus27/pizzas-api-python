# Third-Party Libraries
import logging

from decouple import config
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from uvicorn import run

from src.core.exceptions import AppException, InvalidPriceException, InvalidNameException, \
    InvalidIngredientException
from src.core.settings import get_settings
from src.routes import register_routes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    settings = get_settings()

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

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """Converte exceções de domínio em respostas HTTP padronizadas."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.message, "status_code": exc.status_code},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Captura qualquer exceção não tratada para evitar leaks de stack trace."""
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Internal server error",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
        )

    @app.exception_handler(InvalidPriceException)
    async def price_exception_handler(request: Request, exc: InvalidPriceException):
        return JSONResponse(
            status_code=400,  # Aqui você define o 400!
            content={
                "result": None,
                "message": str(exc),
                "status_code": 400
            }
        )

    @app.exception_handler(InvalidNameException)
    async def price_exception_handler(request: Request, exc: InvalidNameException):
        return JSONResponse(
            status_code=400,  # Aqui você define o 400!
            content={
                "result": None,
                "message": str(exc),
                "status_code": 400
            }
        )

    @app.exception_handler(InvalidIngredientException)
    async def price_exception_handler(request: Request, exc: InvalidIngredientException):
        return JSONResponse(
            status_code=400,  # Aqui você define o 400!
            content={
                "result": None,
                "message": str(exc),
                "status_code": 400
            }
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
