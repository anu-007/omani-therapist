from google.adk.tools import ToolContext
from litellm import completion
from core.config import MODEL_TEXT
from ..prompts import translate_to_english_prompt

def translate_to_english(tool_context: ToolContext) -> dict:
    """
    Translates text (potentially mixed Arabic-English) to pure Arabic.
    
    Args:
        tool_context (ToolContext): The context object containing state
        
    Returns:
        dict: A dictionary containing status and translated text
    """
    try:
        print("===== Dish details enrichment ========")

        translated_text = completion(
            model = MODEL_TEXT,
            messages=[
                {
                    "role": "user",
                    "content": translate_to_english_prompt
                }
            ]
        )
        print('english data', translated_text)

        return {
            "status": "success",
            "data": translated_text.choices[0].message.content
        }
    except Exception as e:
        print(f"Error enriching dish data: {e}")
        return {"status": "error", "message": str(e)}