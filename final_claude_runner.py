import pandas as pd
import time
from tqdm import tqdm
from anthropic import AnthropicVertex

MY_PROJECT_ID = "nppi-claude-test" # เปลี่ยนเป็น Project ID ของคุณ Tak 
MY_REGION = "us-east5" 

client = AnthropicVertex(region=MY_REGION, project_id=MY_PROJECT_ID)

SYSTEM_PROMPT = """Analyze sentiment for: FOOD, SERVICE, ATMOSPHERE, PRICE.
(POS = Positive, NEG = Negative, NEU = Neutral, N/A = Not mentioned)
Format: POS | NEG | NEU | N/A"""

def call_claude(text):
    full_input = f"{SYSTEM_PROMPT}\n\n[REVIEW]:\n{text}"
    
    for attempt in range(3):
        try:
            response = client.messages.create(
                model="claude-haiku-4-5@20251001", 
                max_tokens=100, # ลด Token ฝั่งขาออกลงเพื่อประหยัดโควต้า
                temperature=0.01,
                messages=[{"role": "user", "content": full_input}]
            )
            ans = response.content[0].text
            # ดึงเฉพาะบรรทัดที่มีเครื่องหมาย |
            lines = [l.strip().upper() for l in ans.split('\n') if '|' in l]
            if lines:
                return lines[0] # ส่งกลับมา 1 บรรทัด
            time.sleep(2)
        except Exception as e:
            error_msg = str(e)
            if '429' in error_msg:
                time.sleep(10) # ถ้าบังเอิญโดน 429 ให้พักแค่ 10 วินาทีพอ
            else:
                print(f"\n❌ Error: {e}")
                time.sleep(5)
                
    return "N/A | N/A | N/A | N/A"

# ==========================================
# เริ่มการทำงาน (หยดน้ำ Mode - ทีละ 1 ข้อ)
# ==========================================
print("="*60)
print("🎯 เริ่มรัน Claude Haiku 4.5 (โหมดส่งทีละ 1 ข้อ การันตีผ่านชัวร์)")
print("="*60)

df_results = pd.read_csv('Model_Comparison_Full_Results.csv')
all_preds = []

# ส่งทีละ 1 ข้อ (100 ข้อ = 100 รอบ)
for i in tqdm(range(len(df_results)), desc="Evaluating Claude 4.5"):
    review_text = df_results['Review_Text'].iloc[i]
    pred = call_claude(review_text)
    all_preds.append(pred)
    time.sleep(3) # 🚀 หน่วงเวลา 3 วินาทีต่อข้อ หลอด Token ไม่เต็มแน่นอน

# จัดการตาราง
pred_data = []
for p in all_preds:
    cols = [x.strip() for x in p.split('|')]
    if len(cols) == 4: 
        pred_data.append(cols)
    else: 
        pred_data.append(['N/A', 'N/A', 'N/A', 'N/A'])

claude_df = pd.DataFrame(pred_data, columns=[
    "claude-4.5-haiku_FOOD", "claude-4.5-haiku_SERVICE", 
    "claude-4.5-haiku_ATMOS", "claude-4.5-haiku_PRICE"
])

cols_to_drop = [col for col in df_results.columns if 'claude' in col.lower()]
if cols_to_drop:
    df_results.drop(columns=cols_to_drop, inplace=True)

final_results = pd.concat([df_results, claude_df], axis=1)
final_results.to_csv('Model_Comparison_Full_Results.csv', index=False, encoding='utf-8-sig')

print("\n🎉 ข้อมูลครบ 100 ข้อแล้ว! เซฟลงไฟล์ Model_Comparison_Full_Results.csv เรียบร้อย!")