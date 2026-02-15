"""
Interactive AI Chat Module - FIXED with working model
Provides conversational AI assistant for chapter-specific Q&A
"""

import os
import streamlit as st
import google.generativeai as genai
from typing import List, Dict, Optional

# Configure Gemini API - Support both local and Streamlit Cloud
try:
    # First try Streamlit secrets (for cloud deployment)
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    # Fallback to environment variable (for local development)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class ChapterChatbot:
    """Interactive chatbot for chapter-specific questions"""
    
    def __init__(self, chapter: str, subject: str, class_num: int):
        self.chapter = chapter
        self.subject = subject
        self.class_num = class_num
        self.chat_history: List[Dict[str, str]] = []
        
        # Initialize AI model with context
        if GEMINI_API_KEY:
            try:
                # Use confirmed working model from API
                self.model = genai.GenerativeModel('models/gemini-flash-latest')
            except:
                self.model = None
            
            # System context
            self.system_context = f"""You are an expert CBSE {subject} tutor helping a Class {class_num} student with the chapter: "{chapter}".

YOUR ROLE:
- Answer questions SPECIFICALLY about this chapter
- Explain concepts clearly with examples
- Provide step-by-step solutions for problems
- Give exam-focused tips and shortcuts
- Correct misconceptions patiently

GUIDELINES:
- Keep responses concise (2-3 paragraphs max)
- Use simple language
- Give examples from the NCERT textbook when possible
- If asked about formulas, explain when and how to use them
- If student seems confused, break down the concept further

Stay focused on "{chapter}" - if asked about other chapters, gently redirect to this topic.
"""
        else:
            self.model = None
    
    def ask(self, question: str) -> str:
        """
        Ask a question to the AI tutor (Non-streaming)
        """
        if not self.model:
            return "⚠️ AI Chat requires GEMINI_API_KEY to be set. Please configure your API key."
        
        try:
            # Build conversation (same as before)
            conversation = self._build_prompt(question)
            
            # Generate response
            response = self.model.generate_content(conversation)
            answer = response.text.strip()
            
            # Save to history
            self.chat_history.append({'question': question, 'answer': answer})
            return answer
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

    def ask_stream(self, question: str):
        """
        Ask a question and stream the response
        Yields chunks of text as they are generated
        """
        if not self.model:
            yield "⚠️ AI Chat requires GEMINI_API_KEY to be set."
            return

        try:
            conversation = self._build_prompt(question)
            response = self.model.generate_content(conversation, stream=True)
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    text_chunk = chunk.text
                    full_response += text_chunk
                    yield text_chunk
            
            # Save to history after complete
            self.chat_history.append({'question': question, 'answer': full_response})
            
        except Exception as e:
            yield f"⚠️ Error: {str(e)}"

    def _build_prompt(self, question: str) -> str:
        """Helper to build the conversation prompt"""
        prompt = f"{self.system_context}\n\n"
        for msg in self.chat_history[-5:]:
            prompt += f"Student: {msg['question']}\n"
            prompt += f"Tutor: {msg['answer']}\n\n"
        prompt += f"Student: {question}\nTutor: "
        return prompt
    
    def get_suggested_questions(self) -> List[str]:
        """Get suggested starter questions for this chapter"""
        return [
            f"What is the main concept of {self.chapter}?",
            "Explain the key formula and how to use it",
            "Give me an example problem with solution",
            "What are common mistakes students make?",
            "What should I focus on for exams?",
            "Explain this concept in simpler terms"
        ]
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get chat history"""
        return self.chat_history


def create_chatbot(chapter: str, subject: str, class_num: int) -> ChapterChatbot:
    """Factory function to create a chatbot instance"""
    return ChapterChatbot(chapter, subject, class_num)
