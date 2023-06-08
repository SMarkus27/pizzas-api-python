from typing import Union, List

from pydantic import BaseModel


class BaseResponse(BaseModel):
    result: Union[dict, List[dict]]
    message: str
    status_code: int
