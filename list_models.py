"""List available Gemini models"""
import google.generativeai as genai
import os

os.environ['GEMINI_API_KEY'] = 'AIzaSyD8gBuBcPesTDdKZaQantX4jNFms3G-zk4'
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

print("Available Gemini models:")
print("=" * 50)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Display name: {model.display_name}")
        print(f"   Description: {model.description[:80]}...")
        print()
