from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from core.config import MODEL_TEXT_PRIMARY
from ...prompts import primary_therapist_prompt
from agents.callbacks.after_agent import modify_output_after_agent

primary_therapist_agent = LlmAgent(
    model = LiteLlm(model=MODEL_TEXT_PRIMARY),
    name = "primary_therapist",
    description = "Given a user mental health query provide helpful guidance",
    instruction = primary_therapist_prompt,
    output_key = "primary_therapist_response",
    after_agent_callback = modify_output_after_agent
)