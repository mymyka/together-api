import pydantic


class BaseSchema(pydantic.BaseModel):
    class Config:
        from_attributes = True
