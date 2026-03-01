import pandas as pd

# 1. โหลดข้อมูลที่คุณเพิ่ง Scrape มา
print("⏳ กำลังโหลดและทำความสะอาดข้อมูล...")
df = pd.read_csv('tripadvisor_reviews_cleaned.csv')

# 2. ลบข้อมูลที่ซ้ำซ้อน (Duplicates) จากการที่บอทค้างแล้วรันใหม่
initial_count = len(df)
df_clean = df.drop_duplicates(subset=['Restaurant_Name', 'Detail', 'Date_Written'])
final_count = len(df_clean)
print(f"🧹 ลบข้อมูลที่ซ้ำซ้อนออกไป: {initial_count - final_count} แถว")
print(f"✅ จำนวน Review Text สุทธิที่ใช้ได้จริง: {final_count} คอมเมนต์\n")

# 3. เซฟไฟล์ที่คลีนแล้วเตรียมไว้ให้ AI อ่าน
df_clean.to_csv('tripadvisor_ready_for_nlp.csv', index=False, encoding='utf-8-sig')

# 4. ทำ Validation สรุปรายร้าน (คล้ายที่ Claude แนะนำ)
summary = df_clean.groupby('Restaurant_Name').agg(
    scraped_text_count=('Detail', 'count')
).reset_index()

# เรียงลำดับจากร้านที่มีรีวิวเยอะสุดไปน้อยสุด
summary = summary.sort_values(by='scraped_text_count', ascending=False)

print("📊 สรุปจำนวน Review Text แต่ละร้าน (Top 10):")
print(summary.head(10).to_string(index=False))