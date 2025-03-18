from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    #id: int
    id: Optional[str] = None
    nombre: str
    codigo: str
    estado: str