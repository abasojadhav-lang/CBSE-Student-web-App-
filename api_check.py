# API Setup Check Component
import streamlit as st
import os

def show_api_setup_warning():
    """Display warning if API key is not configured"""
    if not os.getenv("GEMINI_API_KEY"):
        st.info("ℹ️ **AI Features are limited** - Set `GEMINI_API_KEY` for full features. [Setup Guide](https://makersuite.google.com/app/apikey)")
        return False
    return True


def show_api_status_sidebar():
    """Show API status in sidebar"""
    with st.sidebar:
        st.divider()
        if os.getenv("GEMINI_API_KEY"):
            st.success("✅ AI Features: ACTIVE")
            st.caption("Gemini API connected")
        else:
            st.error("❌ AI Features: LIMITED")
            st.caption("[Setup Guide](SETUP_GUIDE.md)")
