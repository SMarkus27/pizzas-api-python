# Third-Party Libraries
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from src.routes.base.route import BaseRouter

router = BaseRouter.get_router_instance()
app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    port = int(config("APPLICATION_PORT"))
    host = config("APPLICATION_HOST")
    run(
        app,
        host=host,
        access_log=True,
        port=port,
    )
