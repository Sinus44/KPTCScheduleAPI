from pydantic import BaseModel


class PingResponse(BaseModel):
    random: float
