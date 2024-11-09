from typing import TypeVar, Generic, Optional
from app.dto.CamelModel import CamelModel

T = TypeVar('T')

class ResponseDSC(CamelModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
