# Smart Classroom Scheduler API 🚀

An IoT-based classroom energy management and scheduling system designed for **UFRN - Campus Caicó**. This REST API acts as the core backend, managing room reservations and preventing scheduling conflicts to optimize electricity consumption via hardware integration.

---

## 🛠️ Tech Stack & Architecture

The project follows a modular, scalable architecture using **Python** and modern frameworks:

* **FastAPI**: High-performance web framework for building APIs.
* **SQLAlchemy**: Object-Relational Mapping (ORM) to interact with the database.
* **Alembic**: Database migrations management.
* **SQLite**: Lightweight, relational database used for the local environment.
* **Pydantic (v2)**: Data validation and settings management using Python type hints.

---

## 📂 Project Structure

The repository is organized following professional clean-code standards, separating responsibilities into dedicated modules:

```text
classroom-booking-api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application factory & router registration
│   ├── database.py       # SQLAlchemy engine & SessionLocal configurations
│   ├── models.py         # SQLAlchemy database models (ORMs)
│   ├── dependencies.py   # Database session yield injectables
│   ├── routers/          # Route controllers divided by entities
│   │   ├── classrooms.py
│   │   ├── professors.py
│   │   └── schedules.py  # Core business logic (conflict checks)
│   └── schemas/          # Pydantic validation and serialization models
│       ├── classroom.py
│       ├── professor.py
│       └── schedule.py
├── alembic/              # Database migration environment
├── alembic.ini           # Alembic configuration file
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```
## 🧠 Core Features & Business Rules

### 1. Classroom Management (CRUD)
* **Full Campus Management:** Complete control over campus rooms and physical buildings (e.g., CERES).
* **Relational Safety Lock:** Preventative check to block the deletion of classrooms that have active or historical lesson schedules linked to them.

### 2. Professor Directory (CRUD)
* **Unique Identification:** Strict unique constraints on institutional registration numbers (`registration_number`) to prevent duplicate teacher profiles.

### 3. Smart Scheduling & Conflict Prevention (`Schedules`)
This is the heart of the system. When registering a reservation (with a UFRN `schedule_code` like `23M56`), the API automatically executes complex validation checks:
* **Classroom Overlap:** Blocks the operation if the target room is already booked on that specific date and time slot.
* **Professor Overlap:** Blocks the operation if the professor is already assigned to another room during the exact same time slot.

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Virtual Environment tool (`venv`)

### Installation & Setup

1. **Clone the repository:**
   
   ```bash
   git remote add origin https://github.com/leonardoddantas/CLASSROOM-BOOKING-API.git
   cd CLASSROOM-BOOKING-API
   ```

  2. **Create and activate the virtual environment:**
     
     ```bash
     # Windows (PowerShell)
     python -m venv venv
     .\venv\Scripts\activate
     ```

   3. **Install the dependencies:**
      
      ```bash
      pip install -r requirements.txt
      ```
     
   4. **Run database migrations (Alembic):**

        ```bash
        # Generate the SQLite local file and tables
        alembic upgrade head
       ```
  5. **Start the development server:**
     
     ```bash
      uvicorn app.main:app --reload
     ```

     The API will be up and running at http://127.0.0.1:8000.

## 📑 Interactive API Documentation

Once the server is running, you can access the interactive Swagger UI documentation to test all endpoints (POST, GET, PATCH, DELETE) directly from your browser:

🔗 Interactive Docs: http://127.0.0.1:8000/docs
