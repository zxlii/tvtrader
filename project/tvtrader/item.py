from pydantic import BaseModel  # FastAPI 定义请求体，需要 Pydantic 模型。需要从pydantic中导入BaseModel。

class Item(BaseModel):
    price: str
    stop: str