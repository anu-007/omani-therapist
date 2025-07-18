from google.genai import types
from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from helpers.crisis import detect_crisis
from helpers.logger import logger

def modify_output_after_agent(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Checks for crisis related statements from agent response.
    If present, returns new Content to *replace* the agent's original output.
    If not preset, continue the flow
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    logger.info(f"\n[Callback] Exiting agent: {agent_name} (Inv: {invocation_id})")

    filtered_text = None

    if agent_name == 'primary_therapist':
        primary_therapist_message = current_state.get("primary_therapist_response")
        filtered_text = detect_crisis(primary_therapist_message) or primary_therapist_message
    elif agent_name == 'fallback_therapist':
        fallback_therapist_message = current_state.get("fallback_therapist_response")
        filtered_text = detect_crisis(fallback_therapist_message) or fallback_therapist_message
    else:
        logger.info(f"[Callback] State condition not met: Using agent {agent_name}'s original output.")
        return None

    return types.Content(
        parts=[types.Part(text=filtered_text)],
        role="model"
    )