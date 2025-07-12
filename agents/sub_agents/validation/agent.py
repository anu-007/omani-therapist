from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from core.config import MODEL_TEXT_FALLBACK
from ...prompts import fallback_therapist_prompt
from agents.callbacks.after_agent import modify_output_after_agent

fallback_therapist_agent = LlmAgent(
    model = LiteLlm(model=MODEL_TEXT_FALLBACK),
    name = "fallback_therapist",
    description = "Given a response from primary therepist evaluate and validate response for any harmful advice or suggestions",
    instruction = fallback_therapist_prompt,
    output_key = "fallback_therapist_response",
    after_agent_callback = modify_output_after_agent
)