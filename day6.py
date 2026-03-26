import os
import dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import Tool

@tool
def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b
tools = [add]
client = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen3-max",
    temperature=0.7
).bind_tools(tools)
messages = [
    SystemMessage(content="You are a helpful assistant that can add two numbers"),
    HumanMessage(content="What is 1 + 1?")
]
for _ in range(5):
    ai_msg = client.invoke(messages)
    messages.append(ai_msg)
    tool_calls = getattr(ai_msg, "tool_calls", [])
    if not tool_calls:
        break
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]
        result = next(tool for tool in tools if tool.name == tool_name)
        messages.append(ToolMessage(content=result.invoke(tool_args), tool_call_id=tool_id))
print(ai_msg.content)