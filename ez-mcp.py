#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "mcp>=1.9.0",
# ]
# ///

"""
EZ-MCP: A Simple, Complete MCP Server Example

This is a comprehensive example of a Model Context Protocol (MCP) server implemented
using the Anthropic MCP Python SDK. It demonstrates all major MCP functionality:

1. **Resources**: Static and dynamic data sources that provide context to LLMs
2. **Tools**: Functions that LLMs can call to perform actions or computations
3. **Prompts**: Reusable templates for LLM interactions
4. **Server Management**: Proper lifecycle handling and configuration

## How to Run This Server

### Option 1: Direct execution with uv (Recommended)
```bash
uv run ez-mcp.py
```

### Option 2: Development mode with MCP Inspector
```bash
uv run mcp dev ez-mcp.py
```

### Option 3: Install in Claude Desktop
```bash
uv run mcp install ez-mcp.py
```

## Claude Desktop Configuration

To use this server with Claude Desktop, add this configuration to your
`claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "ez-mcp": {
      "command": "uv",
      "args": ["run", "/path/to/ez-mcp.py"],
      "env": {
        "GREETING_PREFIX": "Hello"
      }
    }
  }
}
```

Replace `/path/to/ez-mcp.py` with the actual path to this file.

## How to Modify and Enhance This Server

This server is designed to be easily extensible. Here are common modifications:

### Adding New Tools
```python
@mcp.tool()
def my_new_tool(param1: str, param2: int) -> str:
    \"\"\"Description of what this tool does\"\"\"
    # Your implementation here
    return f"Result: {param1} x {param2}"
```

### Adding New Resources
```python
@mcp.resource("my-data://{category}")
def get_my_data(category: str) -> str:
    \"\"\"Dynamic resource based on category\"\"\"
    # Your implementation here
    return f"Data for {category}"
```

### Adding New Prompts
```python
@mcp.prompt()
def my_prompt_template(task: str) -> str:
    \"\"\"Custom prompt template\"\"\"
    return f"Please help me with: {task}\\n\\nProvide a detailed response."
```

### Adding Database Integration
```python
from contextlib import asynccontextmanager
import sqlite3

@asynccontextmanager
async def app_lifespan(server):
    # Initialize database connection
    db = sqlite3.connect("data.db")
    try:
        yield {"db": db}
    finally:
        db.close()

# Pass lifespan to server
mcp = FastMCP("Enhanced Server", lifespan=app_lifespan)
```

### Adding External API Integration
```python
import httpx

@mcp.tool()
async def fetch_external_data(url: str) -> str:
    \"\"\"Fetch data from external API\"\"\"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

### Environment Variables
Use environment variables for configuration:
```python
import os

API_KEY = os.getenv("API_KEY", "default-key")
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"
```

### Error Handling
Add proper error handling to your tools:
```python
@mcp.tool()
def safe_division(a: float, b: float) -> float:
    \"\"\"Safely divide two numbers\"\"\"
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### Adding Dependencies
To add new dependencies, modify the script metadata at the top:
```python
# dependencies = [
#   "mcp>=1.9.0",
#   "httpx",      # For HTTP requests
#   "pandas",     # For data manipulation
#   "pillow",     # For image processing
# ]
```

Then run `uv run ez-mcp.py` and uv will automatically install the new dependencies.

## Architecture Notes

- **FastMCP**: High-level server interface that handles protocol details
- **Decorators**: Use @mcp.tool(), @mcp.resource(), @mcp.prompt() to register functions
- **Type Hints**: Use proper type hints for better development experience
- **Async Support**: Tools and resources can be async functions for I/O operations
- **Context Access**: Use the Context parameter to access server capabilities

For more advanced use cases, see the MCP Python SDK documentation at:
https://github.com/modelcontextprotocol/python-sdk
"""

import os
import json
import datetime
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP


# Create the MCP server
mcp = FastMCP(
    name="EZ-MCP Demo Server",
    dependencies=["mcp>=1.9.0"]
)

# ================================================================================
# RESOURCE: Server information
# ================================================================================

@mcp.resource("server://info")
def get_server_info() -> str:
    """Get information about this MCP server"""
    info = {
        "name": "EZ-MCP Demo Server",
        "version": "1.0.0",
        "description": "A simple MCP server demonstrating basic functionality",
        "features": ["hello tool", "greeting prompt", "server info resource"],
        "author": "EZ-MCP",
        "status": "running"
    }
    return json.dumps(info, indent=2)


# ================================================================================
# TOOL: Hello someone
# ================================================================================

@mcp.tool()
def hello_someone(name: str) -> str:
    """Say hello to someone"""
    if not name.strip():
        return "Error: Please provide a name"
    
    name = name.strip()
    return f"Hello, {name}! Nice to meet you!"


# ================================================================================
# PROMPT: Simple greeting template
# ================================================================================

@mcp.prompt()
def greeting_prompt(person_name: str) -> str:
    """Generate a greeting prompt for someone"""
    return f"""Please create a warm and friendly greeting for {person_name}.

The greeting should be:
1. Warm and welcoming
2. Professional yet friendly
3. Appropriate for a first meeting
4. Memorable and personal

Make it genuine and engaging."""


# ================================================================================
# SERVER STARTUP
# ================================================================================

def main():
    """Main function to run the server"""
    print("🚀 Starting EZ-MCP Demo Server...")
    print("📖 Simple MCP server with:")
    print("   • 1 Resource: Server info")
    print("   • 1 Tool: Hello someone") 
    print("   • 1 Prompt: Greeting template")
    print("")
    print("🔧 Configuration:")
    print(f"   • Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"   • Greeting prefix: {os.getenv('GREETING_PREFIX', 'Welcome')}")
    print("")
    print("📡 Server running on stdio transport...")
    print("   Use 'uv run mcp dev ez-mcp.py' to open the MCP Inspector")
    print("   Or configure this server in Claude Desktop")
    print("")
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
