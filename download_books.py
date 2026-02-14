import os
import requests
import time
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_ncert_books(class_nums=[11, 12], subjects=['Physics', 'Chemistry', 'Biology', 'Maths']):
    """
    Downloads NCERT books based on standard URL patterns.
    Verified to work with NCERT's current server configuration (requires headers + session).
    """
    
    base_url = "https://ncert.nic.in/textbook/pdf"
    
    # Mapping
    class_map = {11: 'k', 12: 'l'}
    subject_map = {
        'Physics': 'ph',
        'Chemistry': 'ch',
        'Biology': 'bo',
        'Maths': 'mh'
    }
    
    # Ensure directory
    if not os.path.exists("books"):
        os.makedirs("books")
        
    download_log = []
    
    # Setup Session with robust headers
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://ncert.nic.in/textbook.php",
        "Connection": "keep-alive"
    }
    session.headers.update(headers)
    
    # IMPORTANT: Establish session by visiting main page first (handles cookies/redirects)
    try:
        print("Initializing connection to NCERT...")
        session.get("http://ncert.nic.in/textbook.php", timeout=15, verify=False)
    except Exception as e:
        download_log.append(f"Warning: Could not connect to main page: {e}")

    for c_num in class_nums:
        c_code = class_map.get(c_num)
        
        for sub in subjects:
            if sub not in subject_map: continue
            s_code = subject_map[sub]
            
            print(f"Checking {sub} Class {c_num}...")
            
            # Try chapters 1 to 16
            for ch in range(1, 17):
                # Standard patterns
                codes_to_try = [
                    f"{c_code}{s_code}{100+ch}", # e.g., leph101
                    f"{c_code}{s_code}{200+ch}"  # e.g., leph201 (Part 2 specific)
                ]
                
                for file_code in codes_to_try:
                    filename = f"{file_code}.pdf"
                    
                    # Nice readable name for saving
                    save_name = f"{sub}_Class{c_num}_Ch{ch}_{file_code}.pdf"
                    save_path = os.path.join("books", save_name)
                    
                    if os.path.exists(save_path):
                        download_log.append(f"Skipped (Exists): {save_name}")
                        continue
                        
                    url = f"{base_url}/{filename}"
                    
                    try:
                        # Head request first using session
                        r = session.head(url, timeout=10, verify=False)
                        
                        if r.status_code == 200:
                            print(f"Downloading {filename}...")
                            r_get = session.get(url, timeout=30, verify=False)
                            with open(save_path, 'wb') as f:
                                f.write(r_get.content)
                            download_log.append(f"SUCCESS: {save_name}")
                            time.sleep(1) # Be nice to server
                        elif r.status_code == 404:
                             # Expected for non-existent chapters/parts
                             pass
                    except Exception as e:
                        print(f"Error {filename}: {e}")
                        download_log.append(f"Error downloading {filename}: {str(e)}")
                        
    return download_log

if __name__ == "__main__":
    logs = download_ncert_books()
    print("\n".join(logs))
