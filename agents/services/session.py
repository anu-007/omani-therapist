from google.adk.sessions import Session, InMemorySessionService

class CustomInMemorySessionService(InMemorySessionService):
    def __init__(self):
        super().__init__()
    
    async def filter_events(self, app: str, user: str, sess: str) -> Session:
        """
        Post-process session events to remove internal tool calls.
        
        Args:
            app: Application name
            user: User ID 
            sess: Session ID
            
        Returns:
            Session with filtered events
        """

        # Get current session from database
        current_session = await self.get_session(
            app_name=app,
            user_id=user,
            session_id=sess
        )
        
        if not current_session:
            raise ValueError(f"No session found for {app}/{user}/{sess}")

        filtered_events = []
        
        # Filter events without modifying DB
        for event in current_session.events:
            if event.author == 'user':
                filtered_events.append(event)
            
            if hasattr(event, 'is_final_response') and event.is_final_response():
                filtered_events.append(event)
                continue

        # Update only the filtered session's events
        current_session.events = filtered_events
        
        return current_session