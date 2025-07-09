from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from ..core.config import MODEL_TEXT
from .prompts import dish_ordering_instruction

# root agent
root_agent = LlmAgent(
    name = "dish_ordering_agent",
    model = LiteLlm(model=MODEL_TEXT),
    description = "Given a restaurnat menu and optional preference extract ingredients and suggest dishes to order",
    instruction = dish_ordering_instruction
)