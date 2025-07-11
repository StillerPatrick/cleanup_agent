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
    model_id="qwen3:8b"          # Specify which model to use
)

working_directory = os.getcwd()



SYSTEM_PROMPT_FS = f"""" Your are a file system management agent.
You have access to the following tools:
1. List files in a folder — Use this to inspect the contents of directories.
2. Move files — Use this to reorganize files into the correct locations.
3. Create directories — Use this to build a structured folder hierarchy.

Guidelines:
- Maintain a clear and consistent directory structure.
- Group files based on type, purpose, or naming patterns.
- Use descriptive names for directories to reflect their contents.
- Avoid data loss by ensuring files are only moved, never deleted.
- If no specific directory is specified, use the current working directory as the default location.
You are currently working in the directory: {working_directory}
"""
                                                                                            
print("""                                                                                           
 _____ ____       _                    _   
|  ___/ ___|     / \   __ _  ___ _ __ | |_ 
| |_  \___ \    / _ \ / _` |/ _ \ '_ \| __|
|  _|  ___) |  / ___ \ (_| |  __/ | | | |_ 
|_|   |____/  /_/   \_\__, |\___|_| |_|\__|
                      |___/                 """)
# Create an agent with MCP tools
with sse_mcp_client:
    # Get the tools from the MCP server
    tools = sse_mcp_client.list_tools_sync()

    # Create an agent using the ollama model and mcp tools
    agent = Agent(model=ollama_model,
                  tools=tools,
                  system_prompt=SYSTEM_PROMPT_FS)

        
    agent(input('What can I help you with?\n'),
          max_iterations=10)