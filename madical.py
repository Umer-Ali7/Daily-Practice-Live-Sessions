# import requests
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



# # from agents import Agent, Tool, Runner
# from pydantic import BaseModel, Field
# from typing import List, Dict

# # Define data models for tool inputs/outputs

# # Define a function to execute Python code (for demonstration purposes, keep it simple and safe!)
# def execute_python(code: str) -> str:
#     """Executes a Python code snippet and returns the output."""
#     try:
#         # Limited execution for safety - don't allow file access or network calls
#         # In a real application, use a secure sandboxing environment
#         local_vars: Dict = {}
#         exec(code, globals(), local_vars)
#         # Collect any printed output
#         output = "\n".join([str(value) for key, value in local_vars.items() if not key.startswith("_")])
#         return f"Code executed successfully. Output: {output}"
#     except Exception as e:
#         return f"Error executing code: {e}"

# # Define the tool for executing Python code
# @function_tool
# def python_executor(code: str) -> str:
#     """Executes a Python code snippet and returns the output."""
#     return execute_python(code)

# # Define the Code Assistant Agent
# code_assistant_agent = Agent(
#     name="CodeAssistant",
#     instructions="You are a helpful coding assistant. You can answer questions about programming, provide code examples, and execute Python code snippets to test solutions. If asked to execute code, use the 'python_executor' tool. Be concise and focus on the user's coding needs.",
#     tools=[python_executor]
# )

# # Example usage
# runner = Runner()
# result = runner.run_sync(code_assistant_agent, "Write a function in Python to calculate the factorial of a number and then execute it for the number 5.",run_config=run_config)

# print(result.final_output)


# from agents import Agent
# from agents import function_tool
from typing import List

# Define a function for diagnosing a patient
def diagnose_patient(symptoms: List[str]) -> str:
    """Diagnoses a patient based on their symptoms.

    Args:
        symptoms: A list of symptoms the patient is experiencing.

    Returns:
        A diagnosis based on the symptoms.
    """
    # Simulate a simple diagnosis logic
    if "fever" in symptoms and "cough" in symptoms:
        return "Possible influenza. Recommend rest and fluids."
    elif "headache" in symptoms and "fatigue" in symptoms:
        return "Possible dehydration or stress. Recommend hydration and rest."
    else:
        return "Symptoms are unclear. Further examination needed."

# Convert the function into a tool
diagnose_tool = function_tool(diagnose_patient)

# Create the Medical Agent
medical_agent = Agent(
    name="Medical Agent",
    instructions="You are a helpful medical assistant. Diagnose patients based on their symptoms.",
    tools=[diagnose_tool],
)

# Example usage (not runnable here, but demonstrates how it would be used)
from agents import Runner
runner = Runner()
result = runner.run_sync(medical_agent, "I have a headpain.",run_config=run_config)
print(result.final_output)