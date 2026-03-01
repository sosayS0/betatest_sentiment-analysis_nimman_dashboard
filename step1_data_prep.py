import pandas as pd
import re
from datetime import datetime, timedelta

# ==========================================
# 1. ตั้งค่าชื่อไฟล์
# ==========================================
FILE_72_REST = '72_restaurants_list.csv'
FILE_GMAPS = 'Nimman_ShopList_126store_Output_409.csv'          # เปลี่ยนชื่อไฟล์ให้ตรงกับของคุณ
FILE_TRIP = 'tripadvisor_ready_for_nlp.csv'

# ==========================================
# 2. ฟังก์ชันแปลงวันที่ (Date Normalization)
# ==========================================
def parse_gmaps_date(date_str, scrape_date=datetime(2026, 2, 1)):
    """ แปลงวันที่ Google Maps (เช่น '2 months ago', 'a week ago') """
    if pd.isna(date_str): return None
    date_str = str(date_str).lower()
    
    # แปลงคำว่า a เป็น 1
    date_str = date_str.replace('a month', '1 month').replace('a week', '1 week').replace('a year', '1 year').replace('a day', '1 day')
    
    try:
        num = int(re.search(r'\d+', date_str).group())
        if 'day' in date_str: return scrape_date - timedelta(days=num)
        elif 'week' in date_str: return scrape_date - timedelta(weeks=num)
        elif 'month' in date_str: return scrape_date - timedelta(days=num*30)
        elif 'year' in date_str: return scrape_date - timedelta(days=num*365)
    except:
        pass
    return scrape_date

# ==========================================
# 3. โหลดข้อมูลและ Filter 72 ร้าน
# ==========================================
print("⏳ กำลังโหลดข้อมูล...")
df_72 = pd.read_csv(FILE_72_REST)
list_72 = df_72['Restaurant_Name'].unique().tolist()

df_gm_raw = pd.read_csv(FILE_GMAPS)
df_trip_raw = pd.read_csv(FILE_TRIP)

# กรอง Google Maps ให้เหลือแค่ 72 ร้าน
df_gm = df_gm_raw[df_gm_raw['Restaurant_Name'].isin(list_72)].copy()
print(f"📌 กรอง Google Maps จาก {len(df_gm_raw)} เหลือ {len(df_gm)} รีวิว (เฉพาะ 72 ร้าน)")

# ==========================================
# 4. ปรับโครงสร้างคอลัมน์ (Schema Mapping)
# ==========================================
print("⏳ กำลังปรับโครงสร้างและแปลงวันที่...")

# ฝั่ง Google Maps
df_gm = df_gm[['Restaurant_Name', 'Rating', 'Date', 'Review_Original']].copy()
df_gm.rename(columns={'Rating': 'Rating_Overall', 'Date': 'Date_Raw', 'Review_Original': 'Review_Text'}, inplace=True)
df_gm['Platform'] = 'Google Maps'
df_gm['Review_Date'] = df_gm['Date_Raw'].apply(parse_gmaps_date)

# ฝั่ง TripAdvisor
df_trip = df_trip_raw[['Restaurant_Name', 'Rating_Overall', 'Date_Written', 'Detail']].copy()
df_trip.rename(columns={'Date_Written': 'Date_Raw', 'Detail': 'Review_Text'}, inplace=True)
df_trip['Platform'] = 'TripAdvisor'
df_trip['Review_Date'] = pd.to_datetime(df_trip['Date_Raw'], errors='coerce')

# ==========================================
# 5. รวมร่างข้อมูล (Union) และคลีนข้อความว่าง
# ==========================================
df_master = pd.concat([df_gm, df_trip], ignore_index=True)

# ทิ้งแถวที่ไม่มี Text (เพราะเราเอาไปทำ NLP ไม่ได้)
initial_len = len(df_master)
df_master.dropna(subset=['Review_Text'], inplace=True)
print(f"🧹 ลบรีวิวที่ไม่มีข้อความออกไป: {initial_len - len(df_master)} รายการ")

# แปลงวันที่ให้เป็นฟอร์แมต YYYY-MM-DD สวยๆ
df_master['Review_Date'] = df_master['Review_Date'].dt.strftime('%Y-%m-%d')

# จัดเรียงคอลัมน์ให้สวยงาม
df_master = df_master[['Restaurant_Name', 'Platform', 'Review_Date', 'Rating_Overall', 'Review_Text']]

# ==========================================
# 6. Data Validation (ตรวจสอบคุณภาพตามหลักการ)
# ==========================================
print("\n" + "="*40)
print("📊 LEVEL 1: DATA VALIDATION REPORT")
print("="*40)

# 6.1 Completeness Check
missing_rate = df_master.isnull().sum() / len(df_master) * 100
print("[1] Completeness Check (Missing %):")
print(missing_rate.round(2).to_string())

# 6.2 Consistency Check
print("\n[2] Consistency Check:")
print(f"- จำนวนร้านทั้งหมดใน Master: {df_master['Restaurant_Name'].nunique()} ร้าน")
print(f"- ข้อมูลจาก Google Maps: {len(df_master[df_master['Platform']=='Google Maps']):,} รีวิว")
print(f"- ข้อมูลจาก TripAdvisor: {len(df_master[df_master['Platform']=='TripAdvisor']):,} รีวิว")

# ==========================================
# 7. เซฟไฟล์ Master เตรียมส่งให้ AI
# ==========================================
df_master.to_csv('Master_Dataset_for_NLP.csv', index=False, encoding='utf-8-sig')
print("\n🎉 สร้างไฟล์ 'Master_Dataset_for_NLP.csv' สำเร็จเรียบร้อย! พร้อมลุย Step 2")