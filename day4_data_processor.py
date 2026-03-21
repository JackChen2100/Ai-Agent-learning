import os
import requests
import logging
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from functools import wraps
import time

# ==========================================
# 模块 1：配置与日志（Day 1-2 的积累）
# ==========================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("QwenAgent")


# ==========================================
# 模块 2：数据模型（Pydantic - 今天的核心）
# ==========================================
# Pydantic 就像一个“模具”，确保 LLM 返回的乱序 JSON 变成整齐的 Python 对象
class QwenMessage(BaseModel):
    role: str
    content: str


class QwenUsage(BaseModel):
    # Field(default=0) 保证即使 API 没返回这个字段，程序也不会崩，而是给个 0
    total_tokens: int = Field(default=0)


class QwenChoice(BaseModel):
    message: QwenMessage
    finish_reason: str


class QwenResponse(BaseModel):
    """这是最高层的模具，对应 API 返回的完整大 JSON"""
    id: str
    choices: List[QwenChoice]
    usage: QwenUsage


# ==========================================
# 模块 3：核心请求类（逻辑封装）
# ==========================================
class QwenRequester:
    def __init__(self):
        # 【修复 AttributeError】先获取 Key，再构造 Headers
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("系统环境变量 DASHSCOPE_API_KEY 未设置！")

        self.url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def call_api(self, prompt: str) -> dict:
        """
        负责发起网络请求。
        注意：这里返回的是 dict（字典），方便后续传给 Pydantic 校验。
        """
        # 【修复 NameError】在请求前必须先定义 payload
        payload = {
            "model": "qwen-plus",
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            # 【修复 Timeout】将超时增加到 30s，给 LLM 留足思考时间
            response = requests.post(
                self.url,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            # 状态码校验（401, 404 等在这里会被拦截）
            response.raise_for_status()

            # 【修复 TypeError】必须返回 .json()，这是一个字典。
            # 如果返回 .text，外部解包就会报 "must be a mapping, not str"
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"网络层错误: {e}")
            raise e


# ==========================================
# 模块 4：业务执行（数据流转）
# ==========================================
if __name__ == "__main__":
    # 1. 初始化工具人
    requester = QwenRequester()

    # 2. 尝试获取并解析数据
    try:
        user_prompt = "请用一个专业术语形容 Python 的动态特性。"

        # 获取原始字典 (dict)
        raw_data = requester.call_api(user_prompt)

        # 将字典塞进 Pydantic 模具进行校验和转换
        # **raw_data 代表将字典里的键值对“拆包”后传给模型
        response_obj = QwenResponse(**raw_data)

        # 3. 此时 response_obj 是一个对象，可以使用“点”操作符访问属性
        content = response_obj.choices[0].message.content
        tokens = response_obj.usage.total_tokens

        print("\n" + "=" * 30)
        print(f"【Qwen 回答】: {content}")
        print(f"【Token 消耗】: {tokens}")
        print("=" * 30)

    except ValidationError as ve:
        logger.error(f"数据校验失败，LLM 返回的格式不对: {ve.json()}")
    except Exception as final_e:
        logger.error(f"程序运行中断: {final_e}")