import pydantic
from . import user


class Message(pydantic.BaseModel):
    id: int
    content: str
    user: user.User | None

    class Config:
        from_attributes = True
        orm_mode = True
