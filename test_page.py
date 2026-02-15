"""
Simple Test Page - Verify API Key Access
"""
import streamlit as st
import os

st.title("🔍 API Key Test")

st.write("## Checking API Key Access...")

# Method 1: Streamlit Secrets
st.write("### 1. Streamlit Secrets:")
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.success(f"✅ SUCCESS! Key found. Length: {len(api_key)}, First 15 chars: {api_key[:15]}...")
except Exception as e:
    st.error(f"❌ FAILED: {str(e)}")

# Method 2: Environment Variable
st.write("### 2. Environment Variable:")
env_key = os.getenv("GEMINI_API_KEY", "")
if env_key:
    st.success(f"✅ Found in env: {env_key[:15]}...")
else:
    st.warning("⚠️ Not in environment variables (expected for cloud)")

# Method 3: Import and test the actual module
st.write("### 3. Testing ai_chatbot module:")
try:
    from ai_chatbot import GEMINI_API_KEY
    if GEMINI_API_KEY:
        st.success(f"✅ ai_chatbot loaded key! Length: {len(GEMINI_API_KEY)}")
    else:
        st.error("❌ ai_chatbot.py GEMINI_API_KEY is empty!")
except Exception as e:
    st.error(f"❌ Error importing: {str(e)}")

# Method 4: Check code version
st.write("### 4. Code Version Check:")
try:
    import ai_chatbot
    import inspect
    code = inspect.getsource(ai_chatbot)
    if 'st.secrets["GEMINI_API_KEY"]' in code:
        st.success("✅ Code is using new st.secrets syntax (bracket notation)")
    elif 'st.secrets.get' in code:
        st.warning("⚠️ Code is using OLD st.secrets.get() syntax - needs update!")
    else:
        st.info("ℹ️ Code is using os.getenv only")
except Exception as e:
    st.error(f"Error checking code: {e}")

st.write("---")
st.write("**If test #1 shows SUCCESS but app still fails, there's a code deployment issue.**")
