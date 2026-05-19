# AI Timetable System

An AI-powered dynamic timetable and teacher replacement management system built using React and FastAPI.

## Overview

This project automatically assigns replacement teachers when a teacher is absent by checking:

- Subject compatibility
- Teacher availability
- Current workload
- Free timetable slots
- Scheduling conflicts

The system uses intelligent scheduling logic to generate efficient replacements dynamically.

---

## Features

- Automatic replacement teacher assignment
- Dynamic timetable handling
- Intelligent scheduling logic
- FastAPI backend APIs
- React frontend dashboard
- Real-time frontend-backend communication
- Easy scalability for schools and colleges

---

## Tech Stack

### Frontend
- React
- Axios

### Backend
- FastAPI
- Python

### Database (Planned)
- MongoDB

---

## Project Structure

```bash
AI-Timetable-system
│
├── backend
│   ├── main.py
│   ├── scheduler.py
│   ├── teacher_data.py
│   └── database.py
│
├── frontend
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/reyanalam-byte/AI-Timetable-system.git
```

---

## Backend Setup

```bash
cd backend

pip install fastapi uvicorn pymongo

uvicorn main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

Swagger Docs:

```bash
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm start
```

Frontend runs on:

```bash
http://localhost:3000
```

---

## Working Flow

```text
Teacher marked absent
        ↓
Frontend sends request
        ↓
Backend API receives request
        ↓
Scheduler finds replacement
        ↓
Frontend displays result
```

---

## Future Improvements

- MongoDB integration
- Authentication system
- Admin dashboard
- Timetable visualization
- Analytics and reports
- Notification system
- Machine learning based scheduling

---

## Author

Developed by Reyan Alam
