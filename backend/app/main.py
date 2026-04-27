from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, students, teachers, parents, ai_agent, library, feedback

app = FastAPI(title="Student AI Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(parents.router)
app.include_router(ai_agent.router)
app.include_router(library.router)
app.include_router(feedback.router)

@app.get("/")
def root():
    return {"message": "Student AI Platform API", "docs": "/docs"}