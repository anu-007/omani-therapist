from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from core.config import MODEL_TEXT
from .prompts import mental_health_instruction
from .tools.translate import translate_to_english

# root agent
root_agent = LlmAgent(
    name = "omani_therapist",
    model = LiteLlm(model=MODEL_TEXT),
    description = "Given a user mental health query provide helpful guidance",
    instruction = mental_health_instruction,
    tools= [translate_to_english]
)