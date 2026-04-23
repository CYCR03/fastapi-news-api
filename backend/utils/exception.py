import traceback
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
# 开发模式：返回错误的详细信息
# 生产模式：返回简化的错误信息
DEBUG_MODE = True

# Requst为获取当前http请求的详细信息
async def http_exception_handler(request:Request, exc: HTTPException):
    """
    处理HTTP异常
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code" : exc.status_code,
            "message" : exc.detail if DEBUG_MODE else "服务器内部错误",
            'data' : None
        }
    )

async def integrity_exception_handler(request:Request, exc: IntegrityError):
    """
    处理数据库完整性约束异常
    """
    error_msg = str(exc.orig)

    # 通过判断原始错误信息中包含的特定关键字，来区分是哪种完整性冲突
    # "username_UNIQUE" 是数据库中定义的唯一索引名，"Duplicate entry" 是 MySQL 插入重复的唯一数据时的报错提示
    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户名已存在"
    # 外键关联冲突的报错
    elif "FOREIGN KEY" in error_msg:
        detail = "关联数据不存在"
    else:
        detail = "数据约束冲突，请检查输入"

    if DEBUG_MODE:
        error_data = {
            "error_type": "IntegrityError",
            "error_msg" : error_msg,
            "path" : str(request.url) 
        }
    else:
        error_data = None

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": detail,
            "data": error_data
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    处理除完整性约束之外的其他通用数据库异常 (如连接失败、SQL语法错误等)
    作为全局兜底的数据库异常处理器
    """
    # 针对开发模式与生产模式做不同处理，避免在生产环境泄露底层数据库结构和代码堆栈
    if DEBUG_MODE:
        error_data = {
            # 获取异常具体类名（例如 OperationalError, DataError 等）
            "error_type" : type(exc).__name__,
            # 异常的简要描述信息
            "error_detail" : str(exc),
            # 获取异常的完整堆栈信息，并格式化为字符串，方便在日志中直接定位报错代码行
            "traceback" : traceback.format_exc(),
            # 记录出错时请求的完整 URL 路径
            "path" : str(request.url)
        }
    else: 
        error_data = None
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库操作失败，请稍后再试",
            "data": error_data
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """
    处理通用异常
    """
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }
    else:
        error_data = None
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": error_data
        }
    )
    