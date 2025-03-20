import os

from mcp import StdioServerParameters
from smolagents import CodeAgent, GradioUI, OpenAIServerModel, ToolCollection, tool

# Initialize Gemini model using OpenAIServerModel with OpenAI-compatible endpoint
model = OpenAIServerModel(
    model_id="gemini-2.0-flashlight",
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.environ["GEMINI_API_KEY"],
)

# Don't forget to install mcp: uv add "smolagents[mcp]"
server_parameters = StdioServerParameters(
    command="uvx",
    args=["--quiet", "pubmedmcp@0.1.3"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

with ToolCollection.from_mcp(server_parameters) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], model=model, add_base_tools=True)
    agent.run("Please find a remedy for hangover. only use the pubmedmcp. ")
