# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 00:23:34 2025

@author: EBUNOLUWASIMI
"""

# Iya Bola Assistant App
# Streamlit prototype: text + live dashboard
"""
Run this app with:
streamlit run Banking_Iya_Bola_App_MVP.py
Requirements: streamlit, pandas, langdetect
"""

import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ---------------------------------
# APP CONFIGURATION
# ---------------------------------
#st.set_page_config(page_title="Banking Iya Bola App MVP", layout="wide")

# ---------------------------------
# INITIALIZE SESSION STATE
# ---------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_logs" not in st.session_state:
    st.session_state.user_logs = pd.DataFrame(columns=["timestamp", "user_input", "assistant_response", "intent", "language"])

# ---------------------------------
# SIMPLE INTENT DETECTION
# ---------------------------------
def detect_intent(user_input):
    text = user_input.lower()
    if any(word in text for word in ["balance", "account", "check"]):
        return "Balance Inquiry"
    elif any(word in text for word in ["send", "transfer", "money", "pay"]):
        return "Transfer or Payment"
    elif any(word in text for word in ["airtime", "data", "bundle"]):
        return "Airtime/Data Purchase"
    elif any(word in text for word in ["save", "savings", "goal"]):
        return "Micro-Savings"
    elif any(word in text for word in ["teach", "learn", "budget", "finance"]):
        return "Financial Education"
    else:
        return "General Inquiry"

# ---------------------------------
# LANGUAGE DETECTION (SIMPLIFIED)
# ---------------------------------
def detect_language(user_input):
    if any(word in user_input.lower() for word in ["trowey", "aza my mama", "wetin i get"]):
        return "Pidgin"
    elif any(word in user_input.lower() for word in ["elo ni mo ni", "mo fe fi", "fi ranse si"]):
        return "Yoruba"
    else:
        return "English"

# ---------------------------------
# SIMPLE RESPONSE GENERATOR
# ---------------------------------
def generate_response(user_input):
    intent = detect_intent(user_input)
    language = detect_language(user_input)

    responses = {
        "Balance Inquiry": [
            "Your balance is ₦5,200. Keep saving small small!",
            "You currently have ₦10,000 in your account."
        ],
        "Transfer or Payment": [
            "Transfer successful! The money don go.",
            "Payment processed. Make sure to keep your receipt safe."
        ],
        "Airtime/Data Purchase": [
            "Airtime top-up complete! Talk well, no go finish your credit.",
            "Your data bundle has been activated."
        ],
        "Micro-Savings": [
            "Great! You’ve saved ₦500 towards your savings goal.",
            "Savings updated. Small drops make an ocean!"
        ],
        "Financial Education": [
            "Tip: Always set aside 10% of your income for savings.",
            "Budgeting helps you control money instead of money controlling you!"
        ],
        "General Inquiry": [
            "I can help you check balances, send money, buy airtime, or learn about saving.",
            "Hello! How can I assist you today?"
        ]
    }

    response = random.choice(responses[intent])
    return response, intent, language

# ---------------------------------
# UI HEADER
# ---------------------------------
st.title("💬 Iya Bola Assistant")
st.caption("Inclusive Financial Assistant for Africa — Text-based Prototype")

# ---------------------------------
# CHAT INTERFACE
# ---------------------------------
user_input = st.text_input("Type your message here (English, Pidgin, Yoruba)...", "")

if st.button("Send") and user_input:
    response, intent, language = generate_response(user_input)

    # Log the interaction
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_input": user_input,
        "assistant_response": response,
        "intent": intent,
        "language": language
    }
    st.session_state.user_logs = pd.concat(
        [st.session_state.user_logs, pd.DataFrame([new_row])], ignore_index=True
    )

    # Add to chat history
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Iya Bola Assistant", response))

# ---------------------------------
# DISPLAY CHAT
# ---------------------------------
for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"🧍‍♂️ **{speaker}:** {message}")
    else:
        st.markdown(f"🤖 **{speaker}:** {message}")

# ---------------------------------
# DASHBOARD SECTION
# ---------------------------------
st.markdown("---")
st.subheader("📊 Analytics Dashboard")

if not st.session_state.user_logs.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(st.session_state.user_logs["intent"].value_counts())
    with col2:
        st.bar_chart(st.session_state.user_logs["language"].value_counts())

    st.download_button(
        label="Download Chat Logs (CSV)",
        data=st.session_state.user_logs.to_csv(index=False),
        file_name="sample_user_log.csv",
        mime="text/csv"
    )
else:
    st.info("No chats yet. Start interacting to see analytics here!")
