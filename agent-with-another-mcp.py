import os
from pathlib import Path

from dotenv import load_dotenv
from mcp import StdioServerParameters
from smolagents import CodeAgent, HfApiModel, ToolCollection

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
skrape_api_key = os.getenv("SKRAPE_API_KEY")

# Verify that the API key exists
if not skrape_api_key:
    raise ValueError("SKRAPE_API_KEY not found in .env file")

model = HfApiModel()

server_parameters = StdioServerParameters(
    command="node",
    args=["/home/hans/youtube-videos/first-agent/skrape-mcp/build/index.js"],
    env={"SKRAPE_API_KEY": skrape_api_key},
)

with ToolCollection.from_mcp(server_parameters) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], model=model, add_base_tools=True)
    agent.run("get me a markdown of this site: https://modelcontextprotocol.io/docs/tools/debugging")