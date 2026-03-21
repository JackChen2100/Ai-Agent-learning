import os


class Config:
    def __init__(self):
        # 从系统环境变量获取 Key
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        # 模型名称
        self.model_name = os.getenv("QWEN_MODEL_NAME", "qwen-plus")

        # 快速失败：如果没有 Key，程序启动时立即报错
        if not self.api_key:
            raise ValueError("环境变量 DASHSCOPE_API_KEY 未设置，请检查系统设置。")


# 实例化，方便其他文件直接引用
settings = Config()