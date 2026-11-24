# Student Management System

## Project Description

The Student Management System is a web application developed using Python and FastAPI to manage student records efficiently.

## Features

- **Create:** Register new students.
- **Read:** View student records and individual student details.
- **Update:** Edit existing student information.
- **Delete:** Remove student records.
- Student profile management.
- Attendance status management.

## Technologies Used

- Python
- FastAPI
- SQLite
- HTML
- CSS
- Jinja2 Templates
- Pydantic

## Project Structure

```text
Student-Management-System/
│
├── main.py
│
└── templates/
    ├── Home.html
    ├── add-student.html
    ├── edit-student.html
    └── single-std.html
```

## How to Run the Project

1. Clone this repository.
2. Install the required Python packages.
3. Run the application:

```bash
uvicorn main:app --reload
```

4. Open your browser:

```text
http://127.0.0.1:8000
```

## Learning Outcomes

This project helped me gain practical experience with FastAPI fundamentals, CRUD operations, routing, form handling, database connectivity and template rendering.
