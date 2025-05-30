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

# Sample data for demonstrations
SAMPLE_DATA = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "user"},
    ],
    "products": [
        {"id": 101, "name": "Widget A", "price": 19.99, "category": "tools"},
        {"id": 102, "name": "Gadget B", "price": 29.99, "category": "electronics"},
        {"id": 103, "name": "Tool C", "price": 39.99, "category": "tools"},
    ],
    "orders": [
        {"id": 1001, "user_id": 1, "product_id": 101, "quantity": 2, "status": "shipped"},
        {"id": 1002, "user_id": 2, "product_id": 102, "quantity": 1, "status": "pending"},
    ]
}


# ================================================================================
# RESOURCES: Provide data/context to LLMs
# ================================================================================

@mcp.resource("config://app")
def get_app_config() -> str:
    """Get application configuration information"""
    config = {
        "app_name": "EZ-MCP Demo",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "greeting_prefix": os.getenv("GREETING_PREFIX", "Welcome"),
        "debug_mode": os.getenv("DEBUG", "false").lower() == "true"
    }
    return json.dumps(config, indent=2)


@mcp.resource("data://users")
def get_all_users() -> str:
    """Get all user data"""
    return json.dumps(SAMPLE_DATA["users"], indent=2)


@mcp.resource("data://products") 
def get_all_products() -> str:
    """Get all product data"""
    return json.dumps(SAMPLE_DATA["products"], indent=2)


@mcp.resource("data://orders")
def get_all_orders() -> str:
    """Get all order data"""
    return json.dumps(SAMPLE_DATA["orders"], indent=2)


@mcp.resource("user://{user_id}")
def get_user_by_id(user_id: str) -> str:
    """Get specific user data by ID"""
    try:
        uid = int(user_id)
        user = next((u for u in SAMPLE_DATA["users"] if u["id"] == uid), None)
        if user:
            return json.dumps(user, indent=2)
        else:
            return f"User with ID {user_id} not found"
    except ValueError:
        return f"Invalid user ID: {user_id}"


@mcp.resource("stats://summary")
def get_data_summary() -> str:
    """Get summary statistics of the data"""
    stats = {
        "total_users": len(SAMPLE_DATA["users"]),
        "total_products": len(SAMPLE_DATA["products"]),
        "total_orders": len(SAMPLE_DATA["orders"]),
        "categories": list(set(p["category"] for p in SAMPLE_DATA["products"])),
        "order_statuses": list(set(o["status"] for o in SAMPLE_DATA["orders"])),
        "generated_at": datetime.datetime.now().isoformat()
    }
    return json.dumps(stats, indent=2)


# ================================================================================
# TOOLS: Allow LLMs to perform actions and computations
# ================================================================================

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """Calculate Body Mass Index given weight in kg and height in meters"""
    if height_m <= 0:
        return "Error: Height must be greater than 0"
    if weight_kg <= 0:
        return "Error: Weight must be greater than 0"
    
    bmi = weight_kg / (height_m ** 2)
    
    # Determine BMI category
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return f"BMI: {bmi:.2f} ({category})"


@mcp.tool()
def generate_password(length: int = 12, include_symbols: bool = True) -> str:
    """Generate a secure random password"""
    import random
    import string
    
    if length < 4:
        return "Error: Password length must be at least 4 characters"
    if length > 128:
        return "Error: Password length must be no more than 128 characters"
    
    # Character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if include_symbols else ""
    
    # Ensure password contains at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits)
    ]
    
    if include_symbols:
        password.append(random.choice(symbols))
    
    # Fill remaining length with random characters
    all_chars = lowercase + uppercase + digits + symbols
    for _ in range(length - len(password)):
        password.append(random.choice(all_chars))
    
    # Shuffle the password
    random.shuffle(password)
    
    return "".join(password)


@mcp.tool()
def search_data(table: str, field: str, value: str) -> str:
    """Search for records in the sample data"""
    if table not in SAMPLE_DATA:
        return f"Error: Table '{table}' not found. Available tables: {list(SAMPLE_DATA.keys())}"
    
    data = SAMPLE_DATA[table]
    results = []
    
    for record in data:
        if field in record:
            if str(record[field]).lower() == value.lower():
                results.append(record)
    
    if results:
        return json.dumps(results, indent=2)
    else:
        return f"No records found in '{table}' where '{field}' equals '{value}'"


@mcp.tool()
def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a number as currency"""
    currency_symbols = {
        "USD": "$",
        "EUR": "€", 
        "GBP": "£",
        "JPY": "¥",
        "CAD": "C$",
        "AUD": "A$"
    }
    
    symbol = currency_symbols.get(currency.upper(), currency.upper())
    
    # Format with comma separators and 2 decimal places
    formatted = f"{symbol}{amount:,.2f}"
    
    return formatted


@mcp.tool()
def count_words(text: str) -> str:
    """Count words, characters, and other text statistics"""
    if not text:
        return "Error: No text provided"
    
    words = text.split()
    chars = len(text)
    chars_no_spaces = len(text.replace(" ", ""))
    sentences = len([s for s in text.split(".") if s.strip()])
    paragraphs = len([p for p in text.split("\n\n") if p.strip()])
    
    stats = {
        "words": len(words),
        "characters": chars,
        "characters_no_spaces": chars_no_spaces,
        "sentences": sentences,
        "paragraphs": paragraphs,
        "average_word_length": round(chars_no_spaces / len(words), 2) if words else 0
    }
    
    return json.dumps(stats, indent=2)


@mcp.tool()
def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    
    valid_units = ["C", "F", "K", "CELSIUS", "FAHRENHEIT", "KELVIN"]
    
    if from_unit not in valid_units or to_unit not in valid_units:
        return f"Error: Invalid units. Use C/Celsius, F/Fahrenheit, or K/Kelvin"
    
    # Normalize unit names
    from_unit = from_unit[0] if len(from_unit) > 1 else from_unit
    to_unit = to_unit[0] if len(to_unit) > 1 else to_unit
    
    # Convert to Celsius first
    if from_unit == "F":
        celsius = (value - 32) * 5/9
    elif from_unit == "K":
        celsius = value - 273.15
    else:  # C
        celsius = value
    
    # Convert from Celsius to target
    if to_unit == "F":
        result = celsius * 9/5 + 32
        unit_name = "Fahrenheit"
    elif to_unit == "K":
        result = celsius + 273.15
        unit_name = "Kelvin"
    else:  # C
        result = celsius
        unit_name = "Celsius"
    
    return f"{value}° {from_unit} = {result:.2f}° {unit_name}"


# ================================================================================
# PROMPTS: Reusable templates for LLM interactions
# ================================================================================

@mcp.prompt()
def code_review_prompt(code: str, language: str = "python") -> str:
    """Generate a prompt for code review"""
    return f"""Please review the following {language} code and provide feedback on:

1. Code quality and readability
2. Potential bugs or issues
3. Performance considerations
4. Best practices and improvements
5. Security concerns (if applicable)

Code to review:
```{language}
{code}
```

Please provide specific, actionable feedback with examples where appropriate."""


@mcp.prompt()
def data_analysis_prompt(dataset_description: str, question: str) -> str:
    """Generate a prompt for data analysis tasks"""
    return f"""I need help analyzing a dataset with the following characteristics:

Dataset: {dataset_description}

Analysis Question: {question}

Please help me:
1. Understand what data I need to examine
2. Suggest appropriate analysis methods
3. Identify potential insights or patterns to look for
4. Recommend visualizations that would be helpful
5. Point out any limitations or assumptions to consider

Please provide a step-by-step approach to answering this question."""


@mcp.prompt()
def debug_help_prompt(error_message: str, context: str = "") -> str:
    """Generate a prompt for debugging assistance"""
    prompt = f"""I'm encountering an error and need help debugging it.

Error Message:
{error_message}
"""
    
    if context:
        prompt += f"""
Context/Additional Information:
{context}
"""
    
    prompt += """
Please help me:
1. Understand what this error means
2. Identify the most likely causes
3. Suggest step-by-step debugging approaches
4. Provide potential solutions
5. Recommend how to prevent this error in the future

Please be specific and include examples where helpful."""
    
    return prompt


@mcp.prompt()
def explain_concept_prompt(concept: str, audience: str = "general") -> str:
    """Generate a prompt for explaining complex concepts"""
    return f"""Please explain the concept of "{concept}" for a {audience} audience.

Structure your explanation to include:
1. A simple, clear definition
2. Why this concept is important or useful
3. Key components or parts (if applicable)
4. Real-world examples or analogies
5. Common misconceptions to avoid
6. Related concepts or next steps for learning

Make the explanation accessible and engaging, using examples that the audience can relate to."""


@mcp.prompt()
def creative_writing_prompt(theme: str, style: str = "narrative", length: str = "short") -> str:
    """Generate a creative writing prompt"""
    return f"""Create a {length} {style} piece based on the theme: "{theme}"

Guidelines:
- Theme: {theme}
- Style: {style}
- Length: {length}

Consider incorporating:
1. Vivid sensory details
2. Character development (if applicable)
3. A clear beginning, middle, and end
4. Emotional resonance
5. Unique perspective or fresh take on the theme

Let your creativity flow while staying true to the theme and style requested."""


# ================================================================================
# SERVER STARTUP
# ================================================================================

def main():
    """Main function to run the server"""
    print("🚀 Starting EZ-MCP Demo Server...")
    print("📖 This server demonstrates all major MCP functionality:")
    print("   • Resources: Static and dynamic data sources")
    print("   • Tools: Functions for calculations and data processing") 
    print("   • Prompts: Templates for LLM interactions")
    print("")
    print("🔧 Configuration:")
    print(f"   • Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"   • Debug mode: {os.getenv('DEBUG', 'false')}")
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
