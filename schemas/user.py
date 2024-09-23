import pydantic


class UserResponse(pydantic.BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
