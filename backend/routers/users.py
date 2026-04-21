from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from schemas.users import UserRequest
from curd.users import create_user, get_user_by_username, create_token

router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
# 注册流程：验证用户是否存在 -> 创建用户 -> 生成token -> 响应结果
    
    # 验证用户是否存在
    verify_user = await get_user_by_username(db, user_data.username)
    if verify_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    
    # 创建用户
    user = await create_user(db, user_data)
    # 生成token
    token = await create_token(db, user.id)
    return {
        "code": 200,
        "message": "用户注册成功",
        "data": {
            "token": token,
            "userInfo":{
                "id": user.id,
                "username": user.username,
                "bio": user.bio,
                "avatar": user.avatar,
            }
        }
    }