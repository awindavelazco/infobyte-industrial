import google.generativeai as genai
import json

def test_model(model_name, keys):
    print(f"--- TESTING MODEL: {model_name} ---")
    for i, key in enumerate(keys):
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hi")
            print(f"Key #{i+1}: ✅ SUCCESS")
            return True # Stop at first success
        except Exception as e:
            print(f"Key #{i+1}: ❌ FAILED - {e}")
    return False

with open('api_keys.json', 'r') as f:
    keys_data = json.load(f)

all_keys = keys_data['news_keys'] + keys_data['video_keys']
models_to_test = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash-exp']

for model in models_to_test:
    if test_model(model, all_keys):
        print(f"\n🎉 FOUND WORKING MODEL: {model}")
        break
else:
    print("\n🚨 ALL MODELS FAILED FOR ALL KEYS.")
