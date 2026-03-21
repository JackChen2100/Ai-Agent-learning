import asyncio
import os
from openai import AsyncOpenAI  # 导入官方库的异步客户端


# ==========================================
# 1. 核心方法：使用 OpenAI 库进行流式城市查询
# ==========================================
async def stream_query_city_food(client: AsyncOpenAI, city: str):
    """
    【机制演示】：
    - stream=True: 告诉服务器开启流式传输模式。
    - async for chunk in response: 调用 AsyncOpenAI 库，直接迭代返回的增量数据块（Chunks）。
    - delta.content: 提取每一帧里的增量文字内容。
    """
    prompt = f"请简述{city}最出名的三种美食是什么？并说明其特色。"

    print(f"\n\n🔍 正在为你连线 Qwen 大模型，查询【{city}】美食攻略...\n")
    print("-" * 40)

    # A. 【库调用点】：发起异步流式请求
    response = await client.chat.completions.create(
        model="qwen-plus",  # 或者用 "qwen-turbo"
        messages=[
            {"role" : "system", "content" : "你是一个旅游专家和旅游爱好者，回到问题要简洁一些，不要废话"},
            {"role": "user", "content": prompt}],
        stream=True  # 【机制关键】：开启流式
    )

    # B. 【机制点】：直接异步遍历响应对象
    # 官方库帮我们处理了底层的 SSE (Server-Sent Events) 协议解析，非常清爽
    async for chunk in response:
        # C. 【delta 实例】：从层层嵌套的结构中，提取最核心的增量内容
        # 注意：流式输出中，这里是 choices[0].delta.content，非流式是 choices[0].message.content
        delta_content = chunk.choices[0].delta.content

        if delta_content:
            # D. 【展现关键】：实时打印增量文字
            # - end="": 打印完不要换行，接在后面
            # - flush=True: 强制立刻把缓冲区的内容推送到终端显示
            print(delta_content, end="", flush=True)

    print("\n" + "-" * 40 + f"\n✅ 【{city}】美食攻略获取完成。")


# ==========================================
# 2. 异步入口主函数
# ==========================================
async def main():
    # 初始化客户端（Qwen 兼容 OpenAI 格式）
    client = AsyncOpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    # 我们要查询的城市列表（模拟你的研究数据）
    target_cities = ["广州", "西安", "成都"]

    # 按顺序流式查询（为了演示效果可读，不让终端乱掉）
    for city in target_cities:
        await stream_query_city_food(client, city)


# ==========================================
# 3. 程序启动器
# ==========================================
if __name__ == "__main__":
    # 启动 Python 事件循环
    asyncio.run(main())