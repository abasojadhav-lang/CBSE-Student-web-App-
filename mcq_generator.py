import json
import os
import random
from datetime import datetime

MCQ_DATA_FILE = "mcq_data.json"
RESULTS_FILE = "test_results.json"

def init_mcq_database():
    """Initialize MCQ database - now uses pre-generated mcq_data.json"""
    if not os.path.exists(MCQ_DATA_FILE):
        print(f"ERROR: {MCQ_DATA_FILE} not found!")
        print("Please run: python generate_complete_mcqs.py")
        return False
    return True

def get_chapter_mcqs(subject, chapter, count=10):
    """Get MCQs for a specific chapter"""
    if not init_mcq_database():
        return []
    
    try:
        with open(MCQ_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        mcqs = data.get("mcqs", {}).get(subject, {}).get(chapter, [])
        
        if len(mcqs) > count:
            return random.sample(mcqs, count)
        return mcqs
    except Exception as e:
        print(f"Error loading MCQs: {e}")
        return []

def get_mock_test_mcqs(subject, count=30):
    """Get MCQs from multiple chapters for mock test"""
    if not init_mcq_database():
        return []
    
    try:
        with open(MCQ_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        all_mcqs = []
        subject_data = data.get("mcqs", {}).get(subject, {})
        
        for chapter, mcqs in subject_data.items():
            all_mcqs.extend(mcqs)
        
        if len(all_mcqs) > count:
            return random.sample(all_mcqs, count)
        return all_mcqs
    except Exception as e:
        print(f"Error loading MCQs: {e}")
        return []

def save_test_result(student_name, test_type, subject, chapter, score, total, time_taken, answers):
    """Save test result to file"""
    result = {
        "id": f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "student_name": student_name,
        "test_type": test_type,
        "subject": subject,
        "chapter": chapter,
        "score": score,
        "total": total,
        "percentage": round((score/total)*100, 2),
        "time_taken": time_taken,
        "answers": answers
    }
    
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"results": []}
    
    data["results"].append(result)
    
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return result["id"]

def get_all_test_results():
    """Get all test results"""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("results", [])
    return []

def get_recent_results(limit=5):
    """Get recent test results"""
    all_results = get_all_test_results()
    return list(reversed(all_results))[:limit]
