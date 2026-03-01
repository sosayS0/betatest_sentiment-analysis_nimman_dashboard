import pandas as pd

# โหลดไฟล์เฉลยของคุณ
df = pd.read_csv('Gold_Standard_Final.csv', keep_default_na=False)

print("="*50)
print(f"📊 สรุปจำนวนรีวิว: {len(df)} ข้อ")
print(f"👉 ถ้าได้ 99 ข้อ แปลว่าเผลอลบรีวิวทิ้งไป 1 แถวครับ (99 x 4 = 396)")
print("="*50)

# สแกนหาคำที่สะกดผิด (ที่ไม่ใช่ POS, NEG, NEU, N/A)
aspects = ['human_food', 'human_service', 'human_atmos', 'human_price']
valid_labels = ['POS', 'NEG', 'NEU', 'N/A']

print("🚨 กำลังสแกนหาคำผิดใน Gold Standard...")
found_error = False

for col in aspects:
    # ดึงเฉพาะแถวที่มีคำแปลกประหลาด
    bad_rows = df[~df[col].astype(str).str.strip().str.upper().isin(valid_labels)]
    
    if not bad_rows.empty:
        found_error = True
        for index, row in bad_rows.iterrows():
            # index + 2 เพื่อให้ตรงกับเลขแถวใน Excel (บวก Header และ 0-indexing)
            print(f"❌ เจอคำผิดที่แถว Excel ที่ {index + 2} แกน {col} -> เขียนว่า: '{row[col]}'")

if not found_error:
    print("✅ ไม่พบคำผิดในไฟล์ Gold Standard เลยครับ!")
print("="*50)