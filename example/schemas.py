from pydantic import BaseModel

__all__ = ("HelloBodyRequest",)


class HelloBodyRequest(BaseModel):
    name: str
    age: int = 27
