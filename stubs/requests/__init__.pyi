from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import exceptions

class RequestException(Exception): ...

class HTTPError(Exception): ...

@dataclass
class Response: 
    cookies: Dict[str, str] = field(init=False)
    status_code: int = field(init=False)
    content: bytes = field(init=False)
    text: str = field(init=False)
    url: str = field(init=False)

    def json(self): ...
    def raise_for_status(self): ...

@dataclass
class Session:
    cookies: Dict[str, str] = field(init=False)

    def get(
        self,
        url = "",
        data = "",
        timeout:int = 10 ,
        params: Optional[Dict[str, Any]] = {},
        payload: Dict[str, str] = {},
        headers: Dict[str, str] = {},
        proxy: Dict[str, str] = {}
        ) -> Response: ...
    def post(
        self,
        url = "",
        data = "",
        timeout:int = 10,
        files: Any = None,
        payload: Dict[str, str] = {},
        headers: Dict[str, str] = {},
        proxy: Dict[str, str] = {}
        ) -> Response: ...


__all__ = ["exceptions", "Session", "Response", "RequestException", "HTTPError"]