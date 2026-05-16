from pydantic import BaseModel
from typing import Optional

class ClassroomBase(BaseModel):
    room_number: str
    building: str

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomUpdate(BaseModel):
    room_number: Optional[str] = None
    building: Optional[str] = None

class ClassroomResponse(ClassroomBase):
    id_classroom: int

    class Config:
        from_attributes = True
