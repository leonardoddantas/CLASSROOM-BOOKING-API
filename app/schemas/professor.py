from pydantic import BaseModel
from typing import Optional

class ProfessorBase(BaseModel):
    name: str
    registration_number: str
    department: str

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorUpdate(BaseModel):
    name: Optional[str] = None
    registration_number: Optional[str] = None
    department: Optional[str] = None

class ProfessorResponse(ProfessorBase):
    id_professor: int

    class Config:
        from_attributes = True
