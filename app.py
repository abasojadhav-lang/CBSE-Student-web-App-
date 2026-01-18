import streamlit as st
import pandas as pd
import os
from data import get_chapters_by_subject, ALL_CHAPTERS
from utils import search_videos, generate_questions, get_pyqs, get_random_motivation
from pdf_generator import generate_pyq_pdf

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
    /* 1. Global Spacing & Background */
    div.block-container {
        padding-top: 2rem !important; /* Reduce top padding */
        padding-bottom: 2rem !important;
    }
    
    /* 2. Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* 3. Main Title Styling */
    .title-text {
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        padding-bottom: 0.5rem;
        margin: 0;
    }
    
    .subtitle-text {
        font-size: 1.2rem;
        color: #B0B0B0;
        font-weight: 400;
        margin-top: -5px;
        margin-bottom: 20px;
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
    
    /* 7. Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0f172a; 
    }
    ::-webkit-scrollbar-thumb {
        background: #334155; 
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #475569; 
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
</style>
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

    st.header("📚 Curriculum")
    
    subject = st.selectbox(
        "Select Subject",
        ["Physics", "Chemistry", "Biology", "Mathematics"]
    )
    
    class_num = st.selectbox(
        "Select Class",
        [11, 12]
    )
    
    chapters = get_chapters_by_subject(subject, class_num)
    chapter_names = [ch["name"] for ch in chapters]
    
    selected_chapter_name = st.selectbox(
        "Select Chapter",
        ["Select a Chapter..."] + chapter_names
    )

# Main Header Area
col_h1, col_h2 = st.columns([2, 1])

with col_h1:
    st.markdown('<div style="text-align: left;"><h1 class="title-text">Learnixis</h1><p class="subtitle-text">Ignite Your Learning Potential</p></div>', unsafe_allow_html=True)

with col_h2:
    # Motivation Card
    quote = get_random_motivation()
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-right: 4px solid #00C9FF;
        padding: 10px;
        border-radius: 10px 0 0 10px;
        margin-top: 0px;
        text-align: right;
    ">
        <p style="
            font-size: 0.8rem;
            font-style: italic;
            color: #94a3b8;
            margin: 0;
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
    tab1, tab2, tab3 = st.tabs(["📺 Videos", "📝 Q&A & Papers", "🤖 AI Tutor"])
    
    with tab1:
        st.subheader("Recommended Videos")
        
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
                            st.write(f"**Answer:** {q['answer']}")
        
        with col2:
            st.subheader("📝 Previous Year Papers")
            
            if class_num == 12:
                years = [2024, 2023, 2022, 2021, 2020]
                for year in years:
                    # Adjusted column ratio to prevent wrapping
                    col_a, col_b = st.columns([2, 1]) 
                    with col_a:
                        st.write(f"**CBSE {subject} {year}**")
                    with col_b:
                        if st.button(f"Download PDF", key=f"dl_{year}", use_container_width=True): # Full width button
                            pdf_path = generate_pyq_pdf(subject, class_num, year)
                            with open(pdf_path, "rb") as pdf_file:
                                 st.download_button(
                                    label=f"Save PDF",
                                    data=pdf_file,
                                    file_name=f"CBSE_{subject}_{class_num}_{year}.pdf",
                                    mime="application/pdf",
                                    key=f"real_dl_{year}"
                                )
                            st.success(f"Generated!")
            else:
                 st.info("Previous Year Board Papers are only available for Class 12.")

    with tab3:
        st.subheader("🤖 Curriculum Assistant")
        st.info(f"Chat about **{selected_chapter_name}**. Ask for definitions, key formulas, or study tips!")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input
        if prompt := st.chat_input("Ask a doubt..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Simple Logic Response (Direct Answers)
            response = ""
            prompt_lower = prompt.lower()
            
            if "formula" in prompt_lower:
                response = f"**Key Formulas for {selected_chapter_name}**:\n\n1. **Fundamental Equation**: $E = mc^2$ (Example)\n2. **Rate Law**: $Rate = k[A]^x[B]^y$\n3. **General Config**: $\\int f(x) dx$\n\n(These are generic examples. For specific formulas, please check your textbook or the dedicated chapter PDF.)"
            elif "def" in prompt_lower or "what is" in prompt_lower:
                response = f"**Definition**:\n\nIn the context of **{selected_chapter_name}**, this concept usually refers to the fundamental property or process that defines the system's behavior. For example, if you asked about 'Flux', it is the total field passing through a surface."
            elif "important" in prompt_lower:
                response = f"**Important Topics for Board Exams**:\n\n1. Derivation of principal formulas.\n2. Numerical problems on efficiency and rates.\n3. Diagrammatic representation of processes.\n4. Real-world applications and reasoning questions."
            elif "solve" in prompt_lower or "problem" in prompt_lower:
                response = "**Solution Approach**:\n\n1. Identify the given values.\n2. Choose the correct formula (e.g., Newton's Laws, Thermodynamics First Law).\n3. Substitute values and calculate.\n4. Ensure units are consistent (SI units)."
            else:
                response = f"Regarding **{selected_chapter_name}**: The core concept involves understanding the interaction between components. If you have a specific question about a derivation or definition, ask me directly!"
            
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

else:
    # Empty State
    st.markdown("""
    <div style="text-align:center; padding: 50px; opacity: 0.6;">
        <h2>👈 Select a Chapter to Begin</h2>
        <p>Choose your Subject and Class from the sidebar to access curated content.</p>
    </div>
    """, unsafe_allow_html=True)
