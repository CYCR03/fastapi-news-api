import datetime
from unittest import result
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security 

# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    db_sql = select(User).where(User.username == username)
    result = await db.execute(db_sql)
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 先密码加密 -> 再添加到数据库中
    hashed_password = security.hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    # 刷新对象，重新获取该对象在存入数据库后的实际数据（既为了获取部分自增或默认值的字段的值）
    await db.refresh(user)  
    return user

# 创建用户令牌
async def create_token(db: AsyncSession, user_id: int):
    '''
    生成token + 设置过期时间 + 
    查询数据库当前用户是否有token + token存在更新; 不存在则添加

    这里的token使用uuid4生成
    ''' 
    token = str(uuid.uuid4())
    expires_at = datetime.now() + datetime.timedelta(days=7)

    db_sql = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(db_sql)
    user_token = result.scalar_one_or_none()

    if user_token:
        # 用户已存在令牌，更新令牌
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        # 用户不存在令牌，添加令牌
        user_token = UserToken(
            user_id=user_id, 
            token=token, 
            expires_at=expires_at
        )
        db.add(user_token)
    # 提交数据库
    await db.commit()
    return token
