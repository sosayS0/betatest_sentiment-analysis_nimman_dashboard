import pandas as pd
from sklearn.metrics import cohen_kappa_score

# 1. ใส่ชื่อไฟล์ CSV ของคุณและเพื่อนตรงนี้ครับ
FILE_ANNO_1 = 'Anno_1.csv'  # ไฟล์ของคุณ
FILE_ANNO_2 = 'Anno_2.csv'  # ไฟล์ของเพื่อน

print("⏳ กำลังโหลดและเทียบคำตอบ...")
df1 = pd.read_csv(FILE_ANNO_1)
df2 = pd.read_csv(FILE_ANNO_2)

# แกนที่เราประเมิน
aspects = ['human_food', 'human_service', 'human_atmos', 'human_price']

# คลีนข้อมูลป้องกัน Human Error (เช่น เผลอกด Spacebar ท้ายคำ หรือพิมพ์ตัวเล็ก)
for col in aspects:
    df1[col] = df1[col].astype(str).str.strip().str.upper()
    df2[col] = df2[col].astype(str).str.strip().str.upper()

# 2. คำนวณ Cohen's Kappa
print("\n" + "="*50)
print("📊 สรุปผลคะแนน Cohen's Kappa (Inter-Annotator Agreement)")
print("="*50)

conflict_rows = []

for aspect in aspects:
    # ดึงคำตอบมาเทียบกัน
    labels_1 = df1[aspect].tolist()
    labels_2 = df2[aspect].tolist()
    
    # คำนวณ Kappa
    kappa = cohen_kappa_score(labels_1, labels_2)
    
    # แปลผลคะแนน
    if kappa >= 0.81: interpretation = "ดีเยี่ยม (Almost Perfect)"
    elif kappa >= 0.61: interpretation = "ดีมาก (Substantial)"
    elif kappa >= 0.41: interpretation = "ปานกลาง (Moderate)"
    else: interpretation = "ต้องปรับปรุง (Fair/Poor)"
        
    print(f"🔹 {aspect.upper()}: {kappa:.4f} -> {interpretation}")
    
    # 3. หาข้อที่ตอบไม่ตรงกัน
    for i in range(len(df1)):
        if df1.at[i, aspect] != df2.at[i, aspect]:
            conflict_rows.append({
                'Row_Index': i,
                'Review_Text': df1.at[i, 'Review_Text'],
                'Aspect': aspect,
                'Tak_Answer': df1.at[i, aspect],
                'Friend_Answer': df2.at[i, aspect],
                'Note': df1.at[i, 'annotation_note'] if 'annotation_note' in df1.columns else ''
            })

# 4. สรุปและเซฟไฟล์ข้อที่ต้องเคลียร์ใจ
print("-" * 50)
conflict_df = pd.DataFrame(conflict_rows)

if not conflict_df.empty:
    print(f"⚠️ พบข้อที่ตอบไม่ตรงกันทั้งหมด: {len(conflict_df)} จุด")
    conflict_df.to_excel('Conflict_Report.xlsx', index=False)
    print("💾 บันทึกไฟล์ 'Conflict_Report.xlsx' สำหรับนำไปนั่งคุยกับเพื่อนแล้วครับ")
else:
    print("🎉 มหัศจรรย์มาก! คุณกับเพื่อนตอบตรงกันเป๊ะ 100% ทุกข้อ!")
print("="*50)