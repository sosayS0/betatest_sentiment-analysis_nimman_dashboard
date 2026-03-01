import pandas as pd
from google import genai
from google.genai import types
import time
import os
from tqdm import tqdm

print("="*60)
print("🚀 เริ่มระบบ Mass Inference (รันข้อมูลจริง 20,000 แถว)")
print("="*60)

# 1. ตั้งค่า API KEY ของคุณตรงนี้ (ใส่ในเครื่องหมายคำพูด)
API_KEY = "AIzaSyDpJzb2X569qOemPEF4QS4ljJNNi23plJE"
client = genai.Client(api_key=API_KEY)

# 2. ตั้งค่าไฟล์
INPUT_FILE = 'Tripadvisor_GoogleMaps_Lang_Tagged.csv'
OUTPUT_FILE = 'NPPI_Sentiment_Results_Final.csv'
BATCH_SIZE = 20
DELAY = 5 # หน่วงเวลา 5 วินาทีต่อรอบ

# ---------------------------------------------------------
# 💡 MASTER PROMPT
# ---------------------------------------------------------
system_instruction = """
You are a sentiment analysis assistant. Analyze the restaurant reviews and classify the sentiment for 4 aspects: FOOD, SERVICE, ATMOSPHERE, and PRICE.
Output ONLY the strict format: POS | NEG | NEU | N/A

Guideline:
- POS = Positive, NEG = Negative, NEU = Neutral/Mixed, N/A = Not Mentioned.
- Reply strictly line by line corresponding to the input. Do not add any extra text, header, or markdown formatting.
"""

def get_gemini_response(prompt, retries=3):
    """ฟังก์ชันส่งข้อมูลไปหา AI พร้อมระบบกันตาย (Auto-Retry)"""
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash', # 👈 ใส่ชื่อรุ่น 2.5 Flash ตัวแรงสุดไปเลยครับ!
                contents=system_instruction + "\n\n[INPUT DATA]\n" + prompt,
            )
            return response.text.strip()
        except Exception as e:
            error_msg = str(e)
            if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg:
                print(f"\n⏳ AI รันเร็วเกินไป! ระบบจะหยุดพัก 60 วินาทีแล้วลุยต่อ (ครั้งที่ {attempt+1}/{retries})...")
                time.sleep(60) # พัก 1 นาทีแล้วลองใหม่
            else:
                print(f"\n⚠️ พบปัญหาขัดข้องจาก API: {error_msg}")
                return None
    return None

# 3. โหลดและกรองข้อมูล
print("⏳ กำลังโหลดและเตรียมข้อมูล...")
df_raw = pd.read_csv(INPUT_FILE)

df = df_raw[df_raw['Language'].isin(['Thai', 'English'])].copy()
print(f"✅ จำนวนข้อมูลที่จะรันจริง: {len(df)} แถว (ตัดภาษาอื่นออกแล้ว)")

# 4. ระบบ Auto-Save 
if os.path.exists(OUTPUT_FILE):
    df_done = pd.read_csv(OUTPUT_FILE)
    processed_indices = df_done['Original_Index'].tolist()
    print(f"♻️ พบไฟล์เดิม! เคยรันไปแล้ว {len(processed_indices)} แถว จะทำต่อจากจุดเดิม...")
    df_to_process = df[~df.index.isin(processed_indices)]
else:
    df_to_process = df.copy()
    pd.DataFrame(columns=['Original_Index', 'Restaurant_Name', 'Review_Text', 'FOOD', 'SERVICE', 'ATMOS', 'PRICE']).to_csv(OUTPUT_FILE, index=False)
    print("✨ สร้างไฟล์ใหม่พร้อมลุย!")

total_remaining = len(df_to_process)
if total_remaining == 0:
    print("🎉 รันข้อมูลครบ 100% แล้วครับคุณ Tak!")
    exit()

# 5. ลูปส่งข้อมูลให้ AI ทำงาน
batches = [df_to_process[i:i + BATCH_SIZE] for i in range(0, total_remaining, BATCH_SIZE)]
print(f"📦 แบ่งข้อมูลได้ทั้งหมด {len(batches)} ก้อน (รอรันประมาณ {len(batches) * DELAY / 60:.1f} นาที)")

for batch in tqdm(batches, desc="🧠 AI กำลังทำงาน"):
    input_text = ""
    for idx, row in batch.iterrows():
        clean_text = str(row['Review_Text']).replace('\n', ' ')
        input_text += f"[{idx}] {clean_text}\n"
    
    # ส่งให้ Gemini
    result_text = get_gemini_response(input_text)
    
    if result_text:
        results_list = result_text.split('\n')
        cleaned_results = [r.replace('```text', '').replace('```', '').strip() for r in results_list if '|' in r]
        
        batch_results = []
        for i, (idx, row) in enumerate(batch.iterrows()):
            try:
                ans = cleaned_results[i].split('|')
                batch_results.append({
                    'Original_Index': idx,
                    'Restaurant_Name': row['Restaurant_Name'],
                    'Review_Text': row['Review_Text'],
                    'FOOD': ans[0].strip(),
                    'SERVICE': ans[1].strip(),
                    'ATMOS': ans[2].strip(),
                    'PRICE': ans[3].strip()
                })
            except:
                batch_results.append({
                    'Original_Index': idx, 'Restaurant_Name': row['Restaurant_Name'], 'Review_Text': row['Review_Text'],
                    'FOOD': 'ERROR', 'SERVICE': 'ERROR', 'ATMOS': 'ERROR', 'PRICE': 'ERROR'
                })
        
        # เซฟลงไฟล์ทันที
        pd.DataFrame(batch_results).to_csv(OUTPUT_FILE, mode='a', header=False, index=False)
    
    time.sleep(DELAY)

print("\n" + "="*60)
print("🎉 MISSION ACCOMPLISHED! รันข้อมูลเสร็จสมบูรณ์ 100% แล้วครับ!")
print("="*60)