from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Schedule, Professor, Classroom
from app.dependencies import get_session
from app.schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleUpdate
from sqlalchemy.orm import Session
from typing import List

schedule_router = APIRouter(prefix="/schedule", tags=["schedule"])

# --- CREATE (Com validação de conflitos) ---
@schedule_router.post("/create", response_model=ScheduleResponse, status_code=201)
async def create_schedule(schedule_schema: ScheduleCreate, session: Session = Depends(get_session)):
    """
    Register a new room reservation.

    Validates if the target classroom and professor exist. Also checks for schedule 
    conflicts to ensure neither the room nor the professor is double-booked on the 
    same date and time slot.
    """
    
    professor = session.query(Professor).filter(Professor.id_professor == schedule_schema.id_professor).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    classroom = session.query(Classroom).filter(Classroom.id_classroom == schedule_schema.id_classroom).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    room_conflict = session.query(Schedule).filter(
        Schedule.id_classroom == schedule_schema.id_classroom,
        Schedule.reservation_date == schedule_schema.reservation_date,
        Schedule.schedule_code == schedule_schema.schedule_code
    ).first()
    
    if room_conflict:
        raise HTTPException(
            status_code=400, 
            detail="Classroom is already reserved for this date and time slot."
        )

    professor_conflict = session.query(Schedule).filter(
        Schedule.id_professor == schedule_schema.id_professor,
        Schedule.reservation_date == schedule_schema.reservation_date,
        Schedule.schedule_code == schedule_schema.schedule_code
    ).first()
    
    if professor_conflict:
        raise HTTPException(
            status_code=400, 
            detail="Professor is already allocated to another classroom for this date and time slot."
        )

    new_schedule = Schedule(**schedule_schema.model_dump())
    session.add(new_schedule)
    session.commit()
    session.refresh(new_schedule)
    return new_schedule


# --- READ ALL ---
@schedule_router.get("/all", response_model=List[ScheduleResponse])
async def get_all_schedules(session: Session = Depends(get_session)):
    """
    Retrieve all room reservations with nested professor and classroom details.
    """
    return session.query(Schedule).all()


# --- READ BY ID ---
@schedule_router.get("/{id_schedule}", response_model=ScheduleResponse)
async def get_schedule_by_id(id_schedule: int, session: Session = Depends(get_session)):
    """
    Get details of a specific reservation by its ID.
    """
    schedule = session.query(Schedule).filter(Schedule.id_schedule == id_schedule).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return schedule


# --- UPDATE (PATCH) ---
@schedule_router.patch("/{id_schedule}", response_model=ScheduleResponse)
async def update_schedule(id_schedule: int, schedule_schema: ScheduleUpdate, session: Session = Depends(get_session)):
    """
    Update reservation details dynamically.
    """
    db_schedule = session.query(Schedule).filter(Schedule.id_schedule == id_schedule).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Reservation not found")

    update_data = schedule_schema.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    for key, value in update_data.items():
        setattr(db_schedule, key, value)

    session.commit()
    session.refresh(db_schedule)
    return db_schedule

# --- DELETE ---
@schedule_router.delete("/{id_schedule}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(id_schedule: int, session: Session = Depends(get_session)):
    """
    Cancel/delete a room reservation.
    """
    db_schedule = session.query(Schedule).filter(Schedule.id_schedule == id_schedule).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Reservation not found")

    session.delete(db_schedule)
    session.commit()
    return None
