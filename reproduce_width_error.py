from pdf_generator import generate_markdown_to_pdf
import os

def reproduction():
    try:
        with open("question_bank/History_Question_Bank.md", "r", encoding="utf-8") as f:
            content = f.read()
            
        # We need to monkey patch or modify pdf_generator to print lines
        # Or just read file and call the function, but since the function loops internally...
        # Let's modify pdf_generator.py to print the line before processing
        print("Modifying pdf_generator.py for debugging...")
        generate_markdown_to_pdf(content, "History_Question_Bank.md", is_marathi=True)
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reproduction()
