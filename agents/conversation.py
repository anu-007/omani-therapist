import random
from typing import Optional
from google.genai import types

from .runner import get_runner
from .services.session import CustomSessionService
from .services.artifacts import get_artifacts
from core.config import APP_NAME, USER_ID

async def run_conversation(preference_text: Optional[str] = None):
    try:
        SESSION_ID = str(random.randint(1, 1000))

        # Initialize session service first
        session_service = CustomSessionService()
        
        # Create session using the service
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )

        # get artifact
        artifact = get_artifacts()
        
        # get runner
        runner = get_runner(APP_NAME, session_service, artifact)

        # forma initial message
        content = types.Content(role='user', parts=[types.Part(text=preference_text)])

        # run convertation
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
            if event.actions and (event.actions.escalate or event.actions.transfer_to_agent):
                await CustomSessionService.filter_events(session_service, APP_NAME, USER_ID, SESSION_ID)
            
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
        
        print("Workflow completed with result:", final_response_text)
        return final_response_text
        
    except Exception as e:
        print(f"Error in run_conversation: {str(e)}")
        raise
