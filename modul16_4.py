from fastapi import FastAPI, Path
from typing import List
from pydantic import BaseModel

    # Создаем экземпляр приложения FastAPI
app = FastAPI()
    # Создайте словарь users
users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
async def start_page() -> dict:
    return {"message": "Главная страница"}

 # 4 CRUD запроса:
@app.get('/users')
async def get_message() -> dict:
    return users

@app.post('/user/{username}/{age}')
async def create_user(username:str = Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser'),
                      age:int = Path(ge=18, le=120, description='Enter age', example='77')) -> dict:
    user_id = (users["-1"].id + 1) if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                     example="UrbanUser")],
        user_id: str = Path(ge=1, le=100, description="Enter User ID", example="25"),
        age: int = Path(ge=18, le=120, description="Enter age", example="24")) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return {"user_id": user_id, "username": username, "age": age}

@app.delete('/user/{user_id}')
async def del_user(user_id: str = Path(ge=1, le=100, description="Enter User ID", example="25"),) -> str:
    try:
        users.pop(user_id)
        return f'User {user_id} was deleted'
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")

