import pandas as pd
import numpy as np

print("🧹 1. กำลังกวาดขยะและทำความสะอาดไฟล์ดิบ...")

# โหลดไฟล์ข้อมูล 20,000 ข้อ
df = pd.read_csv('NPPI_Sentiment_Results_Final.csv')
print(f"   จำนวนแถวเริ่มต้น: {len(df)} แถว")

# รายชื่อคอลัมน์เป้าหมาย (แก้ชื่อให้ตรงกับไฟล์ของคุณ Tak นะครับ)
ASPECTS = ['FOOD', 'SERVICE', 'ATMOS', 'PRICE']
# สมมติว่าคอลัมน์ชื่อร้านคือ 'Restaurant_Name' (แก้ให้ตรงกับไฟล์จริง)
RESTAURANT_COL = 'Restaurant_Name' 

# ล้างช่องว่างและทำเป็นตัวพิมพ์ใหญ่
for col in ASPECTS:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.upper()

# กรองเอาเฉพาะแถวที่คำตอบตรง Format (กำจัดแถวที่งอกจากการเคาะ Enter)
valid_labels = ['POS', 'NEG', 'NEU', 'N/A']
df_clean = df[df['FOOD'].isin(valid_labels)].copy()

print(f"   จำนวนแถวหลังทำความสะอาด: {len(df_clean)} แถว (ต้องใกล้เคียง 15,826)")

print("\n⚙️ 2. กำลังคำนวณคะแนน NASS (Net Aspect Sentiment Score) รายร้าน...")

# ฟังก์ชันคำนวณ NASS ให้แต่ละด้าน
def calculate_nass(series):
    counts = series.value_counts()
    pos = counts.get('POS', 0)
    neg = counts.get('NEG', 0)
    neu = counts.get('NEU', 0)
    
    total_mentions = pos + neg + neu
    if total_mentions == 0:
        return np.nan # ถ้าร้านนี้ไม่มีใครพูดถึงด้านนี้เลย ให้เป็นค่าว่าง
    
    # สูตร NASS = (POS - NEG) / Total Mentions * 100
    return ((pos - neg) / total_mentions) * 100

# จัดกลุ่มตามชื่อร้าน แล้วคำนวณ NASS
nass_results = []

for restaurant, group in df_clean.groupby(RESTAURANT_COL):
    # สมมติว่ามีคอลัมน์ Avg_Rating และ Price_Level ในไฟล์ดิบด้วย
    # ถ้าไม่มี ก็ลบ 2 บรรทัดด้านล่างทิ้งได้เลยครับ
    avg_rating = group['Avg_Rating'].mean() if 'Avg_Rating' in group.columns else np.nan
    total_reviews = len(group)
    
    row_data = {
        'Restaurant_Name': restaurant,
        'Total_Reviews': total_reviews,
        'Avg_Rating': avg_rating
    }
    
    for aspect in ASPECTS:
        row_data[f'NASS_{aspect}'] = calculate_nass(group[aspect])
        
    nass_results.append(row_data)

df_summary = pd.DataFrame(nass_results)

# ปัดเศษทศนิยมให้ดูสวยงาม
for aspect in ASPECTS:
    df_summary[f'NASS_{aspect}'] = df_summary[f'NASS_{aspect}'].round(1)

# เซฟไฟล์พร้อมส่งต่อให้ Cursor
df_summary.to_csv('restaurant_summary.csv', index=False, encoding='utf-8-sig')

print("\n🎉 เสร็จสมบูรณ์! สร้างไฟล์ 'restaurant_summary.csv' สำเร็จแล้วครับ!")
print("เอาไฟล์นี้ไปโยนเข้า Cursor เพื่อปั้น Web Dashboard ได้เลย! 🚀")