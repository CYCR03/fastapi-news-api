import json
from typing import Any

import redis.asyncio as redis
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_DB = os.getenv('REDIS_DB')

redis_client = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    password=REDIS_PASSWORD, 
    db=REDIS_DB,
    decode_responses=True       # 将返回的数据从字节流解码为字符串
    )

# 读取缓存：字符串
async def get_cache_str(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None

# 读取缓存：列表、字典
async def get_cache_json(key: str):
    try:
        data = await redis_client.get(key)
        if data is not None:
            return json.loads(data)     # 将字符串数据转换成字典（反序列化）
        return None
    except Exception as e:
        print(f"获取json缓存失败：{e}")
        return None
    
# 设置缓存
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        # 如果是字典或列表，则需要序列化成字符串再存
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)   # 序列化(ensure_ascii=False 保存中文)
        
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败：{e}")
        return False


