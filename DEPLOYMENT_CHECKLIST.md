# 🚀 Git Deployment Checklist

## ✅ Files to COMMIT (Deploy These)

### Core Application Files
```bash
git add app.py                      # Main app with AI tutor redesign
git add ai_chatbot.py               # NEW - Interactive chatbot module
git add notebook_llm_features.py    # Updated AI model
git add utils.py                    # Shortened welcome speech
```

### New Helper Modules
```bash
git add api_check.py                # NEW - API status checker
```

### Documentation
```bash
git add SETUP_GUIDE.md              # NEW - User setup instructions
git add DEPLOYMENT.md               # NEW - Deployment guide
git add README.md                   # Update if needed
```

### Configuration
```bash
git add requirements.txt            # Updated with google-genai
git add .gitignore                  # Updated to exclude sensitive files
```

---

## ❌ Files to EXCLUDE (Do NOT Commit)

### Sensitive Files (Contains API Key)
```
❌ START_APP.bat          # Contains your API key!
❌ run_app.bat            # Contains your API key!
```

### Test/Debug Scripts
```
❌ test_api.py
❌ test_new_api.py
❌ list_models.py
❌ list_available_models.py
❌ test_*.py (all test files)
```

### Generated/Runtime Files
```
❌ welcome_speech.mp3
❌ audio_summaries/
❌ __pycache__/
❌ user_progress.json
❌ problems_data.json
❌ audio_cache.json
❌ pdf_debug.log
```

---

## 📦 Quick Deploy Commands

### Option 1: Commit All Core Changes
```bash
# Stage only the important files
git add app.py ai_chatbot.py notebook_llm_features.py utils.py api_check.py
git add requirements.txt .gitignore
git add SETUP_GUIDE.md DEPLOYMENT.md

# Commit with descriptive message
git commit -m "Refine AI Study Tools: Interactive tutor, fix Gemini API, enhance UX

- Implemented interactive AI tutor with conversational interface
- Fixed critical Gemini API 404 errors (updated to models/gemini-flash-latest)  
- Removed redundant Questions tab and question generator
- Added API status checking and user-friendly error messages
- Shortened welcome speech to 5 seconds
- Created comprehensive setup and deployment guides
- Enhanced error handling with toast notifications"

# Push to repository
git push origin main
```

### Option 2: Review Changes First
```bash
# See what changed
git status

# Review specific files
git diff app.py
git diff ai_chatbot.py

# Stage selectively
git add -p app.py   # Interactive staging
```

---

## 🔒 Security Checklist

Before pushing, verify:
- [ ] No API keys in committed code
- [ ] `START_APP.bat` and `run_app.bat` are NOT staged
- [ ] `.gitignore` is updated and working
- [ ] No test files committed
- [ ] No user data files committed

### Verify with:
```bash
# Check what will be committed
git diff --staged

# Make sure no API key appears
git diff --staged | grep -i "AIzaSy"   # Should return nothing!
```

---

## 🌐 Production Deployment

### After Git Push:

1. **On Production Server**, set environment variable:
   ```bash
   # Linux/Mac
   export GEMINI_API_KEY="your_api_key_here"
   
   # Windows
   set GEMINI_API_KEY=your_api_key_here
   ```

2. **Install/Update Dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Delete Old Generated Files**:
   ```bash
   rm welcome_speech.mp3  # Will regenerate with new 5-second version
   ```

4. **Run App**:
   ```bash
   streamlit run app.py
   # OR
   python -m streamlit run app.py
   ```

---

## ✅ Verification After Deployment

1. Check sidebar shows: **"✅ API Connected"**
2. Go to AI Study Tools tab
3. Click a suggested question → Should get AI response
4. Try typing custom question → Should work
5. Practice Mode → Questions should generate
6. No warning banners about API key

---

## 📝 Commit Message Template

```
Title: Refine AI Study Tools - Interactive Tutor & API Fixes

Changes:
- Interactive AI chatbot with real-time responses
- Fixed Gemini API compatibility (models/gemini-flash-latest)  
- Removed redundant UI elements (Questions tab, question generator)
- Enhanced error handling and user feedback
- Improved setup process with documentation
- Performance: 5-second welcome vs 45 seconds

Files Modified: 8
New Files: 3
Lines Changed: ~500
```

---

## 🎯 Summary

**COMMIT THESE (8 files):**
1. `app.py`
2. `ai_chatbot.py`
3. `notebook_llm_features.py`
4. `utils.py`
5. `api_check.py`
6. `requirements.txt`
7. `.gitignore`
8. `SETUP_GUIDE.md` / `DEPLOYMENT.md`

**DO NOT COMMIT:**
- Batch files (contain API key)
- Test scripts
- Generated files
- User data

**Ready to deploy? Run the commands above!** 🚀
