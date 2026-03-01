import pandas as pd

# 1. โหลดไฟล์ตั้งต้นที่คุณใช้รัน Scraping ตอนแรกสุด
FILE_INPUT_URLS = 'tripadvisor_urls.csv'  # ไฟล์ที่มี 38 ร้านและ URL
df_target = pd.read_csv(FILE_INPUT_URLS)

# ทำความสะอาดชื่อเผื่อมีช่องว่างซ่อนอยู่
target_set = set(df_target['Restaurant_Name'].astype(str).str.strip())

# 2. โหลดไฟล์ที่เพิ่ง Clean เสร็จ
FILE_FINAL = 'Tripadvisor_GoogleMaps_Final_Clean.csv'
df_final = pd.read_csv(FILE_FINAL)

# ดึงชื่อร้านเฉพาะฝั่ง TripAdvisor ออกมา
scraped_set = set(df_final[df_final['Platform'] == 'TripAdvisor']['Restaurant_Name'].astype(str).str.strip())

# 3. หาจุดต่าง (ชื่อที่มีในเป้าหมาย แต่ไม่มีในผลลัพธ์)
missing_restaurants = target_set - scraped_set

print("=" * 50)
print("🕵️‍♂️ รายงานการตามหาร้าน TripAdvisor ที่หายไป")
print("=" * 50)
print(f"เป้าหมายตั้งต้น: {len(target_set)} ร้าน")
print(f"ดูดมาได้จริง: {len(scraped_set)} ร้าน")
print("-" * 50)

if len(missing_restaurants) > 0:
    print(f"🚨 พบร้านที่หายไป {len(missing_restaurants)} ร้าน ได้แก่:")
    for name in missing_restaurants:
        print(f"   ❌ {name}")
else:
    print("✅ ไม่พบร้านหาย! (อาจเกิดจากชื่อซ้ำในไฟล์ตั้งต้น หรือการนับเว้นวรรคผิดพลาด)")
print("=" * 50)