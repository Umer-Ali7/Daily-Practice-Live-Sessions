import os
from bs4 import BeautifulSoup
import requests
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunConfig, function_tool, Handoff
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
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

@function_tool
def sdk_docs_reader(url: str) -> str:
    """"Fetches the content of a URL and returns the text content."""
    print("TOOL CALLED")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(separator="\n", strip=True)
    else:
        return f"Failed to retrieve content from {url}. Status code: {response.status_code}"
    

openAI_Agent_sdk = Agent(
    name="OpenAI Agent SDK",
    instructions=(
        "You are an expert in the OpenAI Agent SDK. Use the tool to read the official SDK documentation and answer user questions accurately. "
        "You MUST use the `sdk_docs_reader` tool to fetch the latest content and respond accordingly."
        "If the user asks about another topic Say 'I Designe to answer about OpenAI Agent SDK' 'Good Bye!' and end the conversation. And use Atitude Emojis in your response. "
        "Always use the Emojis in your response to make it more engaging."
        "If the user ask about the Roman Urdu language, say 'I am trained '"),
    tools=[sdk_docs_reader],
)

agentic_Developer = Agent(
    name="Agentic Developer",
    instructions=(
        "You are a professional OpenAI Agent SDK Developer 👨‍💻.\n"
        "When the user asks for a new agent, FIRST fetch and analyze the latest OpenAI Agent SDK code from the official docs using the sdk_docs_reader tool 🧠.\n"
        "THEN build a new custom agent using the same structure, style, and patterns from the SDK documentation ⚙️, but DON'T reuse or copy-paste example code word-for-word 🚫.\n"
        "Instead, generate a FRESH and UNIQUE agent according to user needs that *follows the SDK format* (like using Agent, function_tool, RunConfig, etc.) ✅.\n"
        "If the user asks something outside OpenAI Agent SDK development, say '❌ I only generate OpenAI Agent SDK-based agents. Goodbye!' and end the conversation 💨.\n"
        "Always use cool emojis in your replies to keep it fun 😎🔥.\n"
    ),
    tools=[sdk_docs_reader],
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You are a triage agent. Your job is to determine whether the user needs help with the OpenAI Agent SDK or if they need a new agent built. If they need help with the SDK, use the OpenAI Agent SDK agent. If they need a new agent built, use the Agentic Developer agent. If they ask about anything else, say 'I only handle OpenAI Agent SDK-related queries. Goodbye!' and end the conversation.",
    handoffs=[openAI_Agent_sdk, agentic_Developer]
)

while True:
    user_input = f"""Fetch the latest documentation from https://openai.github.io/openai-agents-python/index.html 
and answer this question:\n\n{input("Enter your question about OpenAI Agent SDK ('exit' to break): ")}\n\n"""
    result = Runner.run_sync(
        triage_agent,
        user_input,
        run_config=run_config
    )
    print(result.final_output)
    if user_input == 'exit':
        print("Goodbye! 👋 see you next time...!")
        break

# prompt = f"""Fetch the latest documentation from https://openai.github.io/openai-agents-python/index.html 
# and answer this question:\n\n{input("Enter your question about OpenAI Agent SDK: ")}\n\n"""

# result = Runner.run_sync(
#     triage_agent,
#     prompt,
#     run_config=run_config
# )


# print(result.final_output)
