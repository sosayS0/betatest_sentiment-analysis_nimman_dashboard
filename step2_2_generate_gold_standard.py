import pandas as pd

# 1. โหลดข้อมูลที่ Tag ภาษามาแล้ว
FILE_NAME = 'Tripadvisor_GoogleMaps_Lang_Tagged.csv'
print(f"⏳ กำลังโหลดข้อมูลจาก {FILE_NAME}...")
df = pd.read_csv(FILE_NAME)

# ==========================================
# 🔍 เช็กความผิดปกติของภาษา (Cross-tabulation)
# ==========================================
print("\n" + "="*50)
print("📊 ตรวจสอบการกระจายตัวของภาษาตามแพลตฟอร์ม")
print("="*50)
cross_tab = df.groupby(['Platform', 'Language'])['Review_Text'].count().unstack(fill_value=0)
print(cross_tab[['Thai', 'English']].to_string())
print("-" * 50)

# ==========================================
# 🎯 สร้างชุดข้อสอบ 100 ข้อ (Oversampled Stratified)
# ==========================================
# โควตารวม: English 60 ข้อ / Thai 40 ข้อ
quotas = [
    {'Platform': 'Google Maps', 'Language': 'Thai', 'n': 30},     # คนไทยรีวิวใน Google Maps
    {'Platform': 'Google Maps', 'Language': 'English', 'n': 20},  # ต่างชาติ/คนไทยพิมพ์อิ้ง ใน Google Maps
    {'Platform': 'TripAdvisor', 'Language': 'English', 'n': 40},  # ต่างชาติรีวิวใน Trip
    {'Platform': 'TripAdvisor', 'Language': 'Thai', 'n': 10}      # คนไทยรีวิวใน Trip (มีน้อย เลยเอามาแค่นี้)
]

sampled_dfs = []
for q in quotas:
    subset = df[(df['Platform'] == q['Platform']) & (df['Language'] == q['Language'])]
    if len(subset) >= q['n']:
        sampled = subset.sample(n=q['n'], random_state=42)
        sampled_dfs.append(sampled)
    else:
        print(f"⚠️ คำเตือน: ข้อมูลไม่พอสำหรับ {q['Platform']} - {q['Language']}")
        sampled_dfs.append(subset)

# รวมเป็น 100 ข้อ
df_100 = pd.concat(sampled_dfs, ignore_index=True)

# สลับแถวแบบสุ่ม (Shuffle) เพื่อกันความลำเอียงตอนทำเฉลย
df_100 = df_100.sample(frac=1, random_state=99).reset_index(drop=True)

# สร้างคอลัมน์ว่าง 4 แกน
columns_to_keep = ['Restaurant_Name', 'Platform', 'Language', 'Review_Text']
df_100 = df_100[columns_to_keep]
df_100['human_food'] = ""
df_100['human_service'] = ""
df_100['human_atmos'] = ""
df_100['human_price'] = ""

# เซฟไฟล์ Excel
OUTPUT_FILE = 'Gold_Standard_100.xlsx'
df_100.to_excel(OUTPUT_FILE, index=False)

print("\n" + "="*50)
print(f"🎉 สร้างชุดข้อสอบสำเร็จแล้ว! (รวม {len(df_100)} ข้อ)")
print(f"💾 ไฟล์สำหรับทำเฉลย: {OUTPUT_FILE}")
print("="*50)
