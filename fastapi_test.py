# fastapi_app.py
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置模板
templates = Jinja2Templates(directory="templates")

# 模拟数据库
db = {
    "users": [
        {"id": 1, "username": "user1", "email": "user1@example.com"},
        {"id": 2, "username": "user2", "email": "user2@example.com"}
    ],
    "products": [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Phone", "price": 699.99}
    ]
}

# Pydantic模型
class User(BaseModel):
    username: str
    email: str
    disabled: Optional[bool] = None

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# 依赖项
def get_db():
    return db

# 路由
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/users/", response_model=list[User])
async def read_users(db: dict = Depends(get_db)):
    return db["users"]

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: dict = Depends(get_db)):
    user = next((u for u in db["users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=User, status_code=201)
async def create_user(user: User, db: dict = Depends(get_db)):
    new_user = {
        "id": len(db["users"]) + 1,
        **user.dict()
    }
    db["users"].append(new_user)
    return new_user

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int, db: dict = Depends(get_db)):
    product = next((p for p in db["products"] if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.api_route("/mixed", methods=["GET", "POST"])
async def mixed_handler(request: Request):
    if request.method == "GET":
        return {"message": "This is a GET request"}
    elif request.method == "POST":
        data = await request.json()
        return {"message": "Got POST data", "data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)