from . import base


class User(base.BaseSchema):
    id: int
    username: str
