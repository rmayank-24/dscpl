# utils.py

def get_sos_message():
    return (
        "🆘 I'm here for you. Let’s pause and breathe together... 🌬️\n\n"
        "**Scripture for Strength:** _'The Lord is my strength and my shield.'_ (Psalm 28:7)\n\n"
        "**You are not alone. You are loved. You are stronger than this.** 💪\n\n"
        "Would you like to talk about what you're feeling?"
    )

def get_reflection_prompt():
    return (
        "📝 Before we end today... take a moment to reflect:\n"
        "- What’s one thing you're grateful for?\n"
        "- What’s one challenge you faced?\n\n"
        "_Gratitude turns what we have into enough._ 🌅"
    )

def format_response_with_emojis(text: str) -> str:
    # Optional emoji booster — very basic for now
    text = text.replace("God", "🙏 God")
    text = text.replace("peace", "🕊️ peace")
    text = text.replace("strength", "💪 strength")
    return text
