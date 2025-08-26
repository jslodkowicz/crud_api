from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import Optional, List

app = FastAPI()

DATA_FILE = "users.json"

class User(BaseModel):
    id: Optional[int] = None
    name: str 
    email: str

def read_users():
    try:
        with open(DATA_FILE, "r") as f:
            users = json.load(f)
        return users
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_next_id(users):
    if not users:
        return 1
    return max(user["id"] for user in users) + 1

@app.post("/users", response_model=User, status_code=201)
def create_user(user: User):
    users = read_users()
    user.id = get_next_id(users)
    users.append(user.dict())
    write_users(users)
    return user

@app.get("/users", response_model=List[User])
def get_users():
    return read_users()

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    users = read_users()
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    users = read_users()
    for i, existing_user in enumerate(users):
        if existing_user["id"] == user_id:
            user.id = user_id
            users[i] = user.dict()
            write_users(users)
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    users = read_users()
    for i, user in enumerate(users):
        if user["id"] == user_id:
            del users[i]
            write_users(users)
            return
    raise HTTPException(status_code=404, detail="User not found")
