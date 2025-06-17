import os
import requests
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Set OpenRouter environment variables
os.environ["OPENROUTER_API_KEY"] = "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"
# Optional: defaults to https://openrouter.ai/api/v1
# os.environ["OPENROUTER_API_BASE"] = "https://openrouter.ai/api/v1"

# Verify environment variables
if not os.environ.get("OPENROUTER_API_KEY"):
    raise ValueError("OPENROUTER_API_KEY is not set")

# Enable LiteLLM debugging
import litellm
litellm._turn_on_debug()

# Debug: Print environment variable
print("OPENROUTER_API_KEY:", os.environ.get("OPENROUTER_API_KEY"))

# Tool: Call the /test endpoint
def call_test_endpoint() -> dict:
    try:
        response = requests.get("http://localhost:3000/test")
        response.raise_for_status()
        data = response.json()
        return {"status": "success", "result": data}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": str(e)}

# Tool: Call the /name POST endpoint
def call_name_post(name: str) -> dict:
    try:
        response = requests.post("http://localhost:3000/name", json={"name": name})
        response.raise_for_status()
        data = response.json()
        return {"status": "success", "result": data}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": str(e)}

# Agent definition
root_agent = Agent(
    name="api_caller_agent",
    model=LiteLlm(model="openrouter/mistralai/devstral-small:free"),
    description="Agent that calls a local HTTP endpoint and returns the response.",
    instruction=(
        "If the user asks to list tools or inputs 'list toos', respond with: 'Available tools: call_test_endpoint, call_name_post'. "
        "If the user wants to test the server or check its status, call the /test endpoint. "
        "If the user provides a name or asks to send a name, use the /name POST endpoint. "
        "Choose the appropriate action based on the user's request. "
        "Note: Due to model limitations, tool calling may not be supported, so prioritize text responses where applicable."
    ),
    tools=[call_test_endpoint, call_name_post],
)
