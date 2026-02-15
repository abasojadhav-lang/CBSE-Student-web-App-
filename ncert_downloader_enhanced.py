"""
Enhanced NCERT PDF Downloader
Downloads chapter-wise PDFs from ncert.nic.in with proper naming based on chapter titles
"""

import os
import requests
import time
import urllib3
from typing import List, Dict, Optional
from data import ALL_CHAPTERS

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# NCERT Book Codes Mapping
# Format: {(class, subject): [(part_number, book_code, chapter_range)]}
NCERT_BOOK_CODES = {
    # Class 11
    (11, 'Physics'): [(1, 'keph1', range(1, 9)), (2, 'keph2', range(9, 16))],
    (11, 'Chemistry'): [(1, 'kech1', range(1, 8)), (2, 'kech2', range(8, 15))],
    (11, 'Biology'): [(1, 'kebo1', range(1, 12)), (2, 'kebo2', range(12, 23))],
    (11, 'Mathematics'): [(1, 'kemh1', range(1, 17))],
    
    # Class 12
    (12, 'Physics'): [(1, 'leph1', range(1, 9)), (2, 'leph2', range(9, 16))],
    (12, 'Chemistry'): [(1, 'lech1', range(1, 9)), (2, 'lech2', range(9, 17))],
    (12, 'Biology'): [(1, 'lebo1', range(1, 9)), (2, 'lebo2', range(9, 17))],
    (12, 'Mathematics'): [(1, 'lemh1', range(1, 14))],
}


def get_chapter_info_by_number(class_num: int, subject: str, chapter_num: int) -> Optional[Dict]:
    """Get chapter information from data.py by class, subject, and chapter number"""
    chapters = [ch for ch in ALL_CHAPTERS 
                if ch['class'] == class_num 
                and ch['subject'] == subject
                and ch.get('board', 'CBSE') == 'CBSE']
    
    if 0 < chapter_num <= len(chapters):
        return chapters[chapter_num - 1]
    return None


def download_ncert_chapter(class_num: int, subject: str, chapter_num: int, 
                           output_dir: str = "books", verbose: bool = True) -> Optional[str]:
    """
    Download a specific NCERT chapter PDF
    
    Args:
        class_num: Class number (11 or 12)
        subject: Subject name (Physics, Chemistry, Biology, Mathematics)
        chapter_num: Chapter number (1-based)
        output_dir: Output directory for downloads
        verbose: Print status messages
    
    Returns:
        Path to downloaded file or None if failed
    """
    # Get book codes for this class and subject
    book_info = NCERT_BOOK_CODES.get((class_num, subject))
    if not book_info:
        if verbose:
            print(f"No NCERT book code found for Class {class_num} {subject}")
        return None
    
    # Find which part this chapter belongs to
    book_code = None
    actual_chapter_num = None
    
    for part_num, code, ch_range in book_info:
        if chapter_num in ch_range:
            book_code = code
            # For part 2, chapters might need offset
            if part_num == 2:
                # Some books use 201-208 for part 2, others use 109-115
                # Try both patterns
                actual_chapter_num = chapter_num
            else:
                actual_chapter_num = chapter_num
            break
    
    if not book_code:
        if verbose:
            print(f"Chapter {chapter_num} not in valid range for {subject}")
        return None
    
    # Get chapter metadata from data.py for nice naming
    chapter_info = get_chapter_info_by_number(class_num, subject, chapter_num)
    chapter_name = chapter_info['name'] if chapter_info else f"Chapter {chapter_num}"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename with chapter name
    safe_name = "".join([c if c.isalnum() or c in (' ', '-') else '_' for c in chapter_name])
    filename = f"{subject}_Class{class_num}_Ch{chapter_num:02d}_{safe_name}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    # Check if already exists
    if os.path.exists(filepath):
        if verbose:
            print(f"[o] Already exists: {filename}")
        return filepath
    
    # Setup session with headers
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://ncert.nic.in/textbook.php",
        "Connection": "keep-alive"
    }
    session.headers.update(headers)
    
    # Try multiple URL patterns
    url_patterns = [
        f"https://ncert.nic.in/textbook/pdf/{book_code}{100+actual_chapter_num}.pdf",  # Pattern: leph101, leph102...
        f"https://ncert.nic.in/textbook/pdf/{book_code}{200+actual_chapter_num}.pdf",  # Pattern: leph201 for part 2
        f"https://ncert.nic.in/textbook/pdf/{book_code}{actual_chapter_num:02d}.pdf",    # Pattern: leph01, leph02...
    ]
    
    for url in url_patterns:
        try:
            if verbose:
                print(f"-> Trying: {os.path.basename(url)}")
            
            # Try to download
            response = session.get(url, timeout=30, verify=False)
            
            if response.status_code == 200 and len(response.content) > 10000:  # Must be > 10KB to be valid
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                if verbose:
                    size_mb = len(response.content) / (1024 * 1024)
                    print(f"[+] Downloaded: {filename} ({size_mb:.2f} MB)")
                
                return filepath
        
        except Exception as e:
            if verbose:
                print(f"  Failed: {e}")
            continue
    
    if verbose:
        print(f"[-] Could not download: {chapter_name}")
    return None


def download_all_ncert_books(classes: List[int] = [11, 12], 
                             subjects: List[str] = ['Physics', 'Chemistry', 'Biology', 'Mathematics'],
                             output_dir: str = "books") -> Dict[str, int]:
    """
    Download all NCERT textbooks chapter-wise
    
    Returns:
        Dictionary with download statistics
    """
    stats = {
        'total_attempted': 0,
        'successful': 0,
        'failed': 0,
        'skipped': 0
    }
    
    print("=" * 60)
    print("NCERT Chapter-wise PDF Downloader")
    print("=" * 60)
    print()
    
    for class_num in classes:
        for subject in subjects:
            print(f"\n[*] {subject} - Class {class_num}")
            print("-" * 40)
            
            # Get chapter count for this subject/class
            chapters = [ch for ch in ALL_CHAPTERS 
                       if ch['class'] == class_num 
                       and ch['subject'] == subject
                       and ch.get('board', 'CBSE') == 'CBSE']
            
            for idx, chapter in enumerate(chapters, 1):
                stats['total_attempted'] += 1
                
                result = download_ncert_chapter(class_num, subject, idx, output_dir)
                
                if result:
                    if "Already exists" in str(result):
                        stats['skipped'] += 1
                    else:
                        stats['successful'] += 1
                else:
                    stats['failed'] += 1
                
                time.sleep(0.5)  # Be respectful to server
    
    # Print summary
    print("\n" + "=" * 60)
    print("Download Complete!")
    print("=" * 60)
    print(f"Total Attempted: {stats['total_attempted']}")
    print(f"[+] Successful:    {stats['successful']}")
    print(f"[o] Skipped:       {stats['skipped']}")
    print(f"[-] Failed:        {stats['failed']}")
    print()
    
    return stats


def download_by_chapter_list(chapter_names: List[str], class_num: int, subject: str, 
                             output_dir: str = "books") -> List[str]:
    """
    Download specific chapters by name
    
    Args:
        chapter_names: List of chapter names to download
        class_num: Class number
        subject: Subject name
        output_dir: Output directory
    
    Returns:
        List of successfully downloaded file paths
    """
    downloaded = []
    
    # Get all chapters for this subject/class
    all_chapters = [ch for ch in ALL_CHAPTERS 
                   if ch['class'] == class_num 
                   and ch['subject'] == subject
                   and ch.get('board', 'CBSE') == 'CBSE']
    
    for chapter_name in chapter_names:
        # Find chapter number by name
        for idx, ch in enumerate(all_chapters, 1):
            if ch['name'].lower() == chapter_name.lower():
                result = download_ncert_chapter(class_num, subject, idx, output_dir)
                if result:
                    downloaded.append(result)
                break
    
    return downloaded


if __name__ == "__main__":
    # Example: Download all books
    stats = download_all_ncert_books()
    
    # Example: Download specific chapters
    # download_by_chapter_list(
    #     ["Electric Charges and Fields", "Current Electricity"],
    #     class_num=12,
    #     subject="Physics"
    # )
