import random
from typing import Optional
from google.genai import types

from .runner import get_runner
from .services.session import CustomInMemorySessionService
from .services.artifacts import get_artifacts
from core.config import APP_NAME

async def run_conversation(user_text: Optional[str] = None, user_id: str = None, session_id: str = None):
    try:
        # Initialize session service first
        session_service = CustomInMemorySessionService()
        print('CUstom in memory session init')

        # find existing session
        found_session = await session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
        
        # create session if session not found
        if found_session is None:
            await session_service.create_session(
                app_name = APP_NAME,
                user_id = user_id or str(random.randint(1, 1000)),
                session_id = session_id or str(random.randint(1, 1000))
            )

        # get artifact
        artifact = get_artifacts()
        
        # get runner
        runner = get_runner(APP_NAME, session_service, artifact)

        # forma initial message
        content = types.Content(role='user', parts=[types.Part(text=user_text)])

        # run convertation
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            if event.actions and (event.actions.escalate or event.actions.transfer_to_agent):
                await CustomInMemorySessionService.filter_events(session_service, APP_NAME, user_id, session_id)
            
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
        
        print("Workflow completed with result:", final_response_text)
        return final_response_text
        
    except Exception as e:
        print(f"Error in run_conversation: {str(e)}")
        raise
