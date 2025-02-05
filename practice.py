from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {"status": "online"}

@app.get("/ali/{country}/picnic/{day}")
def ali(country,day: int):
    try:
        if day <= 100:
            raise ValueError("day shoud be greater then 100")
        print(day)
        return {
                "hello": "world",
                "data": [1,2,3,4,5],
                "status": "ok",
                "country": country,
                "day": day,
                }
    except Exception as e:
        return {"message": str(e),
                "status": "error",
                "data": "null"}
    
@app.get("/sad")
def ali(id: int,name: str,marks: int):
    try:
        return {
                "hello": "world",
                "data": [1,2,3,4,5],
                "id": id,
                "name": name,
                "marks": marks,
                }
    except Exception as e:
        return {"message": str(e),
                "status": "error",
                "data": "null"}
    
class student(BaseModel):
    name: str
    id: int 
    smester: int
    address: str

@app.post("/sad")
def ali(student: student):
    try:
        if student:
            if student.id < 100:
                raise ValueError("id shoud be greater then 100")
        return {
                "hello": "world",
                "data": [1,2,3,4,5],
                "information": student
                }
    except Exception as e:
        return {"message": str(e),
                "status": "error",
                "data": "null"}
#poetry run uvicorn hello:app --reload