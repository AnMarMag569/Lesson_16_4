from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()
class User(BaseModel):
    id: int
    username: str = Field(..., min_length=5, max_length=20)
    age: int = Field(..., gt=17, lt=100)

users : List[User] = []
@app.get("/user", response_model=List[User])
async def read_users():
    return [user for user in users]

@app.post("/user", response_model=User)
async def post_user(username, age):
    new_id = max((u.id for u in users), default=0) + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}", response_model=User)
async def update_user(id: int, username, age):
    for i in users:
        if i.id == id:
            i.username = username
            i.age = age
            return i
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}", response_model=dict)
async def delete_user(id: int):
    for i, d in enumerate(users):
        if d.id == id:
            del users[i]
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User was not found")


# uvicorn module_16_4:app --reload