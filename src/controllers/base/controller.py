import json

import fastapi

from src.core.interfaces.controllers.base.interface import IBaseController


class BaseController(IBaseController):
    @staticmethod
    async def run(callback: callable, payload: dict):
        response_data = await callback(payload)
        return fastapi.Response(
            status_code=response_data.get("status_code"),
            content=json.dumps(response_data),
            headers={"Content-type": "application/json"},
        )
