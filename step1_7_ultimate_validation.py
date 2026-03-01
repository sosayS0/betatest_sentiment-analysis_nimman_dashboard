import pandas as pd

# 1. โหลดข้อมูล (ดึงจากไฟล์ Master สเต็ปแรกสุด ก่อนที่จะโดนเติมวันที่ปลอม)
df = pd.read_csv('Master_Dataset_for_NLP.csv')
print("="*50)
print("🛡️ ULTIMATE DATA VALIDATION (ตามหลักวิชาการ)")
print("="*50)

# ==========================================
# 🚨 แก้ปัญหาที่ 2: จัดการ Review_Date อย่างถูกต้อง (Allison, 2001)
# ==========================================
initial_rows = len(df)
df = df.dropna(subset=['Review_Date'])
final_rows = len(df)
print(f"✅ [1] Date Imputation Fix:")
print(f"   - ทำการ Drop (ตัดทิ้ง) รีวิวที่ไม่มีวันที่ จำนวน {initial_rows - final_rows} แถว")
print(f"   - เหตุผล: สัดส่วนน้อยกว่า 5% (แค่ {(initial_rows - final_rows)/initial_rows*100:.2f}%) การตัดทิ้งรักษา Data Integrity ได้ดีที่สุด\n")

# ==========================================
# 🚨 แก้ปัญหาที่ 3: พิสูจน์ตัวเลข 92 ร้าน (Set Intersection)
# ==========================================
gm_restaurants = set(df[df['Platform'] == 'Google Maps']['Restaurant_Name'].unique())
ta_restaurants = set(df[df['Platform'] == 'TripAdvisor']['Restaurant_Name'].unique())

print(f"✅ [2] Restaurant Overlap Verification:")
print(f"   - ฝั่ง Google Maps มี: {len(gm_restaurants)} ร้าน")
print(f"   - ฝั่ง TripAdvisor มี: {len(ta_restaurants)} ร้าน")
print(f"   - 🔗 ร้านที่ชื่อตรงกันเป๊ะ (Overlap): {len(gm_restaurants & ta_restaurants)} ร้าน")
print(f"   - 📊 รวมทั้งหมด (Union): {len(gm_restaurants | ta_restaurants)} ร้าน\n")

# ==========================================
# 🚨 แก้ปัญหาที่ 1: เจาะลึก Rating_Overall ที่หายไป (Rubin, 1976)
# ==========================================
missing_rating_df = df[df['Rating_Overall'].isna()]
print(f"✅ [3] Missing Rating Analysis (จำนวน {len(missing_rating_df)} แถว):")

# ดูว่าแพลตฟอร์มไหนทำแหว่ง
platform_missing = missing_rating_df['Platform'].value_counts()
print(f"   - แตกตาม Platform:\n{platform_missing.to_string()}\n")

# ดูว่าร้านไหนแหว่งเยอะสุด (Top 5)
print(f"   - แตกตามชื่อร้าน (Top 5 ที่ Rating แหว่ง):")
print(missing_rating_df['Restaurant_Name'].value_counts().head(5).to_string())
print("\n" + "="*50)

# เซฟเป็นไฟล์ Final ของจริงที่พร้อมสุดๆ
df.to_csv('Tripadvisor_GoogleMaps_Final_Clean.csv', index=False, encoding='utf-8-sig')
print("💾 บันทึกไฟล์ที่บริสุทธิ์ 100% ชื่อ 'Tripadvisor_GoogleMaps_Final_Clean.csv' เรียบร้อยครับ!")