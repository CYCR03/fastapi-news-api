
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from config.db_config import get_db
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserUpdatePwdRequest
from curd.users import create_user, get_user_by_username, create_token, authenticate_user, update_user, change_password
from utils.response import success_response
from utils.auth import get_current_user

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

    # return {
    #     "code": 200,
    #     "message": "用户注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo":{
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar,
    #         }
    #     }
    # }
    # model_validate将任意数据转换为符合模型定义的对象
    response_data = UserAuthResponse(
        token=token, 
        user_info=UserInfoResponse.model_validate(user)
        )
    return success_response(message="注册成功", data=response_data)

@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登陆逻辑：验证用户是否存在 -> 验证密码 -> 生产token -> 响应结果
    user = await authenticate_user(db, user_data.username, user_data.password)

    # 验证用户是否存在/密码是否正确
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    
    # 生产token
    token = await create_token(db, user.id)
    response_data = UserAuthResponse(
        token=token,
        user_info=UserInfoResponse.model_validate(user)
    )
    
    return success_response(message="登陆成功", data=response_data)

@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))

@router.put("/update")
async def update_user_info(
    user_data : UserUpdateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)

):
    update_user_data = await update_user(db, user.id, user_data)
    # 要传入用户的更新信息，token验证，数据库
    return success_response(message="更新用户信息成功", data=UserInfoResponse.model_validate(update_user_data))

@router.put("/password")
async def update_user_password(
    password_data: UserUpdatePwdRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):  
    change_pwd = await change_password(db, user, password_data.old_password, password_data.new_password)

    # 返回False时，为旧密码错误
    if not change_pwd:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="旧密码错误")
    
    return success_response(message="更新用户密码成功")