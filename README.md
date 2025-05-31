# [EZ-MCP](https://ai.intellectronica.net/ez-mcp): The Fastest Way to Build MCP Servers

**Get an MCP server running in under 2 minutes!** This repository contains complete, ready-to-run templates for single file self-contained MCP servers in both Python/uv and TypeScript/Deno.

## 🚀 Why EZ-MCP?

- **⚡ Instant Setup**: Copy, paste, run - no complex configuration needed
- **🎯 Production Ready**: Both templates use official Anthropic SDKs
- **📚 Comprehensive Examples**: Everything documented with working code
- **🔧 Easily Extensible**: Add your own tools, resources, and prompts in minutes
- **💡 Perfect for Experimentation**: The fastest way to test MCP ideas locally

## 📁 What You Get

Two functionally identical, battle-tested templates:

- **`ez-mcp.py`** - Python server using official MCP SDK with FastMCP
- **`ez-mcp.ts`** - TypeScript server using official MCP SDK with Deno

Each template demonstrates all core MCP features:
- 📊 **Resources**: Dynamic data sources for LLM context
- 🛠️ **Tools**: Functions LLMs can call to perform actions  
- 📝 **Prompts**: Reusable templates for LLM interactions
- ⚙️ **Configuration**: Environment variable support

## ⚡ Quick Test Drive

Want to see these servers in action? Pick your language and run:

### Python Version
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and run immediately
git clone <this-repo>
cd ez-mcp
uv run ez-mcp.py
```

### TypeScript Version  
```bash
# Install Deno (if not already installed)
curl -fsSL https://deno.land/install.sh | sh

# Clone and run immediately
git clone <this-repo>
cd ez-mcp
deno run --allow-all ez-mcp.ts
```

Both servers will start immediately and show you what's available!

## 🎯 Create Your Own Server (Copy & Customise in 5 Minutes)

The fastest way to build your own MCP server is to copy one of our templates and customise it. Both templates are functionally identical and production-ready - just pick your preferred language!

### For Python Developers:

1. **Copy the template**:
   ```bash
   curl -O https://raw.githubusercontent.com/your-repo/ez-mcp/main/ez-mcp.py
   # Or just copy the ez-mcp.py file contents from this repo
   ```

2. **Rename and customise**:
   ```bash
   cp ez-mcp.py my-awesome-server.py
   ```

3. **Edit the server details** (around line 160):
   ```python
   mcp = FastMCP(
       name="My Awesome Server",  # <- Change this to your server name
       dependencies=["mcp>=1.9.0"]
   )
   ```

4. **Add your own tools** (copy this pattern anywhere in the file):
   ```python
   @mcp.tool()
   def my_custom_tool(input_text: str) -> str:
       """Describe what your tool does"""
       # Your logic here
       return f"Processed: {input_text}"
   ```

5. **Run your server**:
   ```bash
   uv run my-awesome-server.py
   ```

### For TypeScript/JavaScript Developers:

1. **Copy the template**:
   ```bash
   curl -O https://raw.githubusercontent.com/your-repo/ez-mcp/main/ez-mcp.ts
   # Or just copy the ez-mcp.ts file contents from this repo
   ```

2. **Rename and customise**:
   ```bash
   cp ez-mcp.ts my-awesome-server.ts
   chmod +x my-awesome-server.ts
   ```

3. **Edit the server details** (around line 160):
   ```typescript
   const server = new McpServer({
     name: "My Awesome Server",  // <- Change this to your server name
     version: "1.0.0"
   });
   ```

4. **Add your own tools** (copy this pattern anywhere in the file):
   ```typescript
   server.tool(
     "my-custom-tool",
     { input_text: z.string() },
     async ({ input_text }) => ({
       content: [{ type: "text", text: `Processed: ${input_text}` }]
     })
   );
   ```

5. **Run your server**:
   ```bash
   deno run --allow-all my-awesome-server.ts
   ```

### 🎉 That's It! 

You now have a working MCP server! The templates include extensive inline documentation and examples for adding:
- **Database connections** (SQLite, PostgreSQL, etc.)
- **API integrations** (REST APIs, GraphQL, etc.)
- **File operations** (reading, writing, searching)
- **Web scraping** 
- **Environment variables** and configuration
- **Error handling** and validation

Just read through the template code - it's designed to teach you everything you need to know!

## � Connect to MCP Clients

Once your server is running, connect it to any MCP client:

### MCP Client Configuration

Add to your `mcp.json` file:

#### Python Server
```json
{
  "mcpServers": {
    "my-python-server": {
      "command": "uv",
      "args": ["run", "/absolute/path/to/your-server.py"],
      "env": {
        "MY_API_KEY": "your-key-here"
      }
    }
  }
}
```

#### TypeScript Server
```json
{
  "mcpServers": {
    "my-typescript-server": {
      "command": "deno", 
      "args": ["run", "--allow-all", "/absolute/path/to/your-server.ts"],
      "env": {
        "MY_API_KEY": "your-key-here"
      }
    }
  }
}
```

## 🛠️ Development and Testing

### Use MCP Inspector for Development

The MCP Inspector provides a web interface to test your server:

#### Python
```bash
# Install the inspector
pip install mcp

# Run with inspector
uv run mcp dev your-server.py
```

#### TypeScript
```bash
# Install the inspector
npm install -g @modelcontextprotocol/inspector

# Run with inspector  
npx @modelcontextprotocol/inspector deno run --allow-all your-server.ts
```

This opens a web interface where you can:
- 🔍 Browse available tools, resources, and prompts
- ▶️ Test tools with different parameters
- 📖 View resource contents
- 🧪 Experiment with prompts

### Adding Dependencies

#### Python
Edit the dependencies section at the top of your `.py` file:
```python
# dependencies = [
#   "mcp>=1.9.0",
#   "requests",     # For HTTP requests
#   "pandas",       # For data manipulation  
#   "sqlalchemy",   # For database access
# ]
```

#### TypeScript  
Simply import what you need - Deno handles the rest:
```typescript
import { parse } from "https://deno.land/std@0.224.0/csv/mod.ts";
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { DB } from "https://deno.land/x/sqlite@v3.8/mod.ts";
```

## 💡 Real-World Examples

### Quick File Search Tool
```python
# Python
@mcp.tool()
def search_files(pattern: str, directory: str = ".") -> str:
    """Search for files matching a pattern"""
    import glob
    import os
    matches = glob.glob(os.path.join(directory, f"**/*{pattern}*"), recursive=True)
    return f"Found {len(matches)} files: {matches[:10]}"  # Show first 10
```

```typescript
// TypeScript  
server.tool(
  "search-files",
  { pattern: z.string(), directory: z.string().default(".") },
  async ({ pattern, directory }) => {
    const matches = [];
    for await (const entry of Deno.readDir(directory)) {
      if (entry.name.includes(pattern)) {
        matches.push(entry.name);
      }
    }
    return {
      content: [{ type: "text", text: `Found files: ${matches.join(", ")}` }]
    };
  }
);
```

### Web Scraper Tool
```python
# Python (add "requests" to dependencies)
@mcp.tool()
async def scrape_url(url: str) -> str:
    """Scrape text content from a URL"""
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text[:1000]  # First 1000 chars
```

```typescript
// TypeScript
server.tool(
  "scrape-url", 
  { url: z.string() },
  async ({ url }) => {
    const response = await fetch(url);
    const text = await response.text();
    return {
      content: [{ type: "text", text: text.slice(0, 1000) }]
    };
  }
);
```

### Database Query Tool
```python
# Python (add "sqlite3" - built-in)
@mcp.tool()
def query_db(sql: str) -> str:
    """Execute a SQL query"""
    import sqlite3
    conn = sqlite3.connect("data.db")
    results = conn.execute(sql).fetchall()
    conn.close()
    return str(results)
```

```typescript
// TypeScript
import { DB } from "https://deno.land/x/sqlite@v3.8/mod.ts";

const db = new DB("data.db");

server.tool(
  "query-db",
  { sql: z.string() },
  async ({ sql }) => {
    const results = db.queryEntries(sql);
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }]
    };
  }
);
```

## 🏗️ Template Features Explained

Both templates include identical functionality to demonstrate all MCP capabilities:

### 📊 Resources (Data Sources)
- **`server://info`** - Dynamic server information
- Shows how to create data sources that LLMs can access
- Perfect for configuration, documentation, or live data

### 🛠️ Tools (LLM Functions)  
- **`hello_someone`** (Python) / **`hello-someone`** (TypeScript)
- Demonstrates parameter validation and environment variables
- Template for any function you want LLMs to call

### 📝 Prompts (Templates)
- **`greeting_prompt`** (Python) / **`greeting-prompt`** (TypeScript)  
- Shows how to create reusable prompt templates
- Perfect for complex instructions or workflows

### ⚙️ Configuration
- Environment variable support (`GREETING_PREFIX`)
- Error handling and input validation
- Production-ready logging and startup messages

## � Common Use Cases

**Perfect for:**
- 🧪 **Rapid Prototyping**: Test MCP ideas in minutes
- 🔧 **Personal Automation**: Quick scripts for daily tasks  
- 📊 **Data Access**: Connect LLMs to your databases/APIs
- 🌐 **Web Integration**: Scrape sites, call APIs, process data
- 📁 **File Operations**: Search, read, write, organise files
- 🔍 **Development Tools**: Code analysis, documentation, testing
- 💼 **Business Logic**: Custom workflows and integrations

## 📚 Learn More & Get Help

### Essential Resources
- 📖 **MCP Specification**: https://modelcontextprotocol.io/
- 🐍 **Python SDK Docs**: https://github.com/modelcontextprotocol/python-sdk  
- 📜 **TypeScript SDK Docs**: https://github.com/modelcontextprotocol/typescript-sdk
- � **MCP Community**: Join the discussions and get help

### Deep Dive Into the Code
Both template files contain **extensive inline documentation** with:
- Line-by-line explanations
- Advanced usage patterns  
- Integration examples (databases, APIs, file systems)
- Error handling best practices
- Performance optimisation tips
- Production deployment guidance

**Read the source code** - it's designed to teach you everything you need to know!

## 🤝 Contributing & Feedback

Found these templates helpful? Have ideas for improvements? We'd love to hear from you!

- 🐛 Report issues or suggest features
- 📝 Share your cool MCP server creations  
- 🔧 Submit improvements to the templates
- 📚 Help improve documentation

## 📜 License

MIT License - Use these templates however you want! See LICENSE file for details.

© Eleanor Berger — [ai.intellectronica.net](https://ai.intellectronica.net/)