from fastapi import FastAPI
from controllers import event_controller, participant_controller
from middleware.cors_middleware import add_cors

app = FastAPI(title="Event Management API")

add_cors(app)

@app.get("/")
def root():
    return {
        "message": "Welcome to Event Management API",
        "version": "1.0",
        "endpoints": {
            "events": "/events",
            "participants": "/participants",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }

app.include_router(event_controller.router)
app.include_router(participant_controller.router)