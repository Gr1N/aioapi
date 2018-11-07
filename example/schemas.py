from pydantic import BaseModel

__all__ = ("User",)


class User(BaseModel):
    first_name: str
    last_name: str
