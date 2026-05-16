from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Classroom, Schedule
from app.dependencies import get_session
from app.schemas.classroom import ClassroomCreate, ClassroomResponse, ClassroomUpdate
from sqlalchemy.orm import Session
from typing import List

classroom_router = APIRouter(prefix="/classroom", tags=["classroom"])

# --- READ ALL ---
@classroom_router.get("/all", response_model=List[ClassroomResponse])
async def get_all_classrooms(session: Session = Depends(get_session)):
    """
    Retrieve a list of all registered classrooms.

    This endpoint fetches all classroom records from the database, which is useful 
    for populating selection components or tables in the user interface.
    """

    classrooms = session.query(Classroom).all()
    return classrooms

# --- READ BY ID ---
@classroom_router.get("/{id_classroom}", response_model=ClassroomResponse)
async def get_classroom_by_id(id_classroom: int, session: Session = Depends(get_session)):
    """
    Retrieve a specific classroom by its unique identifier.

    This endpoint searches for a classroom matching the provided path parameter ID. 
    Returns a 404 error if the classroom cannot be found in the database.
    """
    
    classroom = session.query(Classroom).filter(Classroom.id_classroom == id_classroom).first()
    
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
        
    return classroom

# --- CREATE ---
@classroom_router.post("/create", response_model=ClassroomResponse, status_code=201)
async def create(classroom_schema: ClassroomCreate, session: Session = Depends(get_session)):
    """
    Create a new classroom in the system.

    This endpoint verifies if a classroom with the given room number already exists 
    to prevent duplication. If it does not exist, it registers the classroom and 
    returns its database record containing the auto-generated ID.
    """
    
    classroom = session.query(Classroom).filter(Classroom.room_number == classroom_schema.room_number).first()
    if classroom:
        raise HTTPException(status_code=400, detail="Classroom already exists")
    
    new_classroom = Classroom(**classroom_schema.model_dump())

    session.add(new_classroom)
    session.commit()
    session.refresh(new_classroom)

    return new_classroom

# --- UPDATE (PATCH) ---
@classroom_router.patch("/{id_classroom}", response_model=ClassroomResponse)
async def update_classroom(id_classroom: int, classroom_schema: ClassroomUpdate, session: Session = Depends(get_session)):
    """
    Partially update an existing classroom's details.

    This endpoint performs a partial update (PATCH) using the provided payload. 
    It dynamically overwrites only the fields sent in the request body while 
    preserving the rest of the existing database record.
    """

    db_classroom = session.query(Classroom).filter(Classroom.id_classroom == id_classroom).first()
    
    if not db_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    update_data = classroom_schema.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
        
    for key, value in update_data.items():
        setattr(db_classroom, key, value)
    
    session.commit()
    session.refresh(db_classroom)
    
    return db_classroom

# --- DELETE ---
@classroom_router.delete("/{id_classroom}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_classroom(id_classroom: int, session: Session = Depends(get_session)):
    """
    Delete a classroom from the database.

    This endpoint performs a physical deletion of a classroom record by its ID. 
    It includes a relational integrity check to reject the deletion if there 
    are any active or historical lesson schedules linked to the target room.
    """
    
    db_classroom = session.query(Classroom).filter(Classroom.id_classroom == id_classroom).first()
    
    if not db_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    has_schedules = session.query(Schedule).filter(Schedule.id_classroom == id_classroom).first()
    if has_schedules:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete classroom because it has active or past lesson schedules linked to it."
        )
    
    session.delete(db_classroom)
    session.commit()
    
    return None
