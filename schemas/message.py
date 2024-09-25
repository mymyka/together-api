import pydantic


class Message(pydantic.BaseModel):
    id: int
    content: str
    user: 'User'
