from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student App!"}

@app.get("/student")
def read_student():
    student = {
        "name": "John Doe",
        "age": 20,
        "course": "Computer Science",
        "is_graduated": False
    }
    return student
