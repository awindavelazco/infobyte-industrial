import google.generativeai as genai
import json

def test_model_2_5(keys):
    model_name = 'gemini-2.5-flash'
    print(f"--- TESTING MODEL: {model_name} ---")
    for i, key in enumerate(keys):
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hi, are you active?")
            print(f"Key #{i+1}: SUCCESS! Response: {response.text[:50]}...")
            return True
        except Exception as e:
            print(f"Key #{i+1}: FAILED - {e}")
    return False

with open('api_keys.json', 'r') as f:
    keys_data = json.load(f)

all_keys = keys_data['news_keys'] + keys_data['video_keys']

if test_model_2_5(all_keys):
    print(f"\nFOUND WORKING MODEL: Gemini 2.5 Flash is working with your keys!")
else:
    print("\nFAILURE: Even Gemini 2.5 Flash failed for all keys.")
