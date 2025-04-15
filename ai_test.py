from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from users import user_router

app = FastAPI()


app.include_router(user_router, prefix="/users")


# Model dữ liệu trả về khi thành công
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None


class ListItem(BaseModel):
    items: list[ItemResponse]


# Model lỗi
class ErrorResponse(BaseModel):
    detail: str


@app.post(
    path="/items/{id}",
    response_model=ListItem,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Lỗi đầu vào"},
        500: {
            "model": ErrorResponse,
            "description": "Internal Server Error - Lỗi hệ thống",
        },
    },
    summary="Lấy thông tin sản phẩm",
)
def get_item(id: str, item_id: ListItem):
    """
    Trả về thông tin sản phẩm dựa trên `item_id`.

    - **200**: Trả về thông tin sản phẩm nếu tồn tại.
    - **400**: Lỗi nếu `item_id` không hợp lệ.
    - **500**: Lỗi hệ thống.
    """
    # if item_id <= 0:
    #     raise HTTPException(status_code=400, detail="ID phải lớn hơn 0")

    print(id)
    try:
        return {
            "id": 1,
            "name": "Laptop",
            "price": 1200.5,
            "description": "Laptop gaming",
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Lỗi không xác định")
