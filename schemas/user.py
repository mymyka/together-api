import pydantic
import typing as t


class User(pydantic.BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
