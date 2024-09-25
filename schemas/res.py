import pydantic


class Ok(pydantic.BaseModel):
    message: str = "ok"
