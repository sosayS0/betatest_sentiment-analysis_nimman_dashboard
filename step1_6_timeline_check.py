import pandas as pd

# 1. โหลดข้อมูลที่คลีนแล้ว
FILE_NAME = 'Master_Dataset_Final_Cleaned.csv'
print(f"⏳ กำลังสแกนช่วงเวลาของข้อมูลจากไฟล์ {FILE_NAME}...\n")
df = pd.read_csv(FILE_NAME)

# แปลงคอลัมน์ Review_Date ให้เป็นชนิด Datetime (ถ้ามี error ให้กลายเป็น NaT)
df['Review_Date'] = pd.to_datetime(df['Review_Date'], errors='coerce')

# ดึงเฉพาะปี (Year) ออกมา
df['Year'] = df['Review_Date'].dt.year

# 2. ดูช่วงเวลา เก่าสุด - ใหม่สุด
oldest_date = df['Review_Date'].min().strftime('%Y-%m-%d')
newest_date = df['Review_Date'].max().strftime('%Y-%m-%d')

print("=" * 40)
print("📅 TIMELINE SUMMARY (สรุปช่วงเวลา)")
print("=" * 40)
print(f"🔹 รีวิวที่เก่าที่สุด: {oldest_date}")
print(f"🔹 รีวิวที่ใหม่ที่สุด: {newest_date}\n")

# 3. สร้างตารางแจกแจงจำนวนรีวิวตามปี และ แพลตฟอร์ม
timeline_table = pd.crosstab(df['Year'].astype('Int64'), df['Platform'], margins=True, margins_name="Total")

print("📊 การกระจายตัวของรีวิวแบ่งตามปี (Yearly Distribution):")
print(timeline_table.to_string())
print("\n" + "=" * 40)