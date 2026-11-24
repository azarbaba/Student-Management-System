
from fastapi import FastAPI,Request,Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel,Field
from fastapi.responses import RedirectResponse
import sqlite3

class Student(BaseModel):
    name:str
    age:int=Field(ge=18,le=45)
    gender:str
    marks:int
    course:str
    image:str
    status:int=Field(le=1,ge=0)

def get_connection():
    connection = sqlite3.connect(
        "students.db"
    )
    return connection

get_connection()

def create_table():
    connection=get_connection()
    cursor=connection.cursor()

    q="""
    CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT,
    age INTEGER,
    gender TEXT,
    marks INTEGER,
    course TEXT,
    image TEXT,
    status INTEGER
    )
    """
    cursor.execute(q)
    connection.commit()
    connection.close()

create_table()

templates=Jinja2Templates(
    directory="templates"
)

app=FastAPI()

@app.get("/")
def home(req:Request):
    connection=get_connection()
    cursor=connection.cursor()

    q="select * from students"
    cursor.execute(q)
    students=cursor.fetchall()
    print(students)
    connection.close()

    return templates.TemplateResponse(
        request=req,
        name="Home.html",
        context={"stds":students}
    )

@app.get("/students/{std_id:int}")
def single_std(req:Request,std_id:int,display_id:int=1):
    connection=get_connection()
    cursor=connection.cursor()

    q="select * from students where id=?"
    cursor.execute(q,(std_id,))
    student=cursor.fetchone()
    print(student)

    connection.close()
    return templates.TemplateResponse(
        request=req,
        name="single-std.html",
        context={
            "std":student,
            "display_id":display_id
        }
    )

@app.get("/students/add")
def send_std_form(req:Request):
    return templates.TemplateResponse(
        request=req,
        name="add-student.html",
        context={}
    )

@app.post("/std/delete/{std_id}")
def delete_std(std_id:int):
    connection=get_connection()
    cursor=connection.cursor()
    q="DELETE FROM students where id=?"
    cursor.execute(q,(std_id,))
    connection.commit()
    connection.close()
    return RedirectResponse(url="/",status_code=303)


@app.post("/students/add")
def create_std(
    name=Form(),
    age=Form(),
    gender=Form(),
    marks=Form(),
    course=Form(),
    image=Form(),
    status=Form()
    ):
    student=Student(
        name=name,
        age=age,
        gender=gender,
        marks=marks,
        course=course,
        image=image,
        status=status
    )
    values=(student.name,student.age,student.gender,student.marks,student.course,student.image,student.status)

    connection=get_connection()
    cursor=connection.cursor()
    q= """
    INSERT INTO students(name,age,gender,marks,course,image,status)
    values
    (?,?,?,?,?,?,?)
    """
    cursor.execute(q,values)
    connection.commit()
    connection.close()

    return RedirectResponse(url="/",status_code=303)

@app.get("/students/edit/{std_id}")
def edit_std(req:Request,std_id):

    connection=get_connection()
    cursor=connection.cursor()
    q="select * from students where id=?"

    cursor.execute(q,(std_id,))

    student=cursor.fetchone()
    print(student)

    return templates.TemplateResponse(
        request=req,
        name="edit-student.html",
        context={
            "std":student
        }
    )

@app.post("/students/edit/{std_id}")
def update_std(
    std_id:int,
    name=Form(),
    age=Form(),
    gender=Form(),
    marks=Form(),
    course=Form(),
    image=Form(),
    status=Form()
    ):
    std_obj=Student(
        name=name,
        age=age,
        gender=gender,
        marks=marks,
        course=course,
        image=image,
        status=status
    )

    connection=get_connection()
    cursor=connection.cursor()

    q="""
    UPDATE students
    SET name= ?,
    age = ?,
    marks=?,
    gender=?,
    course=?,
    image=?,
    status=? where id=?
    """

    cursor.execute(q,(std_obj.name,std_obj.age,std_obj.marks,std_obj.gender,std_obj.course,std_obj.image,std_obj.status,std_id))
    connection.commit()
    connection.close()
    return RedirectResponse(url="/",status_code=303)
