from fastapi import APIRouter
from pydantic import BaseModel


# Tạo APIRouter
user_router = APIRouter(prefix="/users", tags=["Users"])


# Request Model
class UserCreate(BaseModel):
    name: str
    age: int


# Response Model
class UserResponse(BaseModel):
    id: int
    name: str
    age: int


# Fake Database
fake_users_db = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
]


# Tạo Class-Based View
class UserAPI:
    def __init__(self):
        self.db = fake_users_db  # Giả lập database

    async def get_users(self) -> list[UserResponse]:
        """Lấy danh sách tất cả users"""
        return self.db

    async def get_user(self, user_id: int) -> UserResponse:
        """Lấy thông tin user theo ID"""
        for user in self.db:
            if user["id"] == user_id:
                return user
        return {"error": "User not found"}

    async def create_user(self, user: UserCreate) -> UserResponse:
        """Tạo user mới"""
        new_user = {"id": len(self.db) + 1, "name": user.name, "age": user.age}
        self.db.append(new_user)
        return new_user


# Khởi tạo class UserAPI
user_api = UserAPI()

# Định nghĩa route bằng class
user_router.add_api_route(
    "/", user_api.get_users, methods=["GET"], response_model=list[UserResponse]
)
user_router.add_api_route(
    "/{user_id}", user_api.get_user, methods=["GET"], response_model=UserResponse
)
user_router.add_api_route(
    "/", user_api.create_user, methods=["POST"], response_model=UserResponse
)
