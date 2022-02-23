from fastapi import FastAPI, HTTPException
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from model import Todo
from database import (
    create_todo,
    fetch_all_todos,
    update_todo,
    remove_todo,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

security = HTTPBasic()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "vaishnavi")
    correct_password = secrets.compare_digest(credentials.password, "123456")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/auth",tags=["AUTH"],summary="AUTHORIZE USERS")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}

@app.post("/api/todo/", response_model=Todo,tags=["CREATE"],summary="ADD TODOs")
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response: 
        return response
    raise HTTPException(400, "Something went wrong")


@app.get("/api/todo", tags=["READ"],summary="READ TODOs")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.put("/api/todo/{title}/", response_model=Todo,tags=["UPDATE/MODIFY"],summary="UPDATE/MODIFY TODOs")
async def put_todo(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.delete("/api/todo/{title}",tags=["DELETE"],summary="DELETE TODOs")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the title {title}")