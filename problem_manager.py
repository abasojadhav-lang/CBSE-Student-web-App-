import json
import os
from datetime import datetime
import uuid

PROBLEMS_FILE = "problems_data.json"

def load_problems():
    """Load problems from JSON file"""
    if os.path.exists(PROBLEMS_FILE):
        try:
            with open(PROBLEMS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"problems": []}
    return {"problems": []}

def save_problems(data):
    """Save problems to JSON file"""
    with open(PROBLEMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_problem(student_name, subject, chapter, problem_text, contact=""):
    """Add a new problem submission"""
    data = load_problems()
    
    new_problem = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "student_name": student_name,
        "contact": contact,
        "subject": subject,
        "chapter": chapter,
        "problem": problem_text,
        "status": "pending",
        "teacher_response": "",
        "response_timestamp": ""
    }
    
    data["problems"].append(new_problem)
    save_problems(data)
    return new_problem["id"]

def get_all_problems():
    """Get all problems"""
    return load_problems()["problems"]

def get_problems_by_status(status="pending"):
    """Get problems filtered by status"""
    all_problems = get_all_problems()
    return [p for p in all_problems if p["status"] == status]

def get_problems_by_subject_chapter(subject, chapter):
    """Get problems for specific subject and chapter"""
    all_problems = get_all_problems()
    return [p for p in all_problems if p["subject"] == subject and p["chapter"] == chapter]

def add_teacher_response(problem_id, response_text):
    """Add teacher response to a problem"""
    data = load_problems()
    
    for problem in data["problems"]:
        if problem["id"] == problem_id:
            problem["teacher_response"] = response_text
            problem["response_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            problem["status"] = "answered"
            break
    
    save_problems(data)
    return True

def get_problem_by_id(problem_id):
    """Get a specific problem by ID"""
    all_problems = get_all_problems()
    for problem in all_problems:
        if problem["id"] == problem_id:
            return problem
    return None
