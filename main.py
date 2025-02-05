from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import re

app = FastAPI()

student_db = { 1001: {"name": "ali", "grades": {"Mathematics": "A", "Physics": "B"}},
    1002: {"name": "saim", "grades": {"Mathematics": "B", "Physics": "A"}}}


@app.get("/students/{student_id}")
def status(student_id: int, st_grades: bool = False, semester: Optional [str] = None, regex ="^(Fall|Spring|Summer)\\d{4}$"):
    try:
        if student_id <= 1000 or student_id >= 9999:
            raise HTTPException(status_code=422, detail="Student not found")
        if student_id not in student_db:
            raise ValueError("studient not found")
        student_data = student_db[student_id]
        response_data = {"student_id":student_id, "student_name": student_data["name"]}
        if st_grades:
            response_data["grades"] = student_data["grades"]
        if semester:
            if not re.match("^(Fall|Spring|Summer)\d{4}$", semester):
                raise ValueError("Semester must be in the format 'FallYYYY', 'SpringYYYY', or 'SummerYYYY'")
        response_data["semester"] = semester
        return {"data":response_data,}
    except Exception as e:
        return {"message": str(e),
                "status": "error",
                "data": "null"}

class register(BaseModel):
    name: str
    email: str
    age: int
    courses: list[str] 


@app.post("/students/register")
def new(register: register):
    try:
        if not re.match("^[A-Za-z\s]{1,50}$", register.name):
            raise ValueError("name contain a string include 1-50 characters, must contain only alphabets and spaces")
        if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", register.email):
            raise ValueError("Invalid email address")
        if register.age <18 or register.age > 30:
            raise ValueError("age must be between 18-30")
        if not (1 <= len(register.courses) <= 5):
            raise ValueError("The list must contain between 1 and 5 courses.") 
        if len(register.courses) != len(set(register.courses)):
            raise ValueError("Duplicate course names are not allowed.")
        for course in register.courses:
            if not (5 <= len(course) <= 30):
                raise ValueError(f"Course name '{course}' must be between 5 and 30 characters long.")
        return{"new studient for registration": register}
    except Exception as e:
        return {"message": str(e),
                "status": "error",
                "data": "null"}
    
class update_email(BaseModel):
    email: str

database_2 = [{ 1111: {"name": "Aslam", "email": "a.aslam@gmail.com", "age": "27", "CGPA": "3.9"}},
              { 2222: {"name": "Dawood", "email": "d.dawood@gmail.com", "age": "25", "CGPA": "3.5"}},
              { 3333: {"name": "Sohaib", "email": "s.sohaib@gmail.com", "age": "22", "CGPA": "1.9"}}
              ]
@app.put("/students/{student_id}/update_my_email")
def new(student_id: int,update_email: update_email):
    try:
        if student_id <= 1000 or student_id >= 9999:
            raise ValueError("id shoud be greater then 1000 and less then 9999")
        if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", update_email.email):
            raise ValueError("Invalid email address")
        student_found = False
        for student in database_2:
            if student_id in student:
                student[student_id]["email"] = update_email.email
                student_found = True
                break
        if not student_found:
            raise ValueError("studient not found")
        response_data = {student_id: student[student_id]}
        return{"information": response_data}
    except Exception as e:
        return {"message": str(e),
                "status": "error",
                "data": "null"}