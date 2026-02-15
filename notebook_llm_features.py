"""
NotebookLM-Style AI Features for CBSE Tutor App

This module provides advanced AI-powered study tools including:
- Multi-format question generation (MCQ, True/False, Short Answer, Long Answer)
- AI audio summaries and podcast-style conversations
- Study guide generation
- Document-based Q&A extraction
"""

import os
import json
import time
from datetime import datetime
from typing import List, Dict, Optional, Literal
import google.generativeai as genai
from gtts import gTTS
import pypdf

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Constants
AUDIO_DIR = "audio_summaries"
CACHE_FILE = "audio_cache.json"
STUDY_GUIDES_DIR = "study_guides"

# Ensure directories exist
for directory in [AUDIO_DIR, os.path.join(AUDIO_DIR, "chapter_summaries"), 
                  os.path.join(AUDIO_DIR, "podcasts"), STUDY_GUIDES_DIR]:
    os.makedirs(directory, exist_ok=True)


def _get_gemini_model():
    """Get configured Gemini model instance"""
    return genai.GenerativeModel('models/gemini-flash-latest')


def generate_multi_format_questions(
    chapter: str,
    subject: str,
    question_types: List[Literal["MCQ", "True/False", "Short Answer", "Long Answer"]],
    count: int = 10,
    difficulty: Optional[str] = None
) -> List[Dict]:
    """
    Generate questions in multiple formats using AI.
    
    Args:
        chapter: Chapter name
        subject: Subject name
        question_types: List of question types to generate
        count: Total number of questions
        difficulty: Optional difficulty level (Easy/Medium/Hard)
    
    Returns:
        List of question dictionaries
    """
    if not GEMINI_API_KEY:
        return _generate_fallback_questions(chapter, subject, question_types, count)
    
    try:
        model = _get_gemini_model()
        
        # Build prompt with strong uniqueness requirements
        types_str = ", ".join(question_types)
        difficulty_str = f"Difficulty: {difficulty}. " if difficulty else "Mix difficulty levels (Easy, Medium, Hard). "
        
        prompt = f"""You are creating a CBSE {subject} exam for Class {class_num} on chapter: "{chapter}".

Generate EXACTLY {count} UNIQUE multiple-choice questions. 

CRITICAL REQUIREMENTS:
1. Each question MUST be completely different - NO repetition
2. Cover DIFFERENT concepts/topics from the chapter
3. Ask about: formulas, definitions, applications, numericals, theory, real-world examples
4. {difficulty_str}
5. Make questions exam-relevant and challenging

QUESTION TOPICS TO COVER (pick {count} different ones):
- Fundamental concepts and definitions
- Mathematical formulas and their applications
- Problem-solving and numerical questions
- Conceptual understanding 
- Real-world applications
- Comparison between related concepts
- Cause and effect relationships
- Graphical interpretations
- Common misconceptions
- Previous year exam patterns

Format as JSON array with this EXACT structure:
[
  {{
    "type": "MCQ",
    "question": "Clear, specific question text (different for each)",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 0,
    "explanation": "Why this answer is correct",
    "difficulty": "Easy|Medium|Hard"
  }}
]

IMPORTANT: 
- Return ONLY valid JSON, no other text
- Ensure all {count} questions are COMPLETELY DIFFERENT
- Each question should test a DIFFERENT aspect of the chapter
- Make options plausible and educational"""

        response = model.generate_content(prompt)
        
        # Parse JSON response
        try:
            response_text = response.text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:].strip()
            
            questions = json.loads(response_text)
            
            # CRITICAL: Deduplicate questions
            seen_questions = set()
            unique_questions = []
            
            for idx, q in enumerate(questions):
                # Normalize question text for comparison
                q_normalized = q['question'].lower().strip()
                
                if q_normalized not in seen_questions:
                    q["id"] = len(unique_questions) + 1
                    if "difficulty" not in q:
                        q["difficulty"] = difficulty or "Medium"
                    unique_questions.append(q)
                    seen_questions.add(q_normalized)
            
            # If we got duplicates, retry once with stronger prompt
            if len(unique_questions) < count * 0.8:  # Less than 80% unique
                print(f"Warning: Only got {len(unique_questions)} unique questions, retrying...")
                # Regenerate with even stronger prompt
                retry_prompt = prompt + f"\n\nWARNING: Previous attempt had duplicates. Generate {count} COMPLETELY DIFFERENT questions!"
                response = model.generate_content(retry_prompt)
                response_text = response.text.strip()
                if response_text.startswith("```"):
                    response_text = response_text.split("```")[1]
                    if response_text.startswith("json"):
                        response_text = response_text[4:].strip()
                questions = json.loads(response_text)
                
                # Deduplicate again
                seen_questions = set()
                unique_questions = []
                for q in questions:
                    q_normalized = q['question'].lower().strip()
                    if q_normalized not in seen_questions:
                        q["id"] = len(unique_questions) + 1
                        if "difficulty" not in q:
                            q["difficulty"] = difficulty or "Medium"
                        unique_questions.append(q)
                        seen_questions.add(q_normalized)
            
            return unique_questions[:count]  # Return exactly requested count
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse AI response as JSON: {response.text[:200]}")
            print(f"JSON Error: {e}")
            return _generate_fallback_questions(chapter, subject, question_types, count)
    
    except Exception as e:
        print(f"Error generating questions with AI: {e}")
        return _generate_fallback_questions(chapter, subject, question_types, count)


def _generate_fallback_questions(chapter, subject, question_types, count):
    """Fallback question generation when AI is unavailable - creates diverse questions"""
    questions = []
    
    # More intelligent fallback templates based on subject
    templates = {
        "MCQ": [
            {
                "question": f"Which of the following best describes the main concept of {chapter}?",
                "options": ["Fundamental laws and principles", "Historical development only", "Mathematical derivations", "Practical applications"],
                "correct": 0,
                "explanation": "This chapter focuses on fundamental laws and principles."
            },
            {
                "question": f"What is the primary application of concepts learned in {chapter}?",
                "options": ["Real-world problem solving", "Theoretical understanding", "Mathematical proofs", "Historical context"],
                "correct": 0,
                "explanation": "The concepts are widely used in practical problem-solving."
            },
            {
                "question": f"In {subject}, {chapter} is important because:",
                "options": ["It builds foundation for advanced topics", "It's part of syllabus", "It has easy numericals", "It's scoring in exams"],
                "correct": 0,
                "explanation": "This chapter provides foundational knowledge."
            }
        ],
        "True/False": [
            {
                "question": f"{chapter} involves understanding both theoretical and practical aspects.",
                "correct": True,
                "explanation": "Most CBSE chapters balance theory with application."
            },
            {
                "question": f"The concepts in {chapter} are only applicable in advanced studies.",
                "correct": False,
                "explanation": "These concepts have real-world applications at all levels."
            }
        ],
        "Short Answer": [
            {
                "question": f"State the key principle discussed in {chapter}.",
                "answer": f"The key principle in {chapter} relates to fundamental concepts that govern the behavior and interactions studied in {subject}. It forms the basis for understanding more complex phenomena.",
                "explanation": "Focus on clear, concise explanation of the main idea."
            },
            {
                "question": f"Give an example of real-world application of {chapter}.",
                "answer": f"Concepts from {chapter} are applied in modern technology, engineering solutions, and everyday observations in nature and daily life.",
                "explanation": "Relating concepts to real life strengthens understanding."
            }
        ],
        "Long Answer": [
            {
                "question": f"Explain the importance and key concepts of {chapter} in {subject}.",
                "answer": f"{chapter} is crucial in {subject} as it establishes foundational understanding. Key concepts include: 1) Basic definitions and terminology essential for the topic, 2) Mathematical or theoretical framework that explains observed phenomena, 3) Practical applications demonstrating real-world relevance, 4) Connections to other chapters and advanced topics. Understanding these concepts thoroughly helps in solving complex problems and developing deeper insights into {subject}.",
                "explanation": "Comprehensive answers should cover significance, key points, and applications."
            }
        ]
    }
    
    # Distribute questions across types with variety
    per_type = max(1, count // len(question_types))
    
    for qtype in question_types:
        template_set = templates.get(qtype, templates["MCQ"])
        
        # Use multiple templates if available
        for i in range(min(per_type, len(template_set))):
            if len(questions) >= count:
                break
            
            q = template_set[i % len(template_set)].copy()
            q["type"] = qtype
            q["id"] = len(questions) + 1
            q["difficulty"] = "Medium"
            questions.append(q)
    
    # Fill remaining with MCQs if needed
    while len(questions) < count:
        q = templates["MCQ"][len(questions) % len(templates["MCQ"])].copy()
        q["type"] = "MCQ"
        q["id"] = len(questions) + 1
        q["difficulty"] = "Medium"
        questions.append(q)
    
    return questions[:count]


def generate_chapter_summary_audio(
    chapter: str,
    subject: str,
    class_num: int,
    force_regenerate: bool = False
) -> Optional[str]:
    """
    Generate AI-narrated audio summary of a chapter.
    
    Args:
        chapter: Chapter name
        subject: Subject name
        class_num: Class number
        force_regenerate: Force regeneration even if cached
    
    Returns:
        Path to audio file or None if failed
    """
    # Check cache
    cache_key = f"{subject}_{chapter}_summary".replace(" ", "_").lower()
    audio_path = os.path.join(AUDIO_DIR, "chapter_summaries", f"{cache_key}.mp3")
    
    if not force_regenerate and os.path.exists(audio_path):
        print(f"Using cached audio: {audio_path}")
        return audio_path
    
    try:
        # Generate summary text using AI
        if GEMINI_API_KEY:
            model = _get_gemini_model()
            prompt = f"""You are an expert CBSE {subject} tutor. Create a detailed, chapter-specific 2-3 minute audio lecture script for Class {class_num} chapter: "{chapter}".

REQUIREMENTS:
- Start with: "Welcome! Today we're exploring {chapter}, a key chapter in Class {class_num} {subject}."
- Explain the MAIN CONCEPT in simple terms with an example
- List 3-4 SPECIFIC key points/subtopics from THIS chapter
- Mention 2-3 IMPORTANT formulas/laws/definitions specific to this chapter
- Give 1-2 REAL-WORLD applications or examples
- End with an exam tip specific to this chapter

Be SPECIFIC to this chapter - don't give generic advice. Use concrete examples.
Write as a spoken narration (use "we", "you", "let's").
Maximum 400 words."""

            response = model.generate_content(prompt)
            summary_text = response.text.strip()
        else:
            # Fallback summary
            summary_text = f"""Welcome! Today we're exploring {chapter} from Class {class_num} {subject}. 
            
This chapter introduces fundamental concepts that build the foundation for advanced topics. The main focus is on understanding the core principles and their applications.

Key points to remember: First, grasp the basic definitions and terminology. Second, understand how these concepts apply in solving problems. Third, practice numerical questions to strengthen your understanding.

For exams, focus on the derivations, important diagrams, and previous year question patterns for this chapter.

Practice regularly and you'll master this! All the best!"""
        
        # Convert to speech
        tts = gTTS(text=summary_text, lang='en', slow=False)
        tts.save(audio_path)
        
        # Update cache
        _update_audio_cache(chapter, subject, "summary", audio_path)
        
        return audio_path
    
    except Exception as e:
        print(f"Error generating audio summary: {e}")
        return None


def generate_podcast_conversation(
    chapter: str,
    subject: str,
    class_num: int,
    force_regenerate: bool = False
) -> Optional[str]:
    """
    Generate podcast-style conversation between two AI hosts discussing the chapter.
    
    Args:
        chapter: Chapter name
        subject: Subject name
        class_num: Class number
        force_regenerate: Force regeneration even if cached
    
    Returns:
        Path to audio file or None if failed
    """
    cache_key = f"{subject}_{chapter}_podcast".replace(" ", "_").lower()
    audio_path = os.path.join(AUDIO_DIR, "podcasts", f"{cache_key}.mp3")
    
    if not force_regenerate and os.path.exists(audio_path):
        return audio_path
    
    try:
        if GEMINI_API_KEY:
            model = _get_gemini_model()
            prompt = f"""Create a podcast-style conversation script between two hosts discussing CBSE Class {class_num} {subject}: "{chapter}".

Host 1 (Teacher): Explains concepts clearly
Host 2 (Student/Curious Learner): Asks questions, seeks clarifications

Format:
Host 1: [Introduction and overview]
Host 2: [Curious question about the topic]
Host 1: [Detailed explanation]
Host 2: [Follow-up or real-world application question]
... (continue for 3-4 exchanges)

Make it conversational, engaging, and educational. Include:
- Key concepts explained simply
- Common student doubts addressed
- Exam tips
- Real-world connections

Maximum 600 words. Use natural dialogue."""

            response = model.generate_content(prompt)
            conversation_text = response.text.strip()
        else:
            conversation_text = f"""Host 1: Welcome! Today we're diving into {chapter}, a fascinating topic in {subject}.

Host 2: I'm really excited about this! So what's the main idea here?

Host 1: Great question! The core concept revolves around understanding how these principles apply in real scenarios. Think of it as the foundation for more advanced topics.

Host 2: That makes sense! Any tips for remembering this for exams?

Host 1: Absolutely! Focus on understanding the underlying concepts rather than rote learning. Practice problems and visualize the concepts. That's the key to success!"""
        
        # For podcast, we'll use simple TTS (in production, could use multiple voices)
        tts = gTTS(text=conversation_text, lang='en', slow=False)
        tts.save(audio_path)
        
        _update_audio_cache(chapter, subject, "podcast", audio_path)
        
        return audio_path
    
    except Exception as e:
        print(f"Error generating podcast: {e}")
        return None


def generate_study_guide(
    chapter: str,
    subject: str,
    class_num: int,
    template_type: Literal["bullet_points", "detailed_notes", "flashcard_format"] = "bullet_points"
) -> str:
    """
    Generate comprehensive study guide in markdown format.
    
    Args:
        chapter: Chapter name
        subject: Subject name
        class_num: Class number
        template_type: Type of study guide
    
    Returns:
        Markdown formatted study guide text
    """
    if not GEMINI_API_KEY:
        return _generate_fallback_study_guide(chapter, subject, template_type)
    
    try:
        model = _get_gemini_model()
        
        if template_type == "bullet_points":
            format_instructions = """Use bullet points and sub-bullets. Structure:
- Main Topic 1
  - Subtopic
  - Key point
- Main Topic 2
  ..."""
        elif template_type == "detailed_notes":
            format_instructions = """Use detailed paragraphs with headings. Include:
## Introduction
## Key Concepts
## Important Formulas/Laws
## Applications
## Summary"""
        else:  # flashcard_format
            format_instructions = """Create Q&A flashcard style:
**Q: [Question]**
A: [Concise answer]

(Repeat for 10-15 flashcards)"""
        
        prompt = f"""Create a comprehensive study guide for CBSE Class {class_num} {subject} chapter: "{chapter}".

Format: {format_instructions}

Include:
- All key concepts and definitions
- Important formulas, laws, or theorems (if applicable)
- Diagrams descriptions (describe what should be drawn)
- Common mistakes to avoid
- Quick revision points
- 2-3 practice questions

Make it thorough but concise, suitable for exam preparation. Use markdown formatting."""

        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"Error generating study guide: {e}")
        return _generate_fallback_study_guide(chapter, subject, template_type)


def _generate_fallback_study_guide(chapter, subject, template_type):
    """Fallback study guide when AI is unavailable"""
    if template_type == "bullet_points":
        return f"""# Study Guide: {chapter}

## Key Concepts
- Fundamental principle of the chapter
  - Core definition
  - Mathematical representation
- Applications in real world
  - Example 1
  - Example 2

## Important Points
- Remember the basic laws
- Understand the derivations
- Practice numerical problems

## Quick Revision
- Focus on formulas
- Review diagrams
- Solve previous year questions"""
    
    elif template_type == "detailed_notes":
        return f"""# {chapter} - Detailed Study Notes

## Introduction
This chapter covers the fundamental aspects of {subject}. Understanding these concepts is crucial for both theoretical knowledge and practical applications.

## Key Concepts
The main concepts include the governing principles, their mathematical formulations, and how they manifest in observable phenomena.

## Important Formulas
Review all derivations and practice applying formulas to different scenarios.

## Applications
These concepts are widely used in technology, engineering, and daily life observations.

## Summary
Focus on understanding rather than memorization. Practice regularly and connect concepts."""
    
    else:  # flashcard_format
        return f"""# {chapter} - Study Flashcards

**Q: What is the main principle of {chapter}?**
A: The fundamental principle governing the behavior and interactions studied in this chapter.

**Q: Name one important formula.**
A: [Refer to your textbook for specific formulas]

**Q: Give a real-world application.**
A: The concepts are applied in modern technology and engineering solutions.

**Q: What is a common mistake to avoid?**
A: Not understanding the underlying concepts and relying solely on memorization."""


def extract_qa_from_document(
    pdf_path: str,
    chapter_query: str,
    num_questions: int = 10
) -> List[Dict]:
    """
    Extract Q&A pairs from PDF textbook using AI.
    
    Args:
        pdf_path: Path to PDF file
        chapter_query: Chapter name or topic to focus on
        num_questions: Number of Q&A pairs to extract
    
    Returns:
        List of Q&A dictionaries
    """
    try:
        # Extract text from PDF
        reader = pypdf.PdfReader(pdf_path)
        text_content = ""
        for page in reader.pages[:20]:  # Limit to first 20 pages
            text_content += page.extract_text() + "\n"
        
        if len(text_content) < 100:
            return []
        
        # Use AI to extract Q&A
        if GEMINI_API_KEY:
            model = _get_gemini_model()
            prompt = f"""From the following textbook content about "{chapter_query}", extract {num_questions} important questions and their answers.

Textbook Content:
{text_content[:4000]}  

Generate questions that:
1. Cover key concepts
2. Are exam-relevant
3. Have clear, concise answers

Format as JSON:
[
  {{
    "question": "...",
    "answer": "...",
    "type": "Short Answer" or "Long Answer"
  }}
]

Return ONLY valid JSON."""

            response = model.generate_content(prompt)
            
            # Parse response
            response_text = response.text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:].strip()
            
            qa_pairs = json.loads(response_text)
            
            # Add IDs
            for idx, qa in enumerate(qa_pairs):
                qa["id"] = idx + 1
                qa["source"] = "document"
            
            return qa_pairs
        
        return []
    
    except Exception as e:
        print(f"Error extracting Q&A from document: {e}")
        return []


def _update_audio_cache(chapter: str, subject: str, audio_type: str, filepath: str):
    """Update audio cache file"""
    try:
        # Load existing cache
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
        else:
            cache_data = {"cache": []}
       
        # Add new entry
        cache_data["cache"].append({
            "chapter": chapter,
            "subject": subject,
            "type": audio_type,
            "filename": filepath,
            "generated_at": datetime.now().isoformat(),
            "duration_seconds": 0  # Would need audio library to calculate
        })
        
        # Save
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f, indent=2)
    
    except Exception as e:
        print(f"Error updating cache: {e}")


def get_audio_cache_info(chapter: str, subject: str, audio_type: str) -> Optional[Dict]:
    """Get cached audio information"""
    try:
        if not os.path.exists(CACHE_FILE):
            return None
        
        with open(CACHE_FILE, 'r') as f:
            cache_data = json.load(f)
        
        for entry in cache_data.get("cache", []):
            if (entry["chapter"] == chapter and 
                entry["subject"] == subject and 
                entry["type"] == audio_type):
                return entry
        
        return None
    except:
        return None
