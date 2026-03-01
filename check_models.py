from google import genai

API_KEY = "AIzaSyAZvTWF1ogAWb8auVOIQQjeVxAIWruNgB0"
client = genai.Client(api_key=API_KEY)

print("🔍 กำลังค้นหาโมเดลทั้งหมดที่ API Key ของคุณใช้งานได้...")
for model in client.models.list():
    print(model.name)