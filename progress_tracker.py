import json
import os
from datetime import datetime

PROGRESS_FILE = "user_progress.json"

def init_progress():
    """Initialize progress file if it doesn't exist"""
    if not os.path.exists(PROGRESS_FILE):
        default_progress = {
            "user_id": "default",
            "chapters_completed": [],
            "test_history": [],
            "total_time_spent": 0,
            "accuracy_by_chapter": {},
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_progress, f, indent=2)

def get_progress():
    """Get user progress data"""
    init_progress()
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_test_performance(subject, chapter, score, total):
    """Update test performance for a chapter"""
    progress = get_progress()
    
    # Update accuracy by chapter
    key = f"{subject}_{chapter}"
    if key not in progress["accuracy_by_chapter"]:
        progress["accuracy_by_chapter"][key] = {
            "subject": subject,
            "chapter": chapter,
            "tests_taken": 0,
            "total_correct": 0,
            "total_questions": 0,
            "average_accuracy": 0
        }
    
    chapter_data = progress["accuracy_by_chapter"][key]
    chapter_data["tests_taken"] += 1
    chapter_data["total_correct"] += score
    chapter_data["total_questions"] += total
    chapter_data["average_accuracy"] = round(
        (chapter_data["total_correct"] / chapter_data["total_questions"]) * 100, 2
    )
    
    # Mark chapter as completed if accuracy > 70%
    if chapter_data["average_accuracy"] >= 70 and chapter not in progress["chapters_completed"]:
        progress["chapters_completed"].append(chapter)
    
    progress["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)

def add_time_spent(minutes):
    """Add time spent studying"""
    progress = get_progress()
    progress["total_time_spent"] += minutes
    progress["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)

def get_weak_chapters(threshold=60):
    """Get chapters with accuracy below threshold"""
    progress = get_progress()
    weak_chapters = []
    
    for key, data in progress["accuracy_by_chapter"].items():
        if data["average_accuracy"] < threshold and data["tests_taken"] >= 1:
            weak_chapters.append(data)
    
    return sorted(weak_chapters, key=lambda x: x["average_accuracy"])

def get_overall_stats():
    """Get overall statistics"""
    progress = get_progress()
    
    total_tests = sum(
        data["tests_taken"] 
        for data in progress["accuracy_by_chapter"].values()
    )
    
    if total_tests > 0:
        total_correct = sum(
            data["total_correct"] 
            for data in progress["accuracy_by_chapter"].values()
        )
        total_questions = sum(
            data["total_questions"] 
            for data in progress["accuracy_by_chapter"].values()
        )
        overall_accuracy = round((total_correct / total_questions) * 100, 2)
    else:
        overall_accuracy = 0
    
    return {
        "chapters_completed": len(progress["chapters_completed"]),
        "total_tests": total_tests,
        "total_time_spent": progress["total_time_spent"],
        "overall_accuracy": overall_accuracy
    }
