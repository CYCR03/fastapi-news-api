import datetime
import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
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
    expires_at = datetime.datetime.now() + datetime.timedelta(days=7)

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

# 验证用户登陆
async def authenticate_user(db: AsyncSession, username: str, password: str):
    """
    根据用户名查询用户 -> 验证密码 -> 返回用户
    """
    user = await get_user_by_username(db, username)
    # 验证用户是否存在
    if user is None:
        return None
    # 验证用户密码
    if not security.verify_password(password, user.password):
        return None
    return user

# 根据token查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    """
    根据token查询user_token表 -> 验证token -> 再根据user_token的用户id查询user表 -> 返回用户
    """
    db_sql = select(UserToken).where(UserToken.token == token)
    result = await db.execute(db_sql)
    db_user_token = result.scalar_one_or_none()
    # 验证usertoken表中的令牌是否存在且是否过期
    if db_user_token is None and db_user_token.expires_at < datetime.datetime.now():
        return None
    db_sql = select(User).where(User.id == db_user_token.user_id)
    result = await db.execute(db_sql)
    return result.scalar_one_or_none()

# 根据用户id查询用户信息
async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    db_sql = select(User).where(User.id == user_id)
    result = await db.execute(db_sql)
    return result.scalar_one_or_none()

# 更新用户信息
async def update_user(
        db: AsyncSession,
        user_id: int,
        user_data: UserUpdateRequest
):
    """
    根据用户id更新用户信息 -> 检查更新操作是否命中 -> 获取更新后的用户信息
    """
    db_sql = update(User).where(User.id == user_id).values(**user_data.model_dump(
        exclude_unset=True,     # 忽略未设置属性
        exclude_none=True       # 忽略值为None的属性
    ))
    # model_dump 是将任何对象转换为字典
    # model_validate 将任意数据转换为符合模型定义的对象

    result = await db.execute(db_sql)
    await db.commit()

    # 判断是否更新成功
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    
    # 获取更新后的用户信息
    update_user = await get_user_by_id(db, user_id)
    return update_user

# 更新用户密码
async def change_password(
        db: AsyncSession,
        user: User,
        old_password: str,
        new_password: str
):
    # 验证旧密码
    if not security.verify_password(old_password, user.password):
        return False
    
    # 更新成新密码的密文
    hash_new_password = security.hash_password(new_password)
    user.password = hash_new_password
    # add()方法是将对象纳入会话管理，已存在的对象会被标记为更新，新对象则标记为插入这样更准确
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True