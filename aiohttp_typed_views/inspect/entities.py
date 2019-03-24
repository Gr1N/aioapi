from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from pydantic import BaseModel

__all__ = ("HandlerMeta",)


@dataclass(frozen=True)
class HandlerMeta:
    name: str
    request_type: Optional[BaseModel] = None
    request_body_pair: Optional[Tuple[str, Any]] = None
    request_path_mapping: Optional[Dict[str, Any]] = None
    request_query_mapping: Optional[Dict[str, Any]] = None
