from anthropic import AnthropicVertex

MY_PROJECT_ID = "nppi-claude-test" 
MY_REGION = "us-east5" 

print("🔍 กำลังส่งสัญญาณทดสอบ (Ping) ไปหา Claude 4.5...")
client = AnthropicVertex(region=MY_REGION, project_id=MY_PROJECT_ID)

try:
    # ยิงคำถามง่ายๆ สั้นๆ ไม่กิน Token
    response = client.messages.create(
        model="claude-haiku-4-5@20251001",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hello, are you there?"}]
    )
    print("\n✅ สำเร็จ! Claude ตอบกลับมาว่า:", response.content[0].text)
except Exception as e:
    print("\n❌ โดนสกัด! นี่คือ Error ที่แท้จริงจาก Google Cloud:")
    print(e)