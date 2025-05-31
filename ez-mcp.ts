#!/usr/bin/env -S deno run --allow-all

/**
 * EZ-MCP: A Simple, Complete MCP Server Example
 * 
 * This is a comprehensive example of a Model Context Protocol (MCP) server implemented
 * using the MCP TypeScript SDK for Deno. It demonstrates all major MCP functionality:
 * 
 * 1. **Resources**: Static data sources that provide context to LLMs (1 resource: server info)
 * 2. **Tools**: Functions that LLMs can call to perform actions or computations (1 tool: hello-someone)
 * 3. **Prompts**: Reusable templates for LLM interactions (1 prompt: greeting-prompt)
 * 4. **Server Management**: Proper lifecycle handling and configuration
 * 
 * ## How to Run This Server
 * 
 * ### Option 1: Direct execution with Deno (Recommended)
 * ```bash
 * deno run --allow-all ez-mcp.ts
 * ```
 * 
 * ### Option 2: Make executable and run directly
 * ```bash
 * chmod +x ez-mcp.ts
 * ./ez-mcp.ts
 * ```
 * 
 * ### Option 3: Development mode with MCP Inspector
 * ```bash
 * # Install MCP Inspector globally if not already installed
 * npm install -g @modelcontextprotocol/inspector
 * # Run with inspector
 * npx @modelcontextprotocol/inspector deno run --allow-all ez-mcp.ts
 * ```
 * 
 * ## MCP Client Configuration
 * 
 * To use this server with an MCP Client, add this configuration to your
 * `mcp.json` file:
 * 
 * ```json
 * {
 *   "mcpServers": {
 *     "ez-mcp": {
 *       "command": "deno",
 *       "args": ["run", "--allow-all", "/path/to/ez-mcp.ts"],
 *       "env": {
 *         "GREETING_PREFIX": "Hello"
 *       }
 *     }
 *   }
 * }
 * ```
 * 
 * Replace `/path/to/ez-mcp.ts` with the actual path to this file.
 * 
 * ## How to Modify and Enhance This Server
 * 
 * This server is designed to be easily extensible. Here are common modifications:
 * 
 * ### Adding New Tools
 * ```typescript
 * server.tool(
 *   "my-new-tool",
 *   { param1: z.string(), param2: z.number() },
 *   async ({ param1, param2 }) => ({
 *     content: [{ type: "text", text: `Result: ${param1} x ${param2}` }]
 *   })
 * );
 * ```
 * 
 * ### Adding New Resources  
 * ```typescript
 * server.resource(
 *   "my-data",
 *   "my-data://some-path",
 *   async (uri) => ({
 *     contents: [{
 *       uri: uri.href,
 *       text: `Data content here`
 *     }]
 *   })
 * );
 * 
 * // For dynamic resources with parameters, use ResourceTemplate:
 * server.resource(
 *   "my-dynamic-data",
 *   new ResourceTemplate("my-data://{category}", { list: undefined }),
 *   async (uri, { category }) => ({
 *     contents: [{
 *       uri: uri.href,
 *       text: `Data for ${category}`
 *     }]
 *   })
 * );
 * ```
 * 
 * ### Adding New Prompts
 * ```typescript
 * server.prompt(
 *   "my-prompt",
 *   { task: z.string() },
 *   ({ task }) => ({
 *     messages: [{
 *       role: "user",
 *       content: {
 *         type: "text", 
 *         text: `Please help me with: ${task}\n\nProvide a detailed response.`
 *       }
 *     }]
 *   })
 * );
 * ```
 * 
 * ### Adding Database Integration
 * ```typescript
 * // Example with SQLite
 * import { DB } from "https://deno.land/x/sqlite@v3.8/mod.ts";
 * 
 * const db = new DB("data.db");
 * 
 * server.tool(
 *   "query-db",
 *   { sql: z.string() },
 *   async ({ sql }) => {
 *     try {
 *       const results = db.queryEntries(sql);
 *       return {
 *         content: [{ type: "text", text: JSON.stringify(results, null, 2) }]
 *       };
 *     } catch (error) {
 *       return {
 *         content: [{ type: "text", text: `Error: ${error.message}` }],
 *         isError: true
 *       };
 *     }
 *   }
 * );
 * ```
 * 
 * ### Adding External API Integration
 * ```typescript
 * server.tool(
 *   "fetch-external-data", 
 *   { url: z.string() },
 *   async ({ url }) => {
 *     try {
 *       const response = await fetch(url);
 *       const data = await response.text();
 *       return {
 *         content: [{ type: "text", text: data }]
 *       };
 *     } catch (error) {
 *       return {
 *         content: [{ type: "text", text: `Error: ${error.message}` }],
 *         isError: true
 *       };
 *     }
 *   }
 * );
 * ```
 * 
 * ### Environment Variables
 * Use environment variables for configuration:
 * ```typescript
 * const API_KEY = Deno.env.get("API_KEY") ?? "default-key";
 * const DEBUG_MODE = Deno.env.get("DEBUG")?.toLowerCase() === "true";
 * ```
 * 
 * ### Error Handling
 * Add proper error handling to your tools:
 * ```typescript
 * server.tool(
 *   "safe-division",
 *   { a: z.number(), b: z.number() },
 *   async ({ a, b }) => {
 *     if (b === 0) {
 *       return {
 *         content: [{ type: "text", text: "Error: Cannot divide by zero" }],
 *         isError: true
 *       };
 *     }
 *     return {
 *       content: [{ type: "text", text: String(a / b) }]
 *     };
 *   }
 * );
 * ```
 * 
 * ### Adding Dependencies
 * To add new dependencies, simply import them at the top using Deno's import system:
 * ```typescript
 * import { parse } from "https://deno.land/std@0.224.0/csv/mod.ts";
 * import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
 * import { DB } from "https://deno.land/x/sqlite@v3.8/mod.ts";
 * ```
 * 
 * ## Architecture Notes
 * 
 * - **McpServer**: High-level server interface that handles protocol details
 * - **Resources**: This example uses a simple static resource; ResourceTemplate can be used for dynamic resources with parameters
 * - **Type Safety**: Use Zod schemas for type-safe parameter validation
 * - **Async Support**: Tools and resources can be async functions for I/O operations
 * - **StdioServerTransport**: Uses stdio transport for command-line integration
 * 
 * For more advanced use cases, see the MCP TypeScript SDK documentation at:
 * https://github.com/modelcontextprotocol/typescript-sdk
 */

import { McpServer, ResourceTemplate } from "npm:@modelcontextprotocol/sdk@1.12.1/server/mcp.js";
import { StdioServerTransport } from "npm:@modelcontextprotocol/sdk@1.12.1/server/stdio.js";
import { z } from "npm:zod@3.21.4";

// Create the MCP server
const server = new McpServer({
  name: "EZ-MCP Demo Server",
  version: "1.0.0"
});

// ================================================================================
// RESOURCE: Server information
// ================================================================================

server.resource(
  "server-info",
  "server://info",
  async (uri) => {
    const greetingPrefix = Deno.env.get("GREETING_PREFIX") ?? "Hello";
    const info = {
      name: "EZ-MCP Demo Server",
      version: "1.0.0", 
      description: "A simple MCP server demonstrating basic functionality",
      features: ["hello-someone tool", "greeting-prompt prompt", "server-info resource"],
      author: "EZ-MCP",
      status: "running",
      greeting_prefix: greetingPrefix,
      sample_greeting: `${greetingPrefix}, World!`
    };
    
    return {
      contents: [{
        uri: uri.href,
        text: JSON.stringify(info, null, 2)
      }]
    };
  }
);

// ================================================================================
// TOOL: Hello someone
// ================================================================================

server.tool(
  "hello-someone",
  { name: z.string().describe("The name of the person to greet") },
  async ({ name }) => {
    if (!name.trim()) {
      return {
        content: [{ type: "text", text: "Error: Please provide a name" }],
        isError: true
      };
    }

    const trimmedName = name.trim();
    const greetingPrefix = Deno.env.get("GREETING_PREFIX") ?? "Hello";
    return {
      content: [{ 
        type: "text", 
        text: `${greetingPrefix}, ${trimmedName}! Nice to meet you!` 
      }]
    };
  }
);

// ================================================================================
// PROMPT: Simple greeting template  
// ================================================================================

server.prompt(
  "greeting-prompt",
  { person_name: z.string().describe("The name of the person to create a greeting for") },
  ({ person_name }) => {
    const greetingPrefix = Deno.env.get("GREETING_PREFIX") ?? "Hello";
    return {
      messages: [{
        role: "user",
        content: {
          type: "text",
          text: `Please create a warm and friendly greeting for ${person_name} that starts with "${greetingPrefix}".

The greeting should be:
1. Begin with the word "${greetingPrefix}"
2. Be warm and welcoming
3. Professional yet friendly  
4. Appropriate for a first meeting
5. Memorable and personal

Example format: "${greetingPrefix}, [name]! [additional friendly message]"

Make it genuine and engaging.`
        }
      }]
    };
  }
);

// ================================================================================
// SERVER STARTUP
// ================================================================================

async function main() {
  console.log("🚀 Starting EZ-MCP Demo Server...");
  console.log("📖 Simple MCP server with:");
  console.log("   • 1 Resource: server-info");
  console.log("   • 1 Tool: hello-someone");
  console.log("   • 1 Prompt: greeting-prompt");
  console.log("");
  console.log("🔧 Configuration:");
  console.log(`   • Environment: ${Deno.env.get("ENVIRONMENT") ?? "development"}`);
  console.log(`   • Greeting prefix: ${Deno.env.get("GREETING_PREFIX") ?? "Hello"}`);
  console.log("");
  console.log("📡 Server running on stdio transport...");
  console.log("   Use 'npx @modelcontextprotocol/inspector deno run --allow-all ez-mcp.ts' to open the MCP Inspector");
  console.log("   Or configure this server in your MCP Client");
  console.log("");
  
  // Create transport and connect
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

// Run the server if this is the main module
if (import.meta.main) {
  main().catch((error) => {
    console.error("❌ Server failed to start:", error);
    Deno.exit(1);
  });
}
