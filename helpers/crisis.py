from .constants import CRISIS_PROTOCOLS, SUICIDE_KEYWORDS, HARM_OTHERS_KEYWORDS, ACUTE_DISTRESS_KEYWORDS

def detect_crisis(message: str) -> str | None:
    """
    Detects if the user's message indicates a crisis and returns the type of crisis.
    Returns None if no crisis, or a string like "suicide_risk", "harm_to_others_risk", "acute_distress_no_direct_harm"
    """
    print("===== Try detecting crisis ========")

    crisis_type = None
    bot_message = None

    for keyword in SUICIDE_KEYWORDS:
        if keyword in message:
            print('matched keyword sucide', keyword)
            crisis_type = "suicide_risk"
    for keyword in HARM_OTHERS_KEYWORDS:
        if keyword in message:
            print('matched keyword harm to other', keyword)
            crisis_type = "harm_to_others_risk"
    for keyword in ACUTE_DISTRESS_KEYWORDS:
        if keyword in message:
            print('matched keyword acute distress', keyword)
            crisis_type = "acute_distress_no_direct_harm"

    print('crisis_type', crisis_type)
    if crisis_type:
        protocol = CRISIS_PROTOCOLS.get(crisis_type, CRISIS_PROTOCOLS["suicide_risk"])
        bot_message = protocol["text_response"]

    return bot_message


        
    