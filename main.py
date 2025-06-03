from fastapi import FastAPI
from database.connection import create_tables
from api.task_routes import router as task_router
from api.user_routes import router as user_router

# Create FastAPI app
app = FastAPI(
    title="Task Manager API",
    description="Task management system with users - demonstrating layered architecture and relationships",
    version="2.0.0"
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

# Include routes
app.include_router(user_router)
app.include_router(task_router)

@app.get("/")
def root():
    return {"message": "Task Manager API with Users is running!"}