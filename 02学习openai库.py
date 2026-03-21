from httpx import stream
from openai import OpenAI


client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
responses = client.chat.completions.create(
    model = "qwen3-max",
    messages = [
        {"role":"system","content" :" 你是一个python编程专家,不要说废话，简单不要浪费token"},
        {"role":"assistant","content" :"好的，我是python编程专家。有什么可以帮到你的吗？"},
        {"role":"user","content" :"输出一个0到10的数字，用python代码写"}
    ]
)

print(responses.choices[0].message.content)