from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# 全局成功响应处理函数
def success_response(message: str = "操作成功", data = None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    # 返回JSON格式数据
    # jsonable_encoder()函数将Python对象转换为JSON兼容对象（这里转换的是data中的pydentic对象）
    # JSONResponse()函数将JSON兼容对象转换为响应对象    
    return JSONResponse(content=jsonable_encoder(content))