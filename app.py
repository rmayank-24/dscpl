# app.py

import streamlit as st
from gemini_chain import get_chat_chain
from rag.rag_chain import get_rag_context
from utils import get_sos_message, get_reflection_prompt
from video_links import video_map  # 🔗 New import for video embedding
import random

# 📄 Page Setup
st.set_page_config(page_title="DSCPL - Your Spiritual Companion", layout="wide")
st.markdown("""
    <h1 style='text-align: center; font-size: 3rem; color: #FACC15;'>DSCPL</h1>
    
""", unsafe_allow_html=True)

# 🔁 Memory Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🧠 Load Memory-backed Chat Chain
chat_chain = get_chat_chain()

# 🎥 Embed Video by Category
def embed_category_video(category):
    videos = video_map.get(category, [])
    if videos:
        video = random.choice(videos)  # Randomize or just use videos[0] for static
        st.markdown(f"##### 🎥 {video['title']}")
        st.video(video["url"])
    else:
        st.info("No video content available for this topic yet.")

# 📍 Sidebar Options
with st.sidebar:
    st.header("💡 Spiritual Tools")
    if st.button("🆘 I Need Help Now"):
        st.session_state.messages.append({"role": "assistant", "content": get_sos_message()})
    if st.button("🧘 Daily Reflection Prompt"):
        st.session_state.messages.append({"role": "assistant", "content": get_reflection_prompt()})
    st.markdown("---")
    

# 🔁 Prompt Map with Christian Spiritual Mentor Tone
prompt_map = {
    "✝️ Daily Devotion": """You are a wise Christian spiritual mentor speaking to your beloved disciple. Provide a 5-minute devotion that includes:
1. A Bible Verse
2. A short reflective prayer
3. A faith-based declaration
Speak with a pastoral, scripture-rooted, and encouraging voice.""",

    "🙏 Daily Prayer": """You are a compassionate spiritual companion. Use the ACTS prayer model:
- Adoration
- Confession
- Thanksgiving
- Supplication
Let the tone be humble, heartfelt, and grounded in faith.""",

    "🧘 Meditation": """Guide your disciple in a peaceful meditation based on scripture (e.g., Psalm 46:10).
Include two reflective questions and a breathing rhythm (Inhale 4s, Hold 4s, Exhale 4s).
Your words should be filled with grace and calm.""",

    "🛡️ Accountability": """Encourage a disciple battling temptation. Include:
- A strength-based Bible verse
- A truth declaration rooted in faith
- A healthy alternative action
- A short SOS message
Use a gentle, understanding, and scripture-infused tone.""",

    "💬 Just Chat": None  # Will trigger free-form input
}

# 🗭 Program Buttons
st.subheader("📚 Choose Your Spiritual Focus")
cols = st.columns(5)

label_to_category = {
    "✝️ Daily Devotion": "Devotion",
    "🙏 Daily Prayer": "Prayer",
    "🧘 Meditation": "Meditation",
    "🛡️ Accountability": "Accountability",
    "💬 Just Chat": None
}

for i, label in enumerate(prompt_map):
    with cols[i]:
        if st.button(label):
            st.session_state.messages.append({"role": "user", "content": label})
            prompt_text = prompt_map[label]

            if prompt_text:
                response = chat_chain.invoke(
                    {"input": prompt_text},
                    config={"configurable": {"session_id": "default"}}
                )
                st.session_state.messages.append({"role": "assistant", "content": response.content})

                # ✅ Clean category match
                category_key = label_to_category.get(label)
                if category_key:
                    embed_category_video(category_key)
            else:
                st.session_state.messages.append({"role": "assistant", "content": "I'm here for you. What's on your heart today, my child?"})

# 💬 Conversation
st.divider()
st.subheader("🚨 Ongoing Conversation")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ⌨️ User Chat Input
if prompt := st.chat_input("What would you like to do today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    rag_context = get_rag_context(prompt)
    enhanced_prompt = f"""You are a Christian spiritual mentor responding with scripture, grace, and love. Here's recent spiritual content to guide your response:\n\n{rag_context}\n\nUser asked: {prompt}"""

    response = chat_chain.invoke({"input": enhanced_prompt}, config={"configurable": {"session_id": "default"}})
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    with st.chat_message("assistant"):
        st.markdown(response.content)
