import pandas as pd
import os
import time
import re
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# รันเฉพาะ 2 ตัวที่ดื้อ
MODELS_TO_TEST = [
    {"name": "Meta-Llama-3.1-8B-Instruct", "provider": "github", "wait_time": 15}, 
    {"name": "DeepSeek-R1", "provider": "github", "wait_time": 65} # ต้องรอ 65 วิ เพราะโดนจำกัด 1 ครั้ง/นาที
]

def call_ai(model_info, batch_texts):
    # ปรับ Prompt ให้ดุดันและบังคับฟอร์แมตขั้นสุด
    prompt_texts = "\n".join([f"[{i+1}] {txt}" for i, txt in enumerate(batch_texts)])
    full_input = f"""You are a strict data extraction tool. Read the {len(batch_texts)} reviews below.
Analyze sentiment for: FOOD, SERVICE, ATMOSPHERE, PRICE.
(POS = Positive, NEG = Negative, NEU = Neutral, N/A = Not mentioned)

CRITICAL RULES:
1. You MUST output EXACTLY {len(batch_texts)} lines.
2. Format: POS | NEG | NEU | N/A
3. DO NOT output any other words, no summaries, no headers.

[REVIEWS]:
{prompt_texts}"""

    for attempt in range(3):
        try:
            client = OpenAI(base_url="https://models.inference.ai.azure.com", api_key=GITHUB_TOKEN)
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": full_input}],
                model=model_info['name'],
                temperature=0.01
            )
            ans = response.choices[0].message.content
            
            # ไม้ตายปราบ DeepSeek: ลบทุกอย่างที่อยู่ใน <think>...</think> ทิ้งไป
            ans = re.sub(r'<think>.*?</think>', '', ans, flags=re.DOTALL)
            
            clean_ans = ans.replace('```text', '').replace('```', '').strip()
            lines = [l.strip().upper() for l in clean_ans.split('\n') if '|' in l]
            
            if len(lines) == len(batch_texts):
                return lines
            else:
                print(f"\n⚠️ {model_info['name']} ดื้อ! ตอบมา {len(lines)}/{len(batch_texts)} บรรทัด กำลังเฆี่ยนแล้วให้ทำใหม่...")
                time.sleep(model_info['wait_time'])
        except Exception as e:
            print(f"\n❌ Error ({model_info['name']}): {e}")
            time.sleep(model_info['wait_time'])
            
    return ["N/A | N/A | N/A | N/A"] * len(batch_texts)

# ==========================================
print("="*60)
print("🛠️ เริ่มปฏิบัติการปราบพยศ Llama & DeepSeek")
print("="*60)

df_test = pd.read_csv('TestSet_100.csv')
BATCH_SIZE = 10 
final_results = df_test.copy()

for model in MODELS_TO_TEST:
    print(f"\n🚀 กำลังส่งข้อสอบให้: {model['name']}...")
    all_preds = []
    
    for i in tqdm(range(0, len(df_test), BATCH_SIZE), desc=f"Evaluating {model['name']}"):
        batch = df_test['Review_Text'].iloc[i:i+BATCH_SIZE].tolist()
        preds = call_ai(model, batch)
        all_preds.extend(preds)
        time.sleep(model['wait_time']) # หน่วงเวลาตามความเอาแต่ใจของแต่ละโมเดล
    
    pred_data = []
    for p in all_preds:
        cols = [x.strip() for x in p.split('|')]
        if len(cols) == 4: pred_data.append(cols)
        else: pred_data.append(['N/A', 'N/A', 'N/A', 'N/A'])
            
    temp_df = pd.DataFrame(pred_data, columns=[f"{model['name']}_FOOD", f"{model['name']}_SERVICE", 
                                               f"{model['name']}_ATMOS", f"{model['name']}_PRICE"])
    final_results = pd.concat([final_results, temp_df], axis=1)

output_file = 'Fixed_Llama_DeepSeek_Results.csv'
final_results.to_csv(output_file, index=False, encoding='utf-8-sig')

print("\n" + "="*60)
print(f"🎉 ปราบสำเร็จ! ไฟล์ถูกเซฟไว้ที่: {output_file}")