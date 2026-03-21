import logging
import time
from functools import wraps

# 1. 配置标准日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)
logger = logging.getLogger("AgentLogger")

# 2. 异常重试装饰器
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @wraps(func)  # 保护原函数的元数据（如函数名）
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == retries - 1: # 最后一次尝试
                        logger.error(f"最终失败：{e}")
                        raise e
                    logger.warning(f"请求波动，正在进行第 {i+1} 次重试...")
                    time.sleep(delay)
        return wrapper
    return decorator