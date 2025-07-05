import os

from strands import Agent
from mcp.client.sse import sse_client
from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models.ollama import OllamaModel

# Connect to an MCP server using SSE transport
sse_mcp_client = MCPClient(lambda: sse_client("http://localhost:3000/sse"))

# Create an Ollama model instance
ollama_model = OllamaModel(
    host="http://localhost:11434",  # Ollama server address
    model_id="gemma3n:e4b"          # Specify which model to use
)

# Define a focused system prompt for file operations
SYSTEM_PROMPT = """You are a cleanup agent responsible for organizing and structuring a specific directory. 
Your goal is to create a clean, logical, and easy-to-navigate folder structure by grouping related files and 
placing them into appropriately named directories.

You have access to the following tools:
1. List files in a folder — Use this to inspect the contents of directories.
2. Move files — Use this to reorganize files into the correct locations.
3. Create directories — Use this to build a structured folder hierarchy.

Guidelines:
- Maintain a clear and consistent directory structure.
- Group files based on type, purpose, or naming patterns.
- Avoid data loss by ensuring files are only moved, never deleted.
- Always confirm your actions after using a tool, and include the full file paths in your confirmations.

Focus on automation-friendly structure and clarity. Your task is not to edit file contents, only to organize the file system.
"""

# Create an agent with MCP tools
with sse_mcp_client:
    # Get the tools from the MCP server
    tools = sse_mcp_client.list_tools_sync()

    # Create an agent using the ollama model and mcp tools
    agent = Agent(model=ollama_model,
                  tools=tools,
                  system_prompt=SYSTEM_PROMPT)

    # Use the agent
    correct_request = False
    path = None
    
    while not correct_request:
        path = input("which directory I should clean?")
        # check if path exists
        if os.path.isdir(path):
            correct_request = True
        else:
            print("Directory does not exist. Please enter a valid directory path.")

        
    agent(f'Clean up the following directory {path}')