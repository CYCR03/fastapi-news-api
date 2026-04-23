from fastapi import FastAPI
from routers import news, users
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_hendlers import register_exception_handlers 

app = FastAPI()

# 注册全局异常处理
register_exception_handlers(app)

# 配置 CORS 中间件，允许前端跨域访问
origins = [
    'http://localhost:3000',  # 前端开发服务器地址
    'http://localhost:5173',  # Vite 开发服务器地址
    'http://127.0.0.1:5173',  # Vite 开发服务器地址（IP 形式）
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的来源列表
    allow_credentials=True, # 允许携带凭证（如 cookies）
    allow_methods=["*"],    # 允许所有方法
    allow_headers=["*"],    # 允许所有请求头
)

@app.get("/")
async def root():
    return {"message":"你好"}

# 注册新闻模块路由
app.include_router(news.router)
# 注册用户模块路由
app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
