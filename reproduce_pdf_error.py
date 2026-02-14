from pdf_generator import generate_markdown_to_pdf
import os

def reproduce_issue():
    # Simulate content
    content = "# इतिहास प्रश्नपेढी\nOnly English here for test."
    filename = "History_Question_Bank.md"
    is_marath = True
    
    print("Running reproduction...")
    generate_markdown_to_pdf(content, filename, is_marath)
    
    if os.path.exists("pdf_debug.log"):
        print("\n--- Log Content ---")
        with open("pdf_debug.log", "r") as f:
            print(f.read())
    else:
        print("No log file created.")

if __name__ == "__main__":
    reproduce_issue()
