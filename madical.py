import os
from bs4 import BeautifulSoup
import requests
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunConfig, function_tool
from dotenv import load_dotenv

load_dotenv()

provider = AsyncOpenAI(
    api_key="AIzaSyAjNb7kfJFv4Hots_CD2em1E_PQZJSuTGU",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)



# from agents import Agent, Tool, Runner
from pydantic import BaseModel, Field
from typing import List, Dict

# Define data models for tool inputs/outputs

# Define a function to execute Python code (for demonstration purposes, keep it simple and safe!)
def execute_python(code: str) -> str:
    """Executes a Python code snippet and returns the output."""
    try:
        # Limited execution for safety - don't allow file access or network calls
        # In a real application, use a secure sandboxing environment
        local_vars: Dict = {}
        exec(code, globals(), local_vars)
        # Collect any printed output
        output = "\n".join([str(value) for key, value in local_vars.items() if not key.startswith("_")])
        return f"Code executed successfully. Output: {output}"
    except Exception as e:
        return f"Error executing code: {e}"

# Define the tool for executing Python code
@function_tool
def python_executor(code: str) -> str:
    """Executes a Python code snippet and returns the output."""
    return execute_python(code)

# Define the Code Assistant Agent
code_assistant_agent = Agent(
    name="CodeAssistant",
    instructions="You are a helpful coding assistant. You can answer questions about programming, provide code examples, and execute Python code snippets to test solutions. If asked to execute code, use the 'python_executor' tool. Be concise and focus on the user's coding needs.",
    tools=[python_executor]
)

# Example usage
runner = Runner()
result = runner.run_sync(code_assistant_agent, "Write a function in Python to calculate the factorial of a number and then execute it for the number 5.",run_config=run_config)

print(result.final_output)

