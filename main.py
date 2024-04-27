from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException 
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()


db: List[User] = [
    User(
        id=uuid4(), 
        # id=UUID("d9ff033c-e9b8-4e4b-9593-fc575e29943c"), 
        first_name="oluchi", 
        last_name="faith",
        gender=Gender.female,
        roles=[Role.student]
    ),

    User(
        id=uuid4(), 
        first_name="peace", 
        last_name="chisom",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
        )
]

@app.get("/")
def root():
    return {"hello dear"}

@app.get("/users")
async def fetch_users():
    return db;

@app.post("/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}
@app.put("/users{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name 

            if user_update.last_name is not None:
                user.last_name = user_update.last_name

            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            return 
        raise HTTPException(
            status_code=404 ,
            details=f"user with id: {user_id} does not exists"
        )



@app.delete("/users{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return 

    raise HTTPException(
        status_code=404, 
        detail=f"user with id: {user_id} does not exists"
    )
