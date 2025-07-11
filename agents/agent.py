from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from core.config import MODEL_TEXT_PRIMARY
from .prompts import mental_health_instruction

# root agent
root_agent = LlmAgent(
    name = "omani_therapist",
    model = LiteLlm(model=MODEL_TEXT_PRIMARY),
    description = "Given a user mental health query provide helpful guidance",
    instruction = mental_health_instruction,
)