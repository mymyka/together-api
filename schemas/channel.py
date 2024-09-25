import pydantic
import typing as t


class Channel(pydantic.BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
