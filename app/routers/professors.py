from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Professor, Schedule
from app.dependencies import get_session
from app.schemas.professor import ProfessorCreate, ProfessorResponse, ProfessorUpdate
from sqlalchemy.orm import Session
from typing import List

professor_router = APIRouter(prefix="/professor", tags=["professor"])

# --- READ ALL ---
@professor_router.get("/all", response_model=List[ProfessorResponse])
async def get_all_professors(session: Session = Depends(get_session)):
    """
    Retrieve a list of all registered professors.

    Useful for populating selection dropdowns when staff members are creating 
    new room reservations.
    """
    return session.query(Professor).all()


# --- READ BY ID ---
@professor_router.get("/{id_professor}", response_model=ProfessorResponse)
async def get_professor_by_id(id_professor: int, session: Session = Depends(get_session)):
    """
    Get a specific professor's details by their unique ID.

    Returns a 404 error if the professor identifier does not exist in the database.
    """
    professor = session.query(Professor).filter(Professor.id_professor == id_professor).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor

# --- CREATE ---
@professor_router.post("/create", response_model=ProfessorResponse, status_code=201)
async def create_professor(professor_schema: ProfessorCreate, session: Session = Depends(get_session)):
    """
    Register a new professor in the system.

    Checks if the registration number (matrícula) is already in use to prevent 
    duplicated records. Returns the newly created professor with their database ID.
    """
    # Validação pelo número de matrícula (registration_number deve ser único)
    existing_prof = session.query(Professor).filter(
        Professor.registration_number == professor_schema.registration_number
    ).first()
    
    if existing_prof:
        raise HTTPException(status_code=400, detail="Professor with this registration number already exists")

    new_professor = Professor(**professor_schema.model_dump())
    session.add(new_professor)
    session.commit()
    session.refresh(new_professor)
    return new_professor

# --- UPDATE (PATCH) ---
@professor_router.patch("/{id_professor}", response_model=ProfessorResponse)
async def update_professor(id_professor: int, professor_schema: ProfessorUpdate, session: Session = Depends(get_session)):
    """
    Partially update a professor's information.

    Updates only the fields provided in the request payload (e.g., changing departments) 
    while leaving other attributes untouched.
    """
    db_professor = session.query(Professor).filter(Professor.id_professor == id_professor).first()
    if not db_professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    update_data = professor_schema.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    for key, value in update_data.items():
        setattr(db_professor, key, value)

    session.commit()
    session.refresh(db_professor)
    return db_professor


# --- DELETE ---
@professor_router.delete("/{id_professor}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_professor(id_professor: int, session: Session = Depends(get_session)):
    """
    Delete a professor record from the database.

    Includes a safety check to reject deletion if the professor has any active 
    or historical classroom schedules associated with them.
    """
    db_professor = session.query(Professor).filter(Professor.id_professor == id_professor).first()
    if not db_professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    has_schedules = session.query(Schedule).filter(Schedule.id_professor == id_professor).first()
    if has_schedules:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete professor because they have linked room reservations in the system."
        )

    session.delete(db_professor)
    session.commit()
    return None