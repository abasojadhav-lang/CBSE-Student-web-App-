from utils import search_videos

print("Testing Video Search for 'Structure of Atom' (Chemistry)...")
videos = search_videos("Structure of Atom", "Chemistry")

if not videos:
    print("FAILED: No videos found.")
else:
    print(f"SUCCESS: Found {len(videos)} videos.")
    for v in videos:
        print(f"- [{v['duration']}] {v['title']} ({v['channel']})")
