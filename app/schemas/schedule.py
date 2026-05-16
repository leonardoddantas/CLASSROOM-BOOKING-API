from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.schemas.professor import ProfessorResponse
from app.schemas.classroom import ClassroomResponse

class ScheduleBase(BaseModel):
    schedule_code: str
    reservation_date: date

class ScheduleCreate(ScheduleBase):
    id_professor: int
    id_classroom: int

class ScheduleUpdate(BaseModel):
    schedule_code: Optional[str] = None
    reservation_date: Optional[date] = None
    id_professor: Optional[int] = None
    id_classroom: Optional[int] = None

class ScheduleResponse(ScheduleBase):
    id_schedule: int
    id_professor: int
    id_classroom: int
    
    professor: ProfessorResponse
    classroom: ClassroomResponse

    class Config:
        from_attributes = True