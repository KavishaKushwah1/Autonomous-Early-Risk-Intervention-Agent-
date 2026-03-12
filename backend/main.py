from fastapi import FastAPI

# Initialize the FastAPI app
app = FastAPI(
    title="Autonomous Early Risk Intervention Agent API",
    description="Backend API for tracking student holistic development and AI interventions.",
    version="1.0.0"
)

# A simple root route to test if the server is working
@app.get("/")
def read_root():
    return {"message": "Welcome to the Autonomous Education Agent API! Server is running smoothly."}

# A placeholder route for our AI agent's 'Observe' loop
@app.get("/api/health-check")
def health_check():
    return {"status": "healthy", "agent_status": "standby"}