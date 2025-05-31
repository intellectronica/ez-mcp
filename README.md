# EZ-MCP: Simple Model Context Protocol Servers

The easiest path to getting an MCP server going! This repository contains complete, production-ready examples of MCP servers in both Python and TypeScript/Deno.

## 📁 What's Included

- **`ez-mcp.py`** - Python MCP server using the FastMCP framework
- **`ez-mcp.ts`** - TypeScript MCP server using Deno and the official MCP SDK

Both implementations are functionally equivalent and demonstrate:
- 📊 **Resources**: Server information endpoint
- 🛠️ **Tools**: Interactive greeting functionality  
- 📝 **Prompts**: Greeting template generation
- ⚙️ **Configuration**: Environment variable support

## 🚀 Quick Start

### Python Version (ez-mcp.py)

```bash
# Run directly with uv (recommended)
uv run ez-mcp.py

# Or with development mode
uv run mcp dev ez-mcp.py

# Or install in MCP Client
uv run mcp install ez-mcp.py
```

### TypeScript/Deno Version (ez-mcp.ts)

```bash
# Run directly with Deno (recommended)
deno run --allow-all ez-mcp.ts

# Or make executable and run
chmod +x ez-mcp.ts
./ez-mcp.ts

# Or with MCP Inspector for development
mcp dev deno run --allow-all ez-mcp.ts
```

## 🔧 MCP Client Configuration

Add either server to your `mcp.json`:

### Python Server
```json
{
  "mcpServers": {
    "ez-mcp-python": {
      "command": "uv",
      "args": ["run", "/path/to/ez-mcp.py"],
      "env": {
        "GREETING_PREFIX": "Hello"
      }
    }
  }
}
```

### TypeScript/Deno Server
```json
{
  "mcpServers": {
    "ez-mcp-typescript": {
      "command": "deno", 
      "args": ["run", "--allow-all", "/path/to/ez-mcp.ts"],
      "env": {
        "GREETING_PREFIX": "Hello"
      }
    }
  }
}
```

## 🎯 Features Demonstrated

| Feature | Python (ez-mcp.py) | TypeScript (ez-mcp.ts) |
|---------|-------------------|------------------------|
| Resources | ✅ Server info via `server://info` | ✅ Server info via `server://info` |
| Tools | ✅ `hello_someone` function | ✅ `hello-someone` function |
| Prompts | ✅ `greeting_prompt` template | ✅ `greeting-prompt` template |
| Environment Variables | ✅ `GREETING_PREFIX` support | ✅ `GREETING_PREFIX` support |
| Error Handling | ✅ Input validation | ✅ Input validation |
| Type Safety | ✅ Pydantic schemas | ✅ Zod schemas |

## 📚 Learn More

- **Python FastMCP**: Check the comments in `ez-mcp.py` for extensive documentation
- **TypeScript SDK**: Check the comments in `ez-mcp.ts` for comprehensive examples
- **MCP Specification**: https://modelcontextprotocol.io/
- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk  
- **TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk

## 🛠️ Extending the Servers

Both servers are designed to be easily extended. See the comprehensive inline documentation in each file for examples of:

- Adding new tools and resources
- Database integration
- External API integration  
- Error handling patterns
- Environment configuration
- And much more!

## 📜 License

MIT License - see LICENSE file for details.
