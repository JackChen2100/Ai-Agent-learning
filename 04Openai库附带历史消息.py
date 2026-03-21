import sys

from openai import OpenAI

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
messages = [
        {"role":"system","content" :" 你是一个AI助理，回答很简洁"},
        {"role":"assistant","content" :"好的，我是Ai助理，我回答很简洁，有什么可以帮到你的吗？"},
        {"role":"user","content" :"小红养了2只猫"},
        {"role" :"assistant","content":"好的"},
        {"role":"user","content" :"小红还养了3只狗"},
        {"role" :"assistant","content":"好的"},
        {"role" : "user","content":"小红总共养了多少只宠物"}
    ]
response = client.chat.completions.create(
    model= "qwen3-max",
    messages = messages,
    stream = True
)
for x in response:
    print(x.choices[0].delta.content,end="",flush=True)