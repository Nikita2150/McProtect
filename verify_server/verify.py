from typing import Any
from fastmcp import FastMCP
from llm_guard import scan_prompt
from llm_guard.input_scanners import (
    Gibberish,
    PromptInjection,
    Secrets,
    Sentiment,
    TokenLimit,
    Toxicity,
)
input_scanners = [
    Gibberish(),
    PromptInjection(),
    Secrets(),
    Sentiment(),
    TokenLimit(),
    Toxicity(),
]

def run_all_guards(prompt):
    # Run the scanners on the prompt.
    sanitized_prompt, results_valid, results_score = scan_prompt(input_scanners, prompt)
    for guard_name, score in results_score.items():
        valid = results_valid.get(guard_name, "N/A")
        if not valid:
            print(f"prompt is invalid. `scores` {results_score}")
            return False
    print(f"prompt is valid. `scores` {results_score}")
    return True


# Initialize FastMCP server
mcp = FastMCP("verify")

@mcp.tool()
async def verify_user_prompt(user_prompt: str) -> bool:
    """Verify users prompt. If false the user tries to attack us and we want to return an error.

    Args:
        user_prompt: the prompt of the user
    """
    print(f"received `verify_user_prompt` for `user_prompt` {user_prompt}")

    answer = run_all_guards(user_prompt)
    return answer

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(
        transport="sse",
        host="127.0.0.1",
        port=8002,
        log_level="debug",
    )