import pandas as pd

# โหลดไฟล์เต็ม
df = pd.read_csv('Tripadvisor_GoogleMaps_Lang_Tagged.csv')

# กรองเอาเฉพาะ TripAdvisor และ ภาษาไทย
ta_thai = df[(df['Platform'] == 'TripAdvisor') & (df['Language'] == 'Thai')]

print("="*50)
print(f"🕵️‍♂️ พบรีวิว TripAdvisor (ภาษาไทย) ทั้งหมด {len(ta_thai)} ข้อ ดังนี้:")
print("="*50)

# วนลูปปริ้นต์ออกมาให้ดูทีละข้อ
for index, row in ta_thai.iterrows():
    print(f"📌 ร้าน: {row['Restaurant_Name']}")
    print(f"💬 ข้อความ: {row['Review_Text']}")
    print("-" * 50)