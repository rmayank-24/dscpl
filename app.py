

import streamlit as st
from gemini_chain import get_chat_chain
from rag.rag_chain import get_rag_context
from utils import get_sos_message, get_reflection_prompt, generate_ics
from video_links import video_map
import random
import datetime

st.set_page_config(page_title="DSCPL - Your Spiritual Companion", layout="wide")
st.markdown("""
    <h1 style='text-align: center; font-size: 3rem; color: #FACC15;'>DSCPL</h1>
    <h4 style='text-align: center; color: #f5f5f5;'></h4>
""", unsafe_allow_html=True)

chat_chain = get_chat_chain()

if "stage" not in st.session_state:
    st.session_state.stage = "category"
    st.session_state.selected_category = None
    st.session_state.selected_topic = None
    st.session_state.duration_days = 1
    st.session_state.chat_history = []
    st.session_state.program_active = False
    st.session_state.program_day = 1
    st.session_state.program_total_days = 0
    st.session_state.program_category = None
    st.session_state.program_topic = None
    st.session_state.history = []

category_topics = {
    "Devotion": [
        "Dealing with Stress", "Overcoming Fear", "Conquering Depression", "Relationships",
        "Healing", "Purpose & Calling", "Anxiety", "Something else..."
    ],
    "Prayer": [
        "Personal Growth", "Healing", "Family/Friends", "Forgiveness",
        "Finances", "Work/Career", "Something else..."
    ],
    "Meditation": [
        "Peace", "God's Presence", "Strength", "Wisdom", "Faith", "Something else..."
    ],
    "Accountability": [
        "Pornography", "Alcohol", "Drugs", "Sex", "Addiction", "Laziness", "Something else..."
    ]
}

prompt_templates = {
    "Devotion": """You are a wise Christian spiritual mentor speaking to your beloved disciple. Provide a 5-minute devotion on the topic '{topic}' that includes:
1. A Bible Verse
2. A short reflective prayer
3. A faith-based declaration
Speak with a pastoral, scripture-rooted, and encouraging voice.""",

    "Prayer": """You are a compassionate spiritual companion. Based on the topic '{topic}', lead a prayer using the ACTS model:
- Adoration
- Confession
- Thanksgiving
- Supplication
Let the tone be humble, heartfelt, and grounded in faith.""",

    "Meditation": """You are a peaceful Christian meditation guide. On the topic '{topic}', provide:
1. A scripture focus
2. Two reflective prompts
3. A breathing rhythm (Inhale 4s, Hold 4s, Exhale 4s)
Use a voice filled with grace and calm.""",

    "Accountability": """You are a spiritual accountability mentor. For the topic '{topic}', provide:
1. A strength-based Bible verse
2. A truth declaration rooted in faith
3. A healthy alternative action
4. A short SOS encouragement
Be gentle, understanding, and scripture-infused."""
}  # unchanged

def show_video_for_topic(category):
    videos = video_map.get(category, [])
    if videos:
        video = random.choice(videos)
        st.markdown(f"<h5 style='margin-top: 1rem;'>🎥 {video['title']}</h5>", unsafe_allow_html=True)
        st.markdown(f"<video width='320' height='180' controls><source src='{video['url']}' type='video/mp4'>Your browser does not support the video tag.</video>", unsafe_allow_html=True)

def button_deck(prompt, options, key_prefix):
    st.markdown(f"<div style='margin-bottom:10px; font-weight: bold;'>{prompt}</div>", unsafe_allow_html=True)
    if len(options) < 1:
        return None
    num_cols = min(len(options), 5)
    rows = [options[i:i+num_cols] for i in range(0, len(options), num_cols)]
    for r, row in enumerate(rows):
        cols = st.columns(len(row))
        for i, option in enumerate(row):
            if cols[i].button(option, key=f"{key_prefix}_{r}_{option}"):
                return option
    return None

# 🚨 Always show main category buttons
st.markdown("<h4 style='margin-top: 2rem;'>✨ Choose Spiritual Focus Anytime</h4>", unsafe_allow_html=True)
category_choice = button_deck("What do you need today?", ["Devotion", "Prayer", "Meditation", "Accountability", "Just Chat"], "main_category")
if category_choice:
    st.session_state.selected_category = category_choice
    if category_choice == "Just Chat":
        st.session_state.stage = "chat"
        st.session_state.chat_history.append({"role": "assistant", "content": "My dear child, I'm here to listen. What is on your heart today? Speak freely, and I will respond with wisdom, scripture, and love."})
    else:
        st.session_state.stage = "duration"
    st.rerun()

if st.session_state.stage == "duration":
    if "duration_choice" not in st.session_state:
        duration = button_deck("How many days would you like this program for?", ["Today Only", "3 Days", "7 Days", "14 Days", "30 Days", "Custom Duration"], "duration")
        if duration:
            st.session_state.duration_choice = duration
            st.rerun()
    else:
        choice = st.session_state.duration_choice
        if choice in ["Today Only", "3 Days", "7 Days", "14 Days", "30 Days"]:
            st.session_state.duration_days = int(choice.split()[0]) if choice != "Today Only" else 1
            del st.session_state.duration_choice
            st.session_state.stage = "topic"
            st.rerun()
        elif choice == "Custom Duration":
            custom_days = st.number_input("Enter custom number of days:", min_value=1, max_value=30, step=1)
            if st.button("Confirm Duration"):
                st.session_state.duration_days = custom_days
                del st.session_state.duration_choice
                st.session_state.stage = "topic"
                st.rerun()
if st.session_state.stage == "topic":
    category = st.session_state.selected_category
    topics = category_topics.get(category, [])
    topic = button_deck(f"What topic would you like help with in {category.lower()}?", topics, "topic")
    if topic:
        st.session_state.selected_topic = topic
        st.session_state.program_active = True
        st.session_state.program_day = 1
        st.session_state.program_total_days = st.session_state.duration_days
        st.session_state.program_category = category
        st.session_state.program_topic = topic
        st.session_state.stage = "program"
        st.rerun()

# Phase 2: Daily Program Progress
if st.session_state.stage == "program" and st.session_state.program_active:
    cat = st.session_state.program_category
    topic = st.session_state.program_topic
    day = st.session_state.program_day
    total = st.session_state.program_total_days

    st.markdown(f"## 📅 Day {day} of {total} – {cat}: {topic}")
    prompt = prompt_templates[cat].format(topic=topic)
    response = chat_chain.invoke({"input": prompt}, config={"configurable": {"session_id": "default"}})
    st.session_state.chat_history.append({"role": "assistant", "content": f"Day {day} – {response.content}"})
    st.markdown(response.content)
    show_video_for_topic(cat)

    if st.button("✅ Mark Day Complete"):
        st.session_state.history.append({"date": str(datetime.date.today()), "category": cat, "topic": topic, "day": day})
        if day >= total:
            st.success("🎉 You’ve completed your program! Well done!")
            st.session_state.program_active = False
            st.session_state.stage = "category"
        else:
            st.session_state.program_day += 1
        st.rerun()

# Calendar Export Option
if st.session_state.program_active and st.button("📆 Export to Calendar (.ics)"):
    ics_data = generate_ics(cat, topic, st.session_state.program_total_days)
    st.download_button("Download .ics file", data=ics_data, file_name="dscpl_program.ics")

# Progress Dashboard
if len(st.session_state.history) > 0:
    st.markdown("## 📊 Program History")
    for entry in st.session_state.history:
        st.markdown(f"- {entry['date']}: {entry['category']} - {entry['topic']} (Day {entry['day']})")

# Chat + Input (no change)
st.markdown("<h4 style='margin-top: 2rem;'>🚨 Ongoing Conversation</h4>", unsafe_allow_html=True)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("What would you like to do today?"):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    context = get_rag_context(user_input)
    full_prompt = f"You are a Christian spiritual mentor responding with scripture, grace, and love. Here's some spiritual context:\n\n{context}\n\nUser said: {user_input}"
    response = chat_chain.invoke({"input": full_prompt}, config={"configurable": {"session_id": "default"}})
    st.session_state.chat_history.append({"role": "assistant", "content": response.content})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(response.content)
