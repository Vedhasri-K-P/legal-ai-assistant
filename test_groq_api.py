"""
Test Groq API Key
"""
import requests
import os
from dotenv import load_dotenv

print("=" * 60)
print("GROQ API KEY TEST")
print("=" * 60)

# Load .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Step 1: Check if API key exists
print("\n[1/3] Checking API key...")
if not api_key:
    print("❌ ERROR: No API key found in .env file!")
    print("\nWhat to do:")
    print("1. Go to: https://console.groq.com/keys")
    print("2. Create a new API key")
    print("3. Add to .env file: GROQ_API_KEY=your_key_here")
    exit()

print(f"✅ API key found: {api_key[:15]}...{api_key[-5:]}")
print(f"   Length: {len(api_key)} characters")

# Step 2: Check API key format
print("\n[2/3] Checking API key format...")
if not api_key.startswith("gsk_"):
    print(f"⚠️  WARNING: Key should start with 'gsk_'")
    print(f"   Your key starts with: {api_key[:4]}")
else:
    print("✅ Format looks correct")

# Step 3: Test API connection
print("\n[3/3] Testing API connection...")

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 20
}

try:
    response = requests.post(url, json=data, headers=headers, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ ✅ ✅ SUCCESS! API is working perfectly!")
        result = response.json()
        print(f"\nAI Response: {result['choices'][0]['message']['content']}")
        print("\n🎉 Your chatbot will work now!")
        
    elif response.status_code == 401:
        print("❌ FAILED: Invalid API key (401 Unauthorized)")
        print("\nYour API key is wrong or expired.")
        print("\nFix:")
        print("1. Go to: https://console.groq.com/keys")
        print("2. Delete old key")
        print("3. Create NEW key")
        print("4. Update .env file")
        
    elif response.status_code == 429:
        print("⚠️  Rate limit exceeded")
        print("Wait a few minutes and try again")
        
    else:
        print(f"⚠️  Unexpected error: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nCheck your internet connection")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)