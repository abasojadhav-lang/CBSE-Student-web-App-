import streamlit as st
import pandas as pd
import os
import time
import base64
from data import get_chapters_by_subject, ALL_CHAPTERS
from utils import search_videos, generate_questions, get_pyqs, get_random_motivation, get_flashcards, get_book_context, generate_welcome_speech, get_featured_video
from pdf_generator import generate_pyq_pdf, generate_chapter_notes
from ncert_downloader_enhanced import download_all_ncert_books, download_by_chapter_list
from problem_manager import add_problem, get_all_problems, get_problems_by_status, get_problems_by_subject_chapter, add_teacher_response
from mcq_generator import get_chapter_mcqs, get_mock_test_mcqs, save_test_result, get_recent_results
from progress_tracker import get_progress, update_test_performance, get_weak_chapters, get_overall_stats, add_time_spent
from notebook_llm_features import (
    generate_multi_format_questions, 
    generate_chapter_summary_audio, 
    generate_podcast_conversation,
    generate_study_guide,
    extract_qa_from_document
)
from ai_chatbot import create_chatbot
from api_check import show_api_setup_warning, show_api_status_sidebar

# Page Config
st.set_page_config(
    page_title="Learnixis - CBSE Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main Header Area logic will come AFTER styling


# Custom CSS for Dark Theme and Styling
# Custom CSS for Premium Look
st.markdown("""
<style>
    /* 1. Global Spacing & Background - ULTRA COMPACT */
    div.block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-height: 100vh !important;
    }
    
    /* Reduce all section spacing */
    .element-container {
        margin-bottom: 0.2rem !important;
    }
    
    /* Compact dividers */
    hr {
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }
    
    /* 2. Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* 3. Main Title Styling - COMPACT */
    .title-text {
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.8rem !important;
        padding-bottom: 0;
        margin: 0;
        line-height: 1.2;
    }
    
    .subtitle-text {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        background: -webkit-linear-gradient(90deg, #4ade80, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -5px;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }
    
    /* 4. Professional Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(37, 99, 235, 0.3);
    }
    
    /* 5. Card/Expander Styling */
    div[data-testid="stExpander"] {
        border: 1px solid #334155;
        border-radius: 10px;
        background-color: #1e293b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 6. Sidebar Polish */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    /* 7. Hide Main Scrollbar */
    ::-webkit-scrollbar {
        width: 0px;
        height: 0px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: transparent;
    }
    
    /* Hide scrollbar for Firefox */
    * {
        scrollbar-width: none;
    }
    
    /* 8. Reduce Container Heights */
    .element-container {
        max-height: 600px;
    }
    
    /* Audio player sizing */
    audio {
        max-width: 300px;
        height: 40px;
    }
    
    /* Remove default top margin of standard headers */
    h1 {
        padding-top: 0rem !important;
    }
    
    /* Founder Image Ring */
    .founder-img {
         border: 2px solid #00C9FF;
    }
    
    /* FIX: Force White Text in Expanders for Deploy */
    .streamlit-expanderContent, .streamlit-expanderHeader {
        color: #e2e8f0 !important;
    }
    div[data-testid="stExpander"] p, 
    div[data-testid="stExpander"] div,
    div[data-testid="stExpander"] span {
        color: #e2e8f0 !important;
    }

    /* Sidebar Dropdown Styling - Premium Look */
    div[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #60a5fa;
        color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    div[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {
        border-color: #00C9FF;
        box-shadow: 0 0 8px rgba(0, 201, 255, 0.3);
    }

    /* Target the dropdown text explicitly */
    div[data-testid="stSidebar"] div[data-baseweb="select"] span {
        font-weight: 600;
        color: #e2e8f0;
    }
    
    /* Dropdown Options Styling */
    div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: #0f172a !important;
        border: 1px solid #334155;
    }
    
    div[data-baseweb="menu"] li:hover {
        background-color: #1e293b !important;
        color: #00C9FF !important;
    }
    
    /* FORCE VISIBILITY FOR SIDEBAR LABELS */
    .st-emotion-cache-16idsys p, .st-emotion-cache-10trblm, label, .stMarkdown p {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    /* Sidebar Headers */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #00C9FF !important; /* Bright Cyan */
        text-shadow: 0 0 10px rgba(0, 201, 255, 0.3);
    }

    /* CHATBOT VISIBILITY FIX */
    /* User Message */
    div[data-testid="stChatMessage"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    div[data-testid="stChatMessage"] p, 
    div[data-testid="stChatMessage"] div {
        color: #f1f5f9 !important; /* Bright White-Slate */
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
        color: #f1f5f9 !important;
    }

    /* HIDE STREAMLIT BRANDING & GITHUB ICON essentially */
    .stDeployButton {
        display: none !important;
    }
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    #MainMenu {
        visibility: hidden;
    }
    header {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:

    # Founder Section (Moved to Top)
    if os.path.exists("founder.jpg"):
        col1, col2 = st.columns([1, 2])
        with col1:
             st.image("founder.jpg", width=80, caption="")
        with col2:
            st.markdown("""
                <div style='text-align: left; margin-top: 0;'>
                    <h3 style='margin:0; font-size: 1.1em;'>Abaso Jadhav</h3>
                    <p style='color: #60a5fa; font-size: 0.8em; margin:0;'>Founder</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Show API connection status
    show_api_status_sidebar()
    
    st.divider()
    
    
    # Board Selection
    board = st.selectbox(
        "Select Board",
        ["CBSE", "Maharashtra State Board"],
        index=0
    )
    
    # Dynamic Class & Subject Lists based on Board
    if board == "Maharashtra State Board":
        st.markdown('<p style="color: #fbbf24; font-size: 0.8rem;">Note: Currently optimization for Class 10 (Marathi Medium)</p>', unsafe_allow_html=True)
        class_options = [10]
        subject_options = [
            "Science 1", "Science 2", 
            "Math 1 (Algebra)", "Math 2 (Geometry)",
            "History", "Geography",
            "Marathi", "English"
        ]
        # Medium Selection
        medium = st.radio("Select Medium", ["Marathi", "English"], horizontal=True, index=0)
    else:
        # CBSE Defaults
        class_options = [11, 12]
        subject_options = ["Physics", "Chemistry", "Biology", "Mathematics"]
        medium = "English" # Default implicit
    
    class_num = st.selectbox("Select Class", class_options)
    
    subject = st.selectbox("Select Subject", subject_options)
    
    # Pass board to filtering
    chapters = get_chapters_by_subject(subject, class_num, board)
    
    # Localize names if Marathi Medium is selected
    if medium == "Marathi":
        # Create mapping to find original name back if needed (or just use index match)
        # Using name_mr if available, else name
        chapter_display_names = [ch.get("name_mr", ch["name"]) for ch in chapters]
    else:
        chapter_display_names = [ch["name"] for ch in chapters]
    
    selected_chapter_display = st.selectbox(
        "Select Chapter",
        ["Select a Chapter..."] + chapter_display_names
    )
    
    # Map back to chapter object
    selected_chapter_name = "Select a Chapter..."
    if selected_chapter_display != "Select a Chapter...":
        if medium == "Marathi":
             # Find matching chapter obj
             for ch in chapters:
                 if ch.get("name_mr") == selected_chapter_display:
                     selected_chapter_name = ch["name"] # Keep internal logic on English ID/Name
                     break
                 # Fallback if name_mr was missing and we used name
                 elif ch["name"] == selected_chapter_display:
                     selected_chapter_name = ch["name"]
                     break
        else:
             selected_chapter_name = selected_chapter_display
    
    # Reset manual book selection if chapter changes
    if "last_selected_chapter" not in st.session_state:
        st.session_state.last_selected_chapter = selected_chapter_name
        
    if st.session_state.last_selected_chapter != selected_chapter_name:
         st.session_state.manual_book_selection = None
         st.session_state.last_selected_chapter = selected_chapter_name

# Main Header Area
col_h1, col_h2, col_h3 = st.columns([2, 1, 1.5])

with col_h1:
    st.markdown('<div style="text-align: left;"><h1 class="title-text">Learnixis</h1><p class="subtitle-text" style="margin-top: -10px;">Ignite Your Learning Potential</p></div>', unsafe_allow_html=True)
    # CBSE Board Note
    st.markdown('<p style="color: #fbbf24; font-size: 0.85rem; margin-top: -10px;">⚠️ for CBSE Board (others soon!)</p>', unsafe_allow_html=True)

with col_h2:
    # ⏱️ Focus Timer
    st.markdown("<h5 style='margin-bottom:0; padding-top:10px;'>⏱️ Focus Timer</h5>", unsafe_allow_html=True)
    
    # Session State for Timer
    if 'pomodoro_active' not in st.session_state:
        st.session_state.pomodoro_active = False
        st.session_state.pomodoro_start_time = 0
        st.session_state.pomodoro_duration = 25 * 60 # 25 mins

    # Compact Layout for Timer
    col_t1, col_t2 = st.columns([1, 1])
    with col_t1:
        focus_time = st.number_input("Mins", min_value=1, max_value=120, value=25, step=5, label_visibility="collapsed", key="header_pomo_input")
    with col_t2:
        if st.button("Start 🚀", key="header_pomo_start", use_container_width=True):
             st.session_state.pomodoro_active = True
             st.session_state.pomodoro_end_time = time.time() + (focus_time * 60)
             st.rerun()

    if st.session_state.get('pomodoro_active'):
        remaining = st.session_state.pomodoro_end_time - time.time()
        if remaining > 0:
            mins, secs = divmod(int(remaining), 60)
            st.metric("Focusing...", f"{mins:02}:{secs:02}")
            time.sleep(1) 
            st.rerun()
        else:
             st.session_state.pomodoro_active = False
             st.balloons()
             st.success("Done! ☕")

with col_h3:
    # 💭 Thought of the Day (Session-persistent)
    # Initialize thought once per session - it will only change when app reopens
    if 'thought_of_day' not in st.session_state:
        st.session_state.thought_of_day = get_random_motivation()
    
    quote = st.session_state.thought_of_day
    st.markdown(f"""
    <div style="
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #00C9FF; 
        border-right: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin-top: 5px;
        text-align: left;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    ">
        <p style="
            font-size: 0.85rem;
            font-style: italic;
            color: #94a3b8;
            margin: 0;
            line-height: 1.3;
        ">{quote}</p>
    </div>
    """, unsafe_allow_html=True)

if selected_chapter_name != "Select a Chapter...":
    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    st.divider()
    
    # Header for chosen chapter
    st.title(f"📖 {selected_chapter_name}")
    st.caption(f"Class {class_num} • {subject}")
    
    # Tabs for Organization
    tab1, tab_rev, tab2, tab_practice, tab_progress, tab_ps, tab_ai, tab4 = st.tabs([
        "📺 Videos", 
        "⚡ Revision", 
        "📋 Q&A",
        "🎯 Practice", 
        "📊 Progress", 
        "🧩 Solving",
        "🤖 AI Study Tools", 
        "📚 Books"
    ])

    
    with tab_rev:
        st.subheader(f"⚡ Flashcards: {selected_chapter_name}")
        
        if "flashcard_idx" not in st.session_state:
            st.session_state.flashcard_idx = 0
        if "flashcard_flipped" not in st.session_state:
            st.session_state.flashcard_flipped = False
            
        fc_data = get_flashcards(selected_chapter_name)
        current_card = fc_data[st.session_state.flashcard_idx]
        
        # Card Container
        card_height = 300
        
        col_c1, col_c2, col_c3 = st.columns([1, 4, 1])
        with col_c2:
            # Card Styling
            st.markdown(f"""
            <div style="
                background-color: #1e293b;
                border: 2px solid #3b82f6;
                border-radius: 16px;
                height: {card_height}px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 20px;
                text-align: center;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
                cursor: pointer;
            ">
                <div style="font-size: 1.2rem; color: #94a3b8; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;">
                    { 'DEFINITION' if st.session_state.flashcard_flipped else 'TERM' }
                </div>
                <div style="font-size: 2rem; font-weight: 800; color: #f8fafc;">
                    { current_card['definition'] if st.session_state.flashcard_flipped else current_card['term'] }
                </div>
                <div style="margin-top: 20px; font-size: 0.9rem; color: #64748b;">
                    (Tap 'Flip' to reveal)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Controls
            c1, c2, c3 = st.columns([1, 2, 1])
            with c1:
                if st.button("⬅️ Prev", use_container_width=True):
                    st.session_state.flashcard_idx = (st.session_state.flashcard_idx - 1) % len(fc_data)
                    st.session_state.flashcard_flipped = False
                    st.rerun()
            with c2:
                if st.button("🔄 Flip Card", type="primary", use_container_width=True):
                    st.session_state.flashcard_flipped = not st.session_state.flashcard_flipped
                    st.rerun()
            with c3:
                if st.button("Next ➡️", use_container_width=True):
                    st.session_state.flashcard_idx = (st.session_state.flashcard_idx + 1) % len(fc_data)
                    st.session_state.flashcard_flipped = False
                    st.rerun()
            
            st.markdown(f"<div style='text-align:center; color:#64748b; margin-top:10px;'>Card {st.session_state.flashcard_idx + 1} of {len(fc_data)}</div>", unsafe_allow_html=True)
    
    with tab1:
        # Featured Section
        feat_key = f"featured_{subject}_{class_num}_{selected_chapter_name}"
        if feat_key not in st.session_state:
             st.session_state[feat_key] = get_featured_video(selected_chapter_name, subject, class_num)
        
        featured = st.session_state[feat_key]
        if featured:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1e293b, #0f172a); 
                padding: 20px; 
                border-radius: 12px; 
                border: 1px solid #3b82f6; 
                margin-bottom: 30px; 
                box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.5);
                display: flex;
                align-items: center;
                gap: 20px;
            ">
                <div style="flex: 0 0 40%; max-width: 320px;">
                    <a href="{featured['link']}" target="_blank">
                         <img src="{featured['thumbnail']}" style="width: 100%; border-radius: 8px; border: 2px solid #60a5fa;">
                         <div style="text-align:center; color: #60a5fa; margin-top:5px; font-weight:bold;">Example from {featured['channel']}</div>
                    </a>
                </div>
                <div style="flex: 1;">
                    <div style="color: #60a5fa; font-size: 0.9rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">
                        ⭐ Featured: CBSE Syllabus 2025 Focus
                    </div>
                    <a href="{featured['link']}" target="_blank" style="text-decoration:none;">
                    <div style="color: white; font-size: 1.5rem; font-weight: 800; line-height: 1.2; margin-bottom: 15px;">
                        {featured['title']}
                    </div>
                    </a>
                    <div style="color: #cbd5e1; font-size: 1rem; line-height: 1.5;">
                        This selected video covers the entire <b>{selected_chapter_name}</b> syllabus for this year. Perfect for a complete revision or starting from scratch.
                    </div>
                     <div style="margin-top: 15px;">
                        <a href="{featured['link']}" target="_blank" style="
                            background-color: #3b82f6; 
                            color: white; 
                            padding: 8px 16px; 
                            border-radius: 6px; 
                            text-decoration: none; 
                            font-weight: bold;
                            display: inline-block;
                        ">
                            ▶️ Watch Featured Class
                        </a>
                     </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("More Recommended Videos")
        
        # Fetch videos using smart search
        with st.spinner(f"Finding best videos for {selected_chapter_name}..."):
            session_key = f"videos_{subject}_{class_num}_{selected_chapter_name}"
            
            if session_key not in st.session_state:
                 st.session_state[session_key] = search_videos(f"{selected_chapter_name}", subject)
            
            videos = st.session_state[session_key]
        
        if not videos:
            st.warning("No videos found. Check your internet connection.")
        else:
            cols = st.columns(3)
            for idx, video in enumerate(videos):
                with cols[idx % 3]:
                     # Determine tag based on duration
                    duration_min = 0
                    parts = video['duration'].split(':')
                    if len(parts) == 2: duration_min = int(parts[0])
                    elif len(parts) == 3: duration_min = int(parts[0])*60
                    
                    badge_color = "#3b82f6" # blue
                    badge_text = "Concept"
                    if duration_min > 45: 
                        badge_color = "#ef4444" # red
                        badge_text = "One Shot"
                    elif duration_min < 10:
                        badge_color = "#22c55e" # green
                        badge_text = "Quick Rev"
                    
                    st.markdown(f"""
                    <div class="video-card">
                        <a href="{video['link']}" target="_blank" style="text-decoration:none; color:white;">
                            <img src="{video['thumbnail']}" width="100%" style="border-radius:10px; margin-bottom:10px;">
                            <div style="font-weight:bold; font-size:1.1em; overflow:hidden; white-space:nowrap; text-overflow:ellipsis;">{video['title']}</div>
                            <div style="font-size:0.8em; color:#94a3b8; display:flex; justify-content:space-between; margin-top:5px;">
                                <span>{video['channel']}</span>
                                <span style="color:#22d3ee;">{video['duration']}</span>
                            </div>
                             <div style="margin-top:5px; font-size: 0.7em; background-color:{badge_color}; display:inline-block; padding:2px 6px; border-radius:4px;">{badge_text}</div>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"💡 Important Questions (50+)")
            
            # Using Session State to keep questions persistent for download
            if "generated_questions" not in st.session_state:
                st.session_state.generated_questions = []

            col_gen, col_dl = st.columns([1, 1])
            with col_gen:
                if st.button("Generate Q&A", key="qa_btn"):
                    st.session_state.generated_questions = generate_questions(selected_chapter_name)
            
            with col_dl:
                if st.session_state.generated_questions:
                    from pdf_generator import generate_qa_pdf
                    if st.button("Download Q&A PDF"):
                        qa_pdf_path = generate_qa_pdf(selected_chapter_name, st.session_state.generated_questions)
                        with open(qa_pdf_path, "rb") as f:
                            st.download_button(
                                label="Confirm Save",
                                data=f,
                                file_name=f"Questions_{selected_chapter_name}.pdf",
                                mime="application/pdf",
                                key="final_qa_dl"
                            )
            
            if st.session_state.generated_questions:
                # Display in a scrollable container
                with st.container(height=500):
                    for q in st.session_state.generated_questions:
                        with st.expander(f"Q{q['id']}: {q['question']} ({q['difficulty']})"):
                            st.markdown(f"**Question:** {q['question']}")
                            st.write(f"**Answer:** {q['answer']}")
        
        with col2:
            st.subheader("📝 Previous Year Papers")
            
            if class_num == 12 or (board == "Maharashtra State Board" and class_num == 10):
                years = [2024, 2023, 2022, 2021, 2020]
                prefix = "MH-SSC" if board == "Maharashtra State Board" else "CBSE"
                
                for year in years:
                    # Adjusted column ratio to prevent wrapping
                    col_a, col_b = st.columns([2, 1]) 
                    with col_a:
                        st.write(f"**{prefix} {subject} {year}**")
                    with col_b:
                        if st.button(f"Download PDF", key=f"dl_{year}", use_container_width=True): # Full width button
                            pdf_path = generate_pyq_pdf(subject, class_num, year)
                            with open(pdf_path, "rb") as pdf_file:
                                 st.download_button(
                                    label=f"Confirm",
                                    data=pdf_file,
                                    file_name=f"{prefix}_{subject}_{class_num}_{year}.pdf",
                                    mime="application/pdf",
                                    key=f"real_dl_{year}"
                                )
                            st.success(f"Generated!")
            else:
                 st.info("Previous Year Board Papers are available for Class 12 CBSE & Class 10 Maharashtra.")


    # Practice Mode Tab
    with tab_practice:
        st.subheader("🎯 Practice Mode - Test Your Knowledge")
        
        # Show API warning if needed
        api_available = show_api_setup_warning()
        
        # Test type selection
        test_type = st.radio("Select Test Type", 
                            ["📚 Chapter Test (10 Q)", "⏰ Mock Test (30 Q)", "🎓 Full Syllabus Test"],
                            horizontal=True)
        
        st.divider()
        
        # Initialize session state for test
        if 'test_active' not in st.session_state:
            st.session_state.test_active = False
        if 'test_questions' not in st.session_state:
            st.session_state.test_questions = []
        if 'test_answers' not in st.session_state:
            st.session_state.test_answers = {}
        if 'test_start_time' not in st.session_state:
            st.session_state.test_start_time = None
        
        if not st.session_state.test_active:
            # Test setup screen
            st.info(f"💡 **{test_type}**: Test yourself and track your progress!")
            
            if test_type == "📚 Chapter Test (10 Q)":
                st.markdown(f"**Chapter**: {selected_chapter_name}")
                st.markdown(f"**Questions**: 10 MCQs from this chapter")
            elif test_type == "⏰ Mock Test (30 Q)":
                st.markdown(f"**Subject**: {subject}")
                st.markdown(f"**Questions**: 30 MCQs from multiple chapters")
                st.markdown(f"**Time Limit**: 30 minutes")
            else:
                st.markdown(f"**Subject**: {subject}")
                st.markdown(f"**Questions**: 50 MCQs from entire syllabus")
                st.markdown(f"**Time Limit**: 45 minutes")
            
            col_start, col_recent = st.columns([1, 1])
            
            with col_start:
                if st.button("🚀 Start Test", type="primary", use_container_width=True):
                    # Generate AI questions for the test
                    with st.spinner("🤖 Generating test questions using AI..."):
                        if test_type == "📚 Chapter Test (10 Q)":
                            # Generate chapter-specific questions
                            questions = generate_multi_format_questions(
                                selected_chapter_name,
                                subject,
                                ["MCQ"],  # Only MCQs for practice test
                                count=10,
                                difficulty="Medium"
                            )
                        elif test_type == "⏰ Mock Test (30 Q)":
                            # Mixed difficulty for mock test
                            questions = generate_multi_format_questions(
                                selected_chapter_name,
                                subject,
                                ["MCQ"],
                                count=30,
                                difficulty=None  # Mix of all difficulties
                            )
                        else:
                            # Full syllabus - harder questions
                            questions = generate_multi_format_questions(
                                selected_chapter_name,
                                subject,
                                ["MCQ"],
                                count=50,
                                difficulty="Hard"
                            )
                    
                    if questions:
                        st.session_state.test_questions = questions
                        st.session_state.test_answers = {}
                        st.session_state.test_active = True
                        st.session_state.test_start_time = time.time()
                        st.session_state.current_test_type = test_type
                        st.rerun()
                    else:
                        st.error("Failed to generate questions. Please check your internet connection.")
            
            with col_recent:
                # Show recent test results
                recent = get_recent_results(3)
                if recent:
                    with st.expander("📊 Recent Results"):
                        for result in recent:
                            st.markdown(f"**{result['test_type']}** - {result['chapter']}")
                            st.markdown(f"Score: {result['score']}/{result['total']} ({result['percentage']}%)")
                            st.caption(result['timestamp'])
                            st.divider()
        
        else:
            # Test active - show questions
            questions = st.session_state.test_questions
            total_questions = len(questions)
            
            # Timer (for timed tests)
            if "Mock Test" in st.session_state.current_test_type or "Full Syllabus" in st.session_state.current_test_type:
                time_limit = 1800 if "Mock" in st.session_state.current_test_type else 2700  # 30 or 45 min
                elapsed = time.time() - st.session_state.test_start_time
                remaining = max(0, time_limit - elapsed)
                
                mins, secs = divmod(int(remaining), 60)
                
                col_timer, col_progress = st.columns([1, 3])
                with col_timer:
                    if remaining > 0:
                        st.metric("⏰ Time Left", f"{mins:02}:{secs:02}")
                    else:
                        st.error("⏰ Time's Up!")
                with col_progress:
                    answered = len(st.session_state.test_answers)
                    st.progress(answered / total_questions, text=f"Progress: {answered}/{total_questions} answered")
                
                if remaining <= 0:
                    st.warning("Time is up! Please submit your test.")
            
            st.divider()
            
            # Display questions
            for idx, q in enumerate(questions):
                st.markdown(f"### Question {idx + 1}")
                st.markdown(f"**{q['question']}**")
                
                answer = st.radio(
                    "Select your answer:",
                    q['options'],
                    key=f"q_{idx}",
                    index=st.session_state.test_answers.get(idx, None)
                )
                
                # Store answer only if user has selected something
                if answer is not None:
                    st.session_state.test_answers[idx] = q['options'].index(answer)
                
                st.divider()
            
            # Submit button
            col_sub1, col_sub2 = st.columns([1, 1])
            with col_sub1:
                if st.button("✅ Submit Test", type="primary", use_container_width=True):
                    # Calculate score
                    score = 0
                    for idx, q in enumerate(questions):
                        if st.session_state.test_answers.get(idx) == q['correct']:
                            score += 1
                    
                    time_taken = int(time.time() - st.session_state.test_start_time)
                    
                    # Save result
                    save_test_result(
                        student_name="Student",
                        test_type=st.session_state.current_test_type,
                        subject=subject,
                        chapter=selected_chapter_name,
                        score=score,
                        total=total_questions,
                        time_taken=time_taken,
                        answers=st.session_state.test_answers
                    )
                    
                    # Update progress
                    update_test_performance(subject, selected_chapter_name, score, total_questions)
                    add_time_spent(time_taken // 60)
                    
                    # Show results
                    st.session_state.test_result = {
                        'score': score,
                        'total': total_questions,
                        'percentage': round((score/total_questions)*100, 2),
                        'time_taken': time_taken
                    }
                    st.session_state.test_active = False
                    st.session_state.show_results = True
                    st.rerun()
            
            with col_sub2:
                if st.button("❌ Cancel Test", use_container_width=True):
                    st.session_state.test_active = False
                    st.session_state.test_questions = []
                    st.session_state.test_answers = {}
        # Show results if just submitted
        if st.session_state.get('show_results'):
            result = st.session_state.test_result
            
            st.balloons()
            
            st.markdown("## 🎉 Test Results")
            
            # Score card
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("Score", f"{result['score']}/{result['total']}")
            with col_r2:
                st.metric("Percentage", f"{result['percentage']}%")
            with col_r3:
                mins, secs = divmod(result['time_taken'], 60)
                st.metric("Time Taken", f"{mins}m {secs}s")
            
            # Performance feedback
            if result['percentage'] >= 80:
                st.success("🌟 Excellent! You've mastered this topic!")
            elif result['percentage'] >= 60:
                st.info("👍 Good job! Review the explanations below to improve.")
            else:
                st.warning("📚 Keep practicing! Focus on the concepts you missed.")
            
            st.divider()
            
            # Show correct answers
            st.markdown("### 📝 Answer Key")
            questions = st.session_state.test_questions
            answers = st.session_state.test_answers
            
            for idx, q in enumerate(questions):
                user_answer = answers.get(idx)
                is_correct = user_answer == q['correct']
                
                with st.expander(f"Q{idx+1}: {'✅' if is_correct else '❌'} {q['question'][:50]}..."):
                    st.markdown(f"**Question**: {q['question']}")
                    st.markdown(f"**Your Answer**: {q['options'][user_answer] if user_answer is not None else 'Not answered'}")
                    st.markdown(f"**Correct Answer**: {q['options'][q['correct']]}")
                    st.info(f"**Explanation**: {q['explanation']}")
            
            if st.button("🔄 Take Another Test"):
                st.session_state.show_results = False
                st.session_state.test_result = {}
                st.rerun()

    with tab_progress:
        st.subheader("📊 Your Progress Dashboard")
        
        # Get statistics
        stats = get_overall_stats()
        weak = get_weak_chapters(60)
        
        # Overall stats cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📚 Chapters Completed", stats['chapters_completed'])
        with col2:
            st.metric("📝 Tests Taken", stats['total_tests'])
        with col3:
            st.metric("⏱️ Time Spent", f"{stats['total_time_spent']} min")
        with col4:
            st.metric("🎯 Overall Accuracy", f"{stats['overall_accuracy']}%")
        
        st.divider()
        
        # Weak chapters alert
        if weak:
            st.warning(f"⚠️ **Weak Topics Detected**: {len(weak)} chapters need more practice!")
            
            with st.expander("🔍 View Weak Chapters", expanded=True):
                for chapter_data in weak:
                    accuracy = chapter_data['average_accuracy']
                    color = "#ef4444" if accuracy < 40 else "#f59e0b"
                    
                    st.markdown(f"""
                    <div style="
                        background-color: #1e293b;
                        border-left: 4px solid {color};
                        padding: 15px;
                        border-radius: 8px;
                        margin-bottom: 10px;
                    ">
                        <h4 style="color: #f8fafc; margin: 0;">{chapter_data['chapter']}</h4>
                        <p style="color: #94a3b8; font-size: 0.9rem; margin: 5px 0;">
                            Subject: {chapter_data['subject']} | Accuracy: {accuracy}%
                        </p>
                        <p style="color: #cbd5e1; font-size: 0.85rem;">
                            Tests Taken: {chapter_data['tests_taken']} | 
                            Correct: {chapter_data['total_correct']}/{chapter_data['total_questions']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"📖 Practice {chapter_data['chapter']}", key=f"practice_{chapter_data['chapter']}"):
                        st.info("Switch to Practice Mode tab to take a test!")
        else:
            st.success("🎉 Great! No weak topics detected. Keep up the excellent work!")
        
        st.divider()
        
        # Chapter-wise performance
        st.markdown("### 📈 Chapter-wise Performance")
        
        progress_data = get_progress()
        chapter_accuracy = progress_data.get('accuracy_by_chapter', {})
        
        if chapter_accuracy:
            for key, data in chapter_accuracy.items():
                col_ch1, col_ch2 = st.columns([3, 1])
                
                with col_ch1:
                    st.markdown(f"**{data['chapter']}**")
                    accuracy = data['average_accuracy']
                    
                    # Color-coded progress bar
                    if accuracy >= 80:
                        bar_color = "🟢"
                    elif accuracy >= 60:
                        bar_color = "🟡"
                    else:
                        bar_color = "🔴"
                    
                    st.progress(accuracy/100, text=f"{bar_color} {accuracy}% ({data['tests_taken']} tests)")
                
                with col_ch2:
                    st.metric("Score", f"{data['total_correct']}/{data['total_questions']}")
                
                st.divider()
        else:
            st.info("📚 No test data yet. Take some tests to see your progress!")

    with tab_ps:
        st.subheader("🧑‍🏫 Problem Solving - Teacher & Student Interaction")
        
        # Toggle between Student and Teacher view
        view_mode = st.radio("Select View", ["👨‍🎓 Student View", "👨‍🏫 Teacher View"], horizontal=True, key="view_mode")
        
        st.divider()
        
        if view_mode == "👨‍🎓 Student View":
            # STUDENT VIEW
            st.markdown("### Submit Your Doubt or Problem")
            st.info("💡 Ask your question and a teacher will respond online!")
            
            with st.form("problem_submission_form", clear_on_submit=True):
                col_s1, col_s2 = st.columns(2)
                
                with col_s1:
                    student_name = st.text_input("Your Name *", placeholder="Enter your name")
                with col_s2:
                    student_contact = st.text_input("Contact (Email/Phone)", placeholder="Optional")
                
                problem_text = st.text_area(
                    "Describe Your Problem/Doubt *",
                    placeholder="Explain your doubt in detail...",
                    height=150
                )
                
                submit_btn = st.form_submit_button("📤 Submit Problem", use_container_width=True)
                
                if submit_btn:
                    if student_name and problem_text:
                        problem_id = add_problem(
                            student_name=student_name,
                            subject=subject,
                            chapter=selected_chapter_name,
                            problem_text=problem_text,
                            contact=student_contact
                        )
                        st.success(f"✅ Problem submitted successfully! ID: {problem_id}")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("⚠️ Please fill in your name and problem description")
            
            st.divider()
            
            # Show student's problems for this chapter
            st.markdown("### Your Submitted Problems")
            chapter_problems = get_problems_by_subject_chapter(subject, selected_chapter_name)
            
            if chapter_problems:
                for prob in reversed(chapter_problems):  # Show newest first
                    status_badge = "✅ Answered" if prob["status"] == "answered" else "🔴 Pending"
                    status_color = "#22c55e" if prob["status"] == "answered" else "#ef4444"
                    
                    with st.expander(f"{status_badge} | {prob['student_name']} - {prob['timestamp']}", expanded=prob["status"]=="answered"):
                        st.markdown(f"**Problem ID:** `{prob['id']}`")
                        st.markdown(f"**Student:** {prob['student_name']}")
                        st.markdown(f"**Submitted:** {prob['timestamp']}")
                        st.markdown(f"**Problem:**\n\n{prob['problem']}")
                        
                        if prob["status"] == "answered":
                            st.divider()
                            st.markdown("**👨‍🏫 Teacher's Response:**")
                            st.success(prob["teacher_response"])
                            st.caption(f"Responded on: {prob['response_timestamp']}")
            else:
                st.info("No problems submitted yet for this chapter.")
        
        else:
            # TEACHER VIEW
            st.markdown("### Respond to Student Problems")
            
            # Filter options
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Answered"])
            with filter_col2:
                filter_chapter_toggle = st.checkbox("Show only current chapter", value=True)
            
            # Get problems based on filters
            if filter_chapter_toggle:
                all_problems = get_problems_by_subject_chapter(subject, selected_chapter_name)
            else:
                all_problems = get_all_problems()
            
            # Apply status filter
            if filter_status == "Pending":
                all_problems = [p for p in all_problems if p["status"] == "pending"]
            elif filter_status == "Answered":
                all_problems = [p for p in all_problems if p["status"] == "answered"]
            
            st.markdown(f"**Total Problems:** {len(all_problems)}")
            st.divider()
            
            if all_problems:
                for prob in reversed(all_problems):  # Show newest first
                    status_badge = "✅ Answered" if prob["status"] == "answered" else "🔴 Pending"
                    status_color = "#22c55e" if prob["status"] == "answered" else "#ef4444"
                    
                    # Problem Card
                    st.markdown(f"""
                    <div style="
                        background-color: #1e293b;
                        border-left: 4px solid {status_color};
                        padding: 15px;
                        border-radius: 8px;
                        margin-bottom: 15px;
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="color: #f8fafc; margin: 0;">{prob['student_name']}</h4>
                            <span style="background: {status_color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem;">{status_badge}</span>
                        </div>
                        <p style="color: #94a3b8; font-size: 0.85rem; margin: 5px 0;">
                            ID: {prob['id']} | Subject: {prob['subject']} | Chapter: {prob['chapter']}
                        </p>
                        <p style="color: #cbd5e1; font-size: 0.9rem;">Submitted: {prob['timestamp']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander(f"View & Respond - {prob['id']}", expanded=prob["status"]=="pending"):
                        st.markdown(f"**Student Contact:** {prob.get('contact', 'Not provided')}")
                        st.markdown(f"**Problem:**")
                        st.info(prob['problem'])
                        
                        if prob["status"] == "answered":
                            st.markdown("**Previous Response:**")
                            st.success(prob["teacher_response"])
                            st.caption(f"Responded on: {prob['response_timestamp']}")
                        
                        st.divider()
                        
                        # Response form
                        with st.form(f"response_form_{prob['id']}"):
                            teacher_response = st.text_area(
                                "Your Response",
                                placeholder="Provide detailed explanation and solution...",
                                height=150,
                                key=f"response_{prob['id']}"
                            )
                            
                            respond_btn = st.form_submit_button("📨 Send Response", use_container_width=True)
                            
                            if respond_btn and teacher_response:
                                add_teacher_response(prob['id'], teacher_response)
                                st.success("✅ Response sent successfully!")
                                time.sleep(1)
                                st.rerun()
            else:
                st.info("No problems found matching the selected filters.")


    with tab_ai:
        st.subheader("🎓 AI Tutor - Interactive Learning Session")
        st.caption("Your personal AI instructor - Ask anything about this chapter!")
        
        # Show API warning if needed
        api_available = show_api_setup_warning()
        
        st.divider()
        
        # Initialize chatbot in session state
        chatbot_key = f"chatbot_{subject}_{selected_chapter_name}"
        if chatbot_key not in st.session_state:
            st.session_state[chatbot_key] = create_chatbot(selected_chapter_name, subject, class_num)
            
        chatbot = st.session_state[chatbot_key]
        
        # Debug: Show chatbot status
        if chatbot.model is None:
            st.error("⚠️ Chatbot model failed to initialize. Please restart the app.")
            st.stop()
        else:
            st.success("✅ AI Chatbot is ready!", icon="🤖")
        
        # Main interactive interface - 2 columns
        col_chat_main, col_chat_sidebar = st.columns([2, 1])
        
        with col_chat_main:
            st.markdown("### 💬 Conversation with AI Tutor")
            
            # Check for API Key
            if not os.getenv("GEMINI_API_KEY") and "GEMINI_API_KEY" not in st.secrets:
                st.error("⚠️ **Missing API Key**: Please set `GEMINI_API_KEY` in `.streamlit/secrets.toml` or environment variables.")
                st.info("You can get a free key from [Google AI Studio](https://aistudio.google.com/).")
                st.stop()

            chat_history = chatbot.get_history()
            
            # Callback to handle submission BEFORE rerun
            def submit_question():
                if st.session_state.user_question_input:
                    user_q = st.session_state.user_question_input
                    # Generate response immediately
                    chatbot.ask(user_q)
                    # Clear input
                    st.session_state.user_question_input = ""
            
            # Input area - MOVED TO TOP as per user request
            with st.container():
                col_input, col_btn = st.columns([5, 1])
                with col_input:
                    st.text_input(
                        "Ask a question", 
                        placeholder="Type your question here...",
                        label_visibility="collapsed",
                        key="user_question_input",
                        on_change=submit_question
                    )
                with col_btn:
                    if st.button("📤 Ask", type="primary", use_container_width=True):
                        submit_question()
                        st.rerun()

            # Container for chat messages
            chat_container = st.container(height=500)
            
            # Render History (which now includes the new Q&A)
            if chat_history:
                with chat_container:
                    # Invert order: Newest at top? User asked for "Reverse".
                    # "Type question is below and answer is up. do reverse."
                    # Means standard: Input Top -> History Bottom (Newest at bottom of container)
                    
                    for idx, exchange in enumerate(chat_history):
                        with st.chat_message("user", avatar="👤"):
                            st.write(exchange['question'])
                        with st.chat_message("assistant", avatar="🎓"):
                            st.write(exchange['answer'])
                        st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info(f"""
                👋 **Welcome to your interactive AI tutor!**
                I'm here to help you master **{selected_chapter_name}**. Ask me anything!
                """)
            
            # Removed the "submitted" block because handle_question updates history directly
            
        with col_chat_sidebar:
            # Clear Chat Button - Top of sidebar
            if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
                chatbot.clear_history()
                st.rerun()
            
            st.markdown("### 💡 Quick Start")
            
            st.markdown("**Suggested Questions:**")
            suggested = chatbot.get_suggested_questions()
            
            for idx, suggestion in enumerate(suggested):
                if st.button(
                    suggestion, 
                    key=f"suggest_ai_{idx}", 
                    use_container_width=True,
                    help="Click to ask this question"
                ):
                    # Append user question to UI
                    with chat_container:
                         with st.chat_message("user", avatar="👤"):
                             st.write(suggestion)
                         
                         with st.chat_message("assistant", avatar="🎓"):
                             message_placeholder = st.empty()
                             full_response = ""
                             
                             try:
                                 # Initial Loading state
                                 message_placeholder.write("Thinking...")
                                 
                                 for chunk in chatbot.ask_stream(suggestion):
                                     full_response += chunk
                                     message_placeholder.markdown(full_response)
                                 
                                 st.rerun()
                             except Exception as e:
                                 st.error(f"❌ Error: {str(e)}")
            
            st.divider()
            
            # Study aids section
            st.markdown("### 📚 Study Aids")
            
            # Audio summary
            with st.expander("🎧 Audio Summary", expanded=False):
                st.caption("Listen to a 2-3 minute chapter summary")
                
                if st.button("🔊 Generate Summary", key="gen_audio_summary_ai", use_container_width=True):
                    with st.spinner("Generating audio..."):
                        audio_path = generate_chapter_summary_audio(
                            selected_chapter_name,
                            subject,
                            class_num
                        )
                    
                    if audio_path:
                        st.session_state['current_audio'] = audio_path
                        st.rerun()
                
                # Play audio if generated
                if 'current_audio' in st.session_state and st.session_state['current_audio']:
                    st.audio(st.session_state['current_audio'], format="audio/mp3")
            
            # Study guide
            with st.expander("📖 Study Guide", expanded=False):
                st.caption("Generate comprehensive notes")
                
                guide_template = st.radio(
                    "Format:",
                    ["Bullet Points", "Detailed Notes", "Flashcards"],
                    key="guide_template_ai",
                    horizontal=False
                )
                
                if st.button("📝 Generate Guide", key="gen_guide_ai", use_container_width=True):
                    with st.spinner("Creating study guide..."):
                        template_map = {
                            "Bullet Points": "bullet_points",
                            "Detailed Notes": "detailed_notes",
                            "Flashcards": "flashcard_format"
                        }
                        
                        guide_content = generate_study_guide(
                            selected_chapter_name,
                            subject,
                            class_num,
                            template_map[guide_template]
                        )
                    
                    st.session_state['study_guide'] = guide_content
                    st.rerun()
                
                # Display guide if generated
                if 'study_guide' in st.session_state and st.session_state['study_guide']:
                    st.markdown(st.session_state['study_guide'])
                    
                    # Download option
                    st.download_button(
                        "⬇️ Download as Markdown",
                        st.session_state['study_guide'],
                        file_name=f"{selected_chapter_name}_study_guide.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
            
            st.divider()
            
            st.markdown("### ✨ Tips")
            st.markdown("""
            - **Be specific** in your questions
            - Ask for **examples**
            - Request **step-by-step** solutions
            - Clarify **any doubt** instantly
            - Get **exam strategies**
            """)








    with tab4:
        st.subheader("📚 Digital Library")
        
        # Library Actions
        col_lib1, col_lib2 = st.columns([3, 1])
        with col_lib1:
             st.info("Manage your Library: Download official NCERT books directly.")
        with col_lib2:
            if st.button("⬇️ Download All Books", type="secondary", use_container_width=True):
                 with st.status("Downloading NCERT Textbooks...", expanded=True) as status:
                     st.write(f"Fetching chapter-wise PDFs for Class {class_num} {subject}...")
                     st.write("This may take several minutes...")
                     
                     stats = download_all_ncert_books(
                         classes=[class_num], 
                         subjects=[subject],
                         output_dir="books"
                     )
                     
                     st.write(f"✓ Successfully downloaded: {stats['successful']} chapters")
                     st.write(f"○ Already had: {stats['skipped']} chapters")
                     if stats['failed'] > 0:
                         st.write(f"✗ Failed: {stats['failed']} chapters")
                     
                     status.update(label="Download Complete!", state="complete", expanded=False)
                     st.rerun()
                     
        books_dir = "books"
        if not os.path.exists(books_dir):
            os.makedirs(books_dir)
            
        # Syllabus Status Monitor
        with st.expander("📂 View Syllabus & File Status", expanded=False):
            st.write(f"**{subject} Class {class_num} - Library Status**")
            
            # Fetch all expected chapters
            all_chapters = get_chapters_by_subject(subject, class_num)
            
            # Check files
            existing_files = os.listdir(books_dir)
            
            for chap in all_chapters:
                c_name = chap['name']
                # Fuzzy check
                is_present = False
                safe_c_name = "".join([c for c in c_name if c.isalnum() or c in (' ','-','_')]).strip()
                
                matched_filename = None
                for f in existing_files:
                    if c_name.lower() in f.lower() or safe_c_name.lower() in f.lower():
                        is_present = True
                        matched_filename = f
                        break
                
                # Display row
                col_s1, col_s2 = st.columns([4, 1])
                with col_s1:
                    st.write(f"• {c_name}")
                with col_s2:
                    if is_present:
                        # Use callback to ensure state persists before rerun
                        def set_book(fname):
                            st.session_state.manual_book_selection = fname
                            
                        st.button(
                            "📖 Read", 
                            key=f"read_{safe_c_name}",
                            on_click=set_book,
                            args=(matched_filename,)
                        )
                    else:
                        st.caption("❌ Missing")
        
        if "manual_book_selection" in st.session_state:
             st.write(f"DEBUG: Session has manual_book_selection: {st.session_state.manual_book_selection}")
        
        # 1. Smart Matching: Look for a book based on manual selection OR fuzzy match
        matching_book = None
        all_books = os.listdir(books_dir)
        st.write(f"DEBUG: Found {len(all_books)} books in directory.")
        
        # Priority: Manual Selection
        manual_sel = st.session_state.get("manual_book_selection")
        
        # Check if manual selection actually exists on disk
        if manual_sel:
            manual_path = os.path.join(books_dir, manual_sel)
            if os.path.exists(manual_path):
                 st.write(f"DEBUG: Manual selection validated on disk: {manual_sel}")
                 matching_book = manual_sel
            else:
                 # Clean up invalid state
                 st.warning(f"Selected book '{manual_sel}' not found.")
                 st.session_state.manual_book_selection = None
        
        if not matching_book:
            # Fallback: Simple fuzzy match
            safe_chapter_name = "".join([c for c in selected_chapter_name if c.isalnum() or c in (' ','-','_')]).strip()
            
            for book in all_books:
                if selected_chapter_name.lower() in book.lower() or safe_chapter_name.lower() in book.lower():
                    matching_book = book
                    break
        
        if matching_book:
            st.success(f"📖 Found Textbook: {matching_book}")
            selected_book = matching_book
        else:
             # Generative Experience
            st.info(f" No textbook found for **{selected_chapter_name}**.")
            
            col_gen1, col_gen2 = st.columns([2, 1])
            with col_gen1:
                 st.write("Use our AI to write comprehensive study notes for this chapter instantly!")
            with col_gen2:
                if st.button(f"✨ Generate Notes for {selected_chapter_name}", type="primary", use_container_width=True):
                    with st.spinner("AI is writing your chapter notes... (This takes 2-3 seconds)"):
                        # Fetch Flashcards to use as data source
                        fc_data = get_flashcards(selected_chapter_name)
                        new_pdf = generate_chapter_notes(selected_chapter_name, subject, fc_data, medium)
                        time.sleep(1) # UX Pause
                        st.rerun()
            
            # Show other books meanwhile
            st.divider()
            st.write("Or read available books:")
            selected_book = st.selectbox("Select a Book", [b for b in all_books if b.endswith('.pdf')])

        # 2. PDF Viewer
        if selected_book:
            pdf_path = os.path.join(books_dir, selected_book)
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)

else:
    # Empty State - Home Page Info (Native Streamlit Components)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🚀 Welcome to Your Personal Learning Hub")
    
    # Auto-play Motivation (First Load Only)
    if 'has_played_welcome' not in st.session_state:
        speech_file = generate_welcome_speech()
        st.audio(speech_file, format='audio/mp3', autoplay=True)
        st.session_state.has_played_welcome = True
    
    # High Visibility Instruction
    st.markdown("""
    <div style="background-color: rgba(30, 41, 59, 0.8); border-left: 5px solid #00C9FF; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <p style="color: #e2e8f0; font-size: 1.1rem; margin: 0;">
            👈 Also select a <span style="color: #00C9FF; font-weight: 800;">Subject</span> and <span style="color: #92FE9D; font-weight: 800;">Chapter</span> to start!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.info("**📺 Curated Videos**\n\nHigh-quality 'One Shot' & Topic-wise video tutorials for every chapter.")
        
    with col_f2:
        st.success("**📝 Smart Q&A**\n\nGenerate 50+ exam questions & download PDFs for offline practice.")
        
    with col_f3:
        st.warning("**🤖 AI Tutor**\n\n24/7 Instant doubt solving, definitions, and formulas.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 👈 Get Started by choosing a Class & Subject!")
