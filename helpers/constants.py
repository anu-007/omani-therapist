CRISIS_PROTOCOLS = {
    "suicide_risk": {
        "text_response": "أشعر أنك تمر بألم عميق الآن، وأنا هنا لأستمع. من فضلك، إذا كنت تفكر في إيذاء نفسك، اتصل برقم الطوارئ [9999] على الفور، أو تواصل مع خط الدعم النفسي في عمان على الرقم [أدخل رقم الخط الساخن المخصص]. المساعدة متاحة لك.",
        "emergency_contact": "9999 (شرطة/إسعاف سلطنة عمان - للطوارئ الجسدية)",
        "mental_health_hotline": "+968 24 607 555 (Royal Hospital Psychiatry Department – Mental Health Support Line)"
    },
    "harm_to_others_risk": {
        "text_response": "أسمع أنك تشعر بالغضب الشديد، ولكن من فضلك، إذا كنت تفكر في إيذاء شخص آخر، فمن الضروري أن تطلب المساعدة على الفور. هذا ليس شيئًا يجب عليك التعامل معه بمفردك. اتصل بالشرطة على [9999].",
        "emergency_contact": "9999 (شرطة/إسعاف سلطنة عمان - للطوارئ الجسدية)",
        "mental_health_hotline": "+968 24 607 555 (Royal Hospital Psychiatry Department – Mental Health Support Line)"
    },
    "acute_distress_no_direct_harm": {
        "text_response": "يبدو أنك تمر بضائقة شديدة وصعوبة بالغة. أنا هنا لأستمع وأقدم الدعم، ولكن يبدو أن هذا الموقف يتطلب دعمًا بشريًا مباشرًا. إذا كنت تشعر بالإرهاق الشديد أو أنك لا تستطيع التعامل مع مشاعرك، فكر في التواصل مع أخصائي نفسي أو طبيب. يمكنك العثور على مساعدة متخصصة من خلال [أدخل رابطًا أو اسم مؤسسة صحية نفسية في عمان].",
        "emergency_contact": "9999 (شرطة/إسعاف سلطنة عمان - للطوارئ الجسدية)",
        "mental_health_hotline": "+968 24 607 555 (Royal Hospital Psychiatry Department – Mental Health Support Line)"
    }
}

SUICIDE_KEYWORDS = [
    "أريد أن أموت",            # I want to die
    "سأنهي حياتي",           # I will end my life
    "سأؤذي نفسي",            # I will harm myself
    "أفكر في الانتحار",       # I am thinking of suicide
    "انتحر",                  # Commit suicide (as a verb)
    "لا أريد العيش",          # I don't want to live
    "سأتخلص من نفسي",        # I will get rid of myself
    "أتمنى لو لم أولد",       # I wish I was never born
    "لا أستطيع الاستمرار",    # I can't go on (when combined with other suicidal indicators)
    "أتمنى أن أنام ولا أستيقظ", # I wish to sleep and not wake up
    "أتمنى لو مت",             # I wish I was dead
    "ياريت أموت",              # I wish I would die (colloquial)
    "الموت أرحم",             # Death is more merciful
    "خلاص ما فيني اتحمل",     # That's it, I can't bear it anymore (Omani/Gulf colloquial, indicating extreme endpoint)
    "ما أبغي أعيش",           # I don't want to live (Omani/Gulf colloquial)
    "I want to die",
    "kill myself",
    "end my life",
    "suicide"      # Keyword set by agent
]

HARM_OTHERS_KEYWORDS = [
    "سأؤذيه",                 # I will harm him/her
    "سأقتله",                 # I will kill him/her
    "سأنتقم",                 # I will take revenge
    "أريد أن أضر شخصًا",       # I want to harm someone
    "سأضربه",                 # I will hit him/her
    "سأعتدي عليه",             # I will assault him/her
    "لن أتركه يفلت",           # I won't let him get away
    "سأجعله يندم",             # I will make him regret it
    "أريد تدمير كل شيء",      # I want to destroy everything (if context implies violence towards others)
    "لابد أن يدفع الثمن",     # He/she must pay the price (if context implies violent retribution)
    "تهديد",                   # Threat
    "عنف",                     # Violence
    "قتل",                     # Killing
    "ضرب",                     # Hitting
    "I will kill",
    "I will hurt",
    "I want to harm",
    "revenge",
    "attack him/her",
    "gonna get them",
    "harm_to_other" # Keyword set by agent
]

ACUTE_DISTRESS_KEYWORDS = [
    "ما أقدر أتحمل",         # I can't bear it/handle it (implies extreme limit)
    "حاس بإني بنهار",        # I feel like I'm breaking down
    "مخنوق",                 # Suffocated/choked (emotionally, implying extreme distress)
    "أزمة نفسية",            # Psychological crisis/breakdown (direct term for severe distress)
    "ما قادر أسيطر على نفسي", # I can't control myself (referring to emotions, implying loss of composure)
    "بالي مشغول جدًا",       # My mind is very busy/preoccupied (if coupled with other extreme distress cues)
    "تعبان نفسيًا",          # Mentally exhausted/tired (if extreme)
    "قلق للغاية",            # Extremely anxious
    "مضطرب جدًا",            # Very distressed/agitated
    "في قمة التوتر",          # At the peak of stress/tension
    "acute_distress"
]

CRISIS_RESPONSES = [
    "أشعر أنك تمر بألم عميق الآن، وأنا هنا لأستمع. من فضلك، إذا كنت تفكر في إيذاء نفسك، اتصل برقم الطوارئ [9999] على الفور، أو تواصل مع خط الدعم النفسي في عمان على الرقم [أدخل رقم الخط الساخن المخصص]. المساعدة متاحة لك.",
    "أسمع أنك تشعر بالغضب الشديد، ولكن من فضلك، إذا كنت تفكر في إيذاء شخص آخر، فمن الضروري أن تطلب المساعدة على الفور. هذا ليس شيئًا يجب عليك التعامل معه بمفردك. اتصل بالشرطة على [9999].",
    "يبدو أنك تمر بضائقة شديدة وصعوبة بالغة. أنا هنا لأستمع وأقدم الدعم، ولكن يبدو أن هذا الموقف يتطلب دعمًا بشريًا مباشرًا. إذا كنت تشعر بالإرهاق الشديد أو أنك لا تستطيع التعامل مع مشاعرك، فكر في التواصل مع أخصائي نفسي أو طبيب. يمكنك العثور على مساعدة متخصصة من خلال [أدخل رابطًا أو اسم مؤسسة صحية نفسية في عمان]."
]