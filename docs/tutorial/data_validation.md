# Data Validation

`AIOAPI` relies on `pydantic` for data validation. To know how to work with `pydantic` and to get know all about its features please follow [official documentation](https://pydantic-docs.helpmanual.io/).

Below you can find a simple example of `pydantic`s model declaration:

```python
from datetime import datetime
from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: datetime = None
    friends: List[int] = []
```
