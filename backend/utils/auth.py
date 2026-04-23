from fastapi import HTTPException, Header, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from curd.users import get_user_by_token

# 整合根据请求头的token验证,对通过验证的token,查询用户信息
async def get_current_user(
        token: str | None = Header(None, alias="Authorization"), 
        db: AsyncSession = Depends(get_db)
):
    """
    获取请求头中的token -> 验证token -> 查询用户信息
    """
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌为空")
    
    user = await get_user_by_token(db, token)
    # 请求头的格式: Authorization: `${this.token}`
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效令牌或令牌已过期")
    
    return user
