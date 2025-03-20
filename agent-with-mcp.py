import os

from mcp import StdioServerParameters
from smolagents import CodeAgent, GradioUI, HfApiModel, ToolCollection, tool

model = HfApiModel()

#dont forget to install mcp:  uv add "smolagents[mcp]"  
server_parameters = StdioServerParameters(
    command="uvx",
    args=["--quiet", "pubmedmcp@0.1.3"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

with ToolCollection.from_mcp(server_parameters) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], model=model, add_base_tools=True)
    agent.run("Please find a remedy for hangover. only use the pubmedmcp. ")