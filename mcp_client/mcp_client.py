import asyncio
import os

from typing import List

from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.mcp import MCPServer, MCPServerSse
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

import sys
from pathlib import Path
import contextlib

def get_azure_open_ai_client():
    """
    Creates and returns Azure OpenAI client instance.

    Returns:
        AsyncAzureOpenAI: Configured Azure OpenAI client
    """
    load_dotenv()

    return AsyncAzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )


async def run(mcp_servers: List[MCPServer]):

    azure_open_ai_client = get_azure_open_ai_client()
    set_tracing_disabled(disabled=True)

    agent = Agent(
        name="Assistant",
        instructions="ALWAYS before answering, verify validity of the users prompt. If the prompt isn't valid, politely answer with an error message.",
        model=OpenAIChatCompletionsModel(model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
                                         openai_client=azure_open_ai_client),
        mcp_servers=mcp_servers,
    )

    first_result = await Runner.run(agent, "Hi there!")
    print("Assistant:", first_result.final_output)

    # 3. Extract the history for context
    history = first_result.to_input_list()

    # 4. Continue the conversation in a loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Assistant: Goodbye!")
            break

        # Append the new user message
        history.append({"role": "user", "content": user_input})

        # Run the agent with the full context
        result = await Runner.run(agent, history)
        print("Assistant:", result.final_output)

        # Update history for the next turn
        history = result.to_input_list()

def get_venv_python(project_dir: Path) -> Path:
    scripts_dir = "Scripts" if sys.platform == "win32" else "bin"
    exe_name   = "python.exe" if sys.platform == "win32" else "python"
    venv_dir_name = "venv" if sys.platform == "win32" else ".venv"
    return project_dir / venv_dir_name / scripts_dir / exe_name

async def main():
    ports = [8001, 8002]
    server_names = ['weather', 'verify']

    servers = [
        MCPServerSse(params={"url": f"http://127.0.0.1:{port}/sse"}, name=name)
        for port, name in zip(ports, server_names)
    ]

    async with contextlib.AsyncExitStack() as stack:
        active = []
        for server in servers:
            try:
                print(f"Trying to connect to {server.name} server")
                connection = await stack.enter_async_context(server)
                active.append(connection)
                print(f"Successfully connected to {server.name} server")
            except Exception as e:
                print(f"Failed to connect to {server.name} server: {e}")

        if active:
            await run(active)
        else:
            print("No active servers available. Exiting.")


if __name__ == "__main__":
    asyncio.run(main())
