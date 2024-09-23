import pydantic
from .channel import Channel
import typing as t


class UserResponse(pydantic.BaseModel):
    id: int
    username: str
    channels: t.List[Channel]

    class Config:
        from_attributes = True
