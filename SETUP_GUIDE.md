# CBSE Tutor App - Setup & Configuration Guide

## 🚀 Quick Start for Students

### Prerequisites
- Python 3.8 or higher
- Internet connection
- Google Gemini API Key (FREE)

---

## ⚙️ Setup Instructions

### Step 1: Get Your FREE Gemini API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key (it will look like: `AIzaSy...`)

### Step 2: Set the API Key

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="paste_your_key_here"
```

**On Windows (Command Prompt):**
```batch
set GEMINI_API_KEY=paste_your_key_here
```

**On Linux/Mac:**
```bash
export GEMINI_API_KEY="paste_your_key_here"
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the App

```bash
streamlit run app.py
```

OR

```bash
python -m streamlit run app.py
```

---

## 🔥 Features Available

### ✅ With API Key (Recommended)
- **AI-Generated Practice Questions** - Unique, chapter-specific MCQs
- **Interactive AI Chat** - Ask questions, get instant answers
- **Audio Summaries** - Chapter-specific 2-3 minute lectures
- **Study Guides** - Comprehensive notes tailored to each chapter
- **Smart Question Analysis** - AI-powered q&a extraction

### ⚠️ Without API Key (Limited Mode)
- Video search and resources
- Progress tracking
- Problem submission to teachers
- NCERT PDF library
- Basic practice tests (generic questions)

---

## 📌 Important Notes

### For Best Experience:
1. **Always set API key before running** - Copy-paste the command each time you open a new terminal
2. **Internet required** - AI features need internet connection
3. **First load may be slow** - AI generates content on-demand
4. **Free tier limits** - Gemini free tier: 60 requests/minute

### Common Issues:

**"GEMINI_API_KEY not set" error:**
- Solution: Follow Step 2 above in your terminal before running app

**"API key invalid" error:**
- Solution: Get a new key from https://makersuite.google.com/app/apikey

**Questions are generic/repetitive:**
- Solution: Make sure API key is set correctly
- Check: Run `echo %GEMINI_API_KEY%` (Windows) or `echo $GEMINI_API_KEY` (Linux/Mac)

---

## 🎓 For Students

This app is designed to help you:
- Practice with AI-generated questions
- Get instant doubt clarification
- Listen to audio summaries on the go
- Track your progress
- Access NCERT textbooks

**Tip:** Use the **Interactive AI Chat** feature to ask any doubts about the chapter!

---

## 👨‍🏫 For Teachers/Deployment

If deploying for students:

1. **Set API key as environment variable** system-wide:
   - Windows: System Properties > Environment Variables
   - Linux: Add to `/etc/environment` or `~/.bashrc`

2. **Or include .env file** (not recommended for git):
   ```
   GEMINI_API_KEY=your_key_here
   ```

3. **Monitor API usage** at: https://makersuite.google.com/app/apikey

---

## 📞 Support

Having issues? Check:
1. API key is set: `echo %GEMINI_API_KEY%` or `echo $GEMINI_API_KEY`
2. Internet connection is active
3. Python version: `python --version` (need 3.8+)
4. All dependencies installed: `pip install -r requirements.txt`

---

**Happy Learning! 🎉**
