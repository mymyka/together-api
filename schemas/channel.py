import pydantic
from . import message
import typing as t


class Channel(pydantic.BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        orm_mode = True


class ChannelInfo(Channel):
    messages: t.List[message.Message]

    class Config:
        from_attributes = True
        orm_mode = True
