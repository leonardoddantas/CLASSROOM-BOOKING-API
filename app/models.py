from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Professor(Base):
    __tablename__ = "professors"

    id_professor = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    registration_number = Column(String, unique=True, nullable=False)
    department = Column(String)

    schedules = relationship("Schedule", back_populates="professor")

class Classroom(Base):
    __tablename__ = "classrooms"

    id_classroom = Column(Integer, primary_key=True, autoincrement=True)
    room_number = Column(String, nullable=False)
    building = Column(String, nullable=False)

    schedules = relationship("Schedule", back_populates="classroom")

class Schedule(Base):
    __tablename__ = "schedules"

    id_schedule = Column(Integer, primary_key=True, autoincrement=True)
    schedule_code = Column(String, nullable=False) # Ex: 23M56
    reservation_date = Column(Date, nullable=False)
    id_professor = Column(Integer, ForeignKey("professors.id_professor"), nullable=False)
    id_classroom = Column(Integer, ForeignKey("classrooms.id_classroom"), nullable=False)

    professor = relationship("Professor", back_populates="schedules")
    classroom = relationship("Classroom", back_populates="schedules")