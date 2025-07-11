CRISIS_PROTOCOLS = {
    "suicide_risk": {
        "text_response": "أشعر أنك تمر بألم عميق الآن، وأنا هنا لأستمع. من فضلك، إذا كنت تفكر في إيذاء نفسك، اتصل برقم الطوارئ [9999] على الفور، أو تواصل مع خط الدعم النفسي في عمان على الرقم [أدخل رقم الخط الساخن المخصص]. المساعدة متاحة لك.",
        "emergency_contact": "9999 (Police/Ambulance, Oman)",
        "mental_health_hotline": "+968 24 607 555 (Royal Hospital Psychiatry Department – Mental Health Support Line)"
    },
    "harm_to_others_risk": {
        "text_response": "أسمع أنك تشعر بالغضب الشديد، ولكن من فضلك، إذا كنت تفكر في إيذاء شخص آخر، فمن الضروري أن تطلب المساعدة على الفور. هذا ليس شيئًا يجب عليك التعامل معه بمفردك. اتصل بالشرطة على [9999].",
        "emergency_contact": "9999 (Police/Ambulance, Oman)",
        "mental_health_hotline": "+968 24 607 555 (Royal Hospital Psychiatry Department – Mental Health Support Line)"
    },
    "acute_distress_no_direct_harm": {
        "text_response": "يبدو أنك تمر بضائقة شديدة وصعوبة بالغة. أنا هنا لأستمع وأقدم الدعم، ولكن يبدو أن هذا الموقف يتطلب دعمًا بشريًا مباشرًا. إذا كنت تشعر بالإرهاق الشديد أو أنك لا تستطيع التعامل مع مشاعرك، فكر في التواصل مع أخصائي نفسي أو طبيب. يمكنك العثور على مساعدة متخصصة من خلال [أدخل رابطًا أو اسم مؤسسة صحية نفسية في عمان].",
        "emergency_contact": "9999 (شرطة/إسعاف سلطنة عمان - للطوارئ الجسدية)",
        "mental_health_hotline": "+968 24 607 555 (Royal Hospital Psychiatry Department – Mental Health Support Line)"
    }
}

SUICIDE_KEYWORDS = [
    # Direct statements of intent
    "أريد أن أموت",            # I want to die
    "سأنهي حياتي",           # I will end my life
    "سأؤذي نفسي",            # I will harm myself
    "أفكر في الانتحار",       # I am thinking of suicide
    "انتحر",                  # Commit suicide (as a verb)
    "لا أريد العيش",          # I don't want to live
    "سأتخلص من نفسي",        # I will get rid of myself
    "أتمنى لو لم أولد",       # I wish I was never born

    # Indirect statements of hopelessness/desire to disappear
    "لا أستطيع الاستمرار",    # I can't go on
    "تعبت من الحياة",        # Tired of life
    "أريد أن أختفي",          # I want to disappear
    "لا أرى أي أمل",          # I see no hope
    "لا يوجد مخرج",           # There is no way out
    "أتمنى أن أنام ولا أستيقظ", # I wish to sleep and not wake up
    "لن يفتقدني أحد",         # No one will miss me
    "كل شيء مظلم",            # Everything is dark
    "أشعر باليأس",            # I feel despair
    "الحياة لا تستحق",        # Life is not worth it

    # Methods (be cautious with too specific terms to avoid prompting)
    "حبوب",                    # Pills (in context of overdose)
    "حبل",                     # Rope (in context of hanging)
    "سكين",                    # Knife (in context of cutting/stabbing)
    "قفز",                     # Jump (in context of jumping from height)

    # Passive suicidal ideation
    "أتمنى لو مت",             # I wish I was dead
    "ياريت أموت",              # I wish I would die (colloquial)
    "الموت أرحم",             # Death is more merciful

    # Common Omani/Gulf Arabic variations (approximate transliteration for some common phrases)
    "خلاص ما فيني اتحمل",     # That's it, I can't bear it anymore (Omani/Gulf colloquial)
    "ما أبغي أعيش",           # I don't want to live (Omani/Gulf colloquial)
    "قلبي يعورني وايد",      # My heart hurts a lot (can imply deep emotional pain)

    # English phrases if code-switching is common
    "I want to die",
    "kill myself",
    "end my life",
    "suicide",
    "can't go on",
    "I give up",
    "no point"
]

HARM_OTHERS_KEYWORDS = [
    # Direct threats
    "سأؤذيه",                 # I will harm him/her
    "سأقتله",                 # I will kill him/her
    "سأنتقم",                 # I will take revenge
    "أريد أن أضر شخصًا",       # I want to harm someone
    "سأضربه",                 # I will hit him/her
    "سأعتدي عليه",             # I will assault him/her
    "لن أتركه يفلت",           # I won't let him get away
    "سأجعله يندم",             # I will make him regret it

    # Expressing intense rage/violent fantasies
    "أريد تدمير كل شيء",      # I want to destroy everything
    "أنا غاضب لدرجة أريد أن أكسر", # I'm so angry I want to break things
    "لابد أن يدفع الثمن",     # He/she must pay the price
    "أريد أن أرى الألم في عيونهم", # I want to see pain in their eyes

    # Specific terms
    "تهديد",                   # Threat
    "عنف",                     # Violence
    "قتل",                     # Killing
    "ضرب",                     # Hitting

    # English phrases if code-switching is common
    "I will kill",
    "I will hurt",
    "I want to harm",
    "revenge",
    "attack him/her",
    "gonna get them"
]