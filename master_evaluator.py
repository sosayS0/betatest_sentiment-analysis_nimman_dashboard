import pandas as pd
import os
import time
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI
from google import genai

# ==========================================
# 1. ระบบรักษาความปลอดภัย & ดึง API Keys
# ==========================================
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not GITHUB_TOKEN or not GEMINI_KEY:
    print("🚨 ERROR: หา API Key ไม่เจอ! กรุณาตรวจสอบไฟล์ .env ด่วนครับ!")
    exit()

# ==========================================
# 2. รายชื่อนักสู้ AI (คัดมาเน้นๆ ครบทุกสไตล์)
# ==========================================
MODELS_TO_TEST = [
    {"name": "gemini-2.5-flash", "provider": "gemini"},            # Baseline ของเรา (จ่ายสตางค์เดียว)
    {"name": "gpt-4o-mini", "provider": "github"},                 # ตัวแทน OpenAI (ฟรี)
    {"name": "DeepSeek-R1", "provider": "github"},                 # ตัวแทนสาย Reasoning จากจีน (ฟรี)
    {"name": "Meta-Llama-3.1-8B-Instruct", "provider": "github"}   # ตัวแทน Open Source จาก Meta (ฟรี)
]

# ==========================================
# 3. Master Prompt (คำสั่งคุมสอบ)
# ==========================================
SYSTEM_PROMPT = """You are a strictly formatted sentiment analysis assistant.
Analyze the following restaurant reviews and classify the sentiment for 4 aspects: FOOD, SERVICE, ATMOSPHERE, and PRICE.
Format EXACTLY as: POS | NEG | NEU | N/A

Rules:
1. Provide EXACTLY one line of output per input review.
2. Do not include review numbers, headers, markdown, or any conversational text.
3. If an aspect is missing, use N/A."""

# ==========================================
# 4. ฟังก์ชันส่งข้อสอบไปให้ AI (พร้อมระบบกันพัง)
# ==========================================
def call_ai(model_info, batch_texts):
    # มัดรวมข้อสอบ 10 ข้อ
    prompt = "\n".join([f"Review {i+1}: {txt}" for i, txt in enumerate(batch_texts)])
    full_input = f"{SYSTEM_PROMPT}\n\n[INPUT REVIEWS]:\n{prompt}"
    
    # ระบบ Auto-Retry ให้โอกาสทำใหม่ 3 ครั้งถ้าตอบรวน
    for attempt in range(3):
        try:
            if model_info['provider'] == 'github':
                client = OpenAI(base_url="https://models.inference.ai.azure.com", api_key=GITHUB_TOKEN)
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": full_input}],
                    model=model_info['name'],
                    temperature=0.01
                )
                ans = response.choices[0].message.content
            else: # Gemini
                client = genai.Client(api_key=GEMINI_KEY)
                response = client.models.generate_content(model=model_info['name'], contents=full_input)
                ans = response.text
            
            # คลีนคำตอบและเช็กยอดว่าครบ 10 บรรทัดไหม
            clean_ans = ans.replace('```text', '').replace('```', '').strip()
            lines = [l.strip().upper() for l in clean_ans.split('\n') if '|' in l]
            
            if len(lines) == len(batch_texts):
                return lines
            else:
                print(f"\n⚠️ {model_info['name']} ตอบขาด/เกิน ({len(lines)}/{len(batch_texts)} บรรทัด) กำลังสั่งทำใหม่...")
                time.sleep(3)
        except Exception as e:
            print(f"\n❌ พบปัญหา API ของ {model_info['name']}: {e}")
            time.sleep(5)
            
    # ถ้าพังครบ 3 รอบ ให้ตอบ N/A รวนไปเลยจะได้ข้ามไปก่อน
    return ["N/A | N/A | N/A | N/A"] * len(batch_texts)

# ==========================================
# 5. สั่งลุยรันระบบจริง
# ==========================================
print("="*60)
print("⚔️ ยินดีต้อนรับสู่สมรภูมิประลอง AI (Multi-Model Evaluation)")
print("="*60)

# โหลดข้อสอบ
df_test = pd.read_csv('TestSet_100.csv')
BATCH_SIZE = 10 
final_results = df_test.copy()

for model in MODELS_TO_TEST:
    print(f"\n🚀 กำลังส่งข้อสอบให้โมเดล: {model['name']}...")
    all_preds = []
    
    # วิ่งทีละ 10 ข้อ
    for i in tqdm(range(0, len(df_test), BATCH_SIZE), desc=f"Evaluating {model['name']}"):
        batch = df_test['Review_Text'].iloc[i:i+BATCH_SIZE].tolist()
        preds = call_ai(model, batch)
        all_preds.extend(preds)
        time.sleep(12) # หน่วงเวลา 12 วิ ไม่ให้โดน GitHub แบน (โควต้าของฟรี)
    
    # จัดเรียงผลลัพธ์ใส่ตาราง
    pred_data = []
    for p in all_preds:
        cols = [x.strip() for x in p.split('|')]
        if len(cols) == 4:
            pred_data.append(cols)
        else:
            pred_data.append(['N/A', 'N/A', 'N/A', 'N/A'])
            
    temp_df = pd.DataFrame(pred_data, columns=[f"{model['name']}_FOOD", f"{model['name']}_SERVICE", 
                                               f"{model['name']}_ATMOS", f"{model['name']}_PRICE"])
    
    final_results = pd.concat([final_results, temp_df], axis=1)

# ==========================================
# 6. เซฟผลลัพธ์ลงไฟล์ CSV
# ==========================================
output_file = 'Model_Comparison_Full_Results.csv'
final_results.to_csv(output_file, index=False, encoding='utf-8-sig')

print("\n" + "="*60)
print(f"🎉 โคตรเจ๋ง! ประเมินเสร็จสมบูรณ์ 100% แล้วครับคุณ Tak!")
print(f"👉 ไปเปิดดูผลลัพธ์ในไฟล์: {output_file} ได้เลย")
print("="*60)