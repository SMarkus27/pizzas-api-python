import json

import fastapi


class BaseController:

    @staticmethod
    async def run(callback: callable, payload: dict):

        response_data = await callback(payload)
        return fastapi.Response(
            status_code=response_data.get("status_code"),
            content=json.dumps(response_data),
            headers={"Content-type": "application/json"}
        )
