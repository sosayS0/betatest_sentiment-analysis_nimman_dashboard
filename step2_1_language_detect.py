import pandas as pd
from langdetect import detect
from tqdm import tqdm
import time

# 1. โหลดข้อมูล Final Clean (28,156 แถว)
FILE_NAME = 'Tripadvisor_GoogleMaps_Final_Clean.csv'
print(f"⏳ กำลังโหลดข้อมูลจาก {FILE_NAME}...")
df = pd.read_csv(FILE_NAME)

# เปิดใช้งาน progress bar สำหรับ pandas
tqdm.pandas(desc="🔍 กำลังสแกนภาษาทีละบรรทัด")

# 2. ฟังก์ชันตรวจจับภาษา
def detect_language(text):
    try:
        # ดัก error กรณี text ว่าง หรือเป็นตัวเลขล้วน
        lang = detect(str(text))
        if lang == 'th': return 'Thai'
        elif lang == 'en': return 'English'
        elif lang == 'zh-cn' or lang == 'zh-tw': return 'Chinese'
        elif lang == 'ko': return 'Korean'
        elif lang == 'ja': return 'Japanese'
        else: return 'Other'
    except:
        return 'Unknown'

# 3. สแกนและสร้างคอลัมน์ใหม่
print("🚀 เริ่มตรวจจับภาษา (อาจใช้เวลา 1-3 นาที ขึ้นอยู่กับสเปคคอม)...")
start_time = time.time()
df['Language'] = df['Review_Text'].progress_apply(detect_language)

# 4. สรุปผลลัพธ์
print("\n" + "="*50)
print("📊 LANGUAGE DISTRIBUTION REPORT (สัดส่วนภาษาทั้งหมด)")
print("="*50)

# คำนวณ %
lang_counts = df['Language'].value_counts()
lang_percent = df['Language'].value_counts(normalize=True) * 100

# สร้างตารางสรุปให้ดูง่ายๆ
summary_df = pd.DataFrame({
    'จำนวนรีวิว (แถว)': lang_counts,
    'สัดส่วน (%)': lang_percent.round(2)
})
print(summary_df.to_string())

# คำนวณสัดส่วน TH + EN
th_en_pct = lang_percent.get('Thai', 0) + lang_percent.get('English', 0)
print("-" * 50)
print(f"🎯 สัดส่วน ไทย + อังกฤษ รวมกันคิดเป็น: {th_en_pct:.2f}%")
print(f"⏱️ ใช้เวลาประมวลผล: {time.time() - start_time:.2f} วินาที")
print("="*50)

# เซฟทับเป็นไฟล์ใหม่เพื่อเอาไปสุ่ม 100 ข้อ
df.to_csv('Tripadvisor_GoogleMaps_Lang_Tagged.csv', index=False, encoding='utf-8-sig')
print("💾 บันทึกไฟล์ที่แท็กภาษาแล้วชื่อ 'Tripadvisor_GoogleMaps_Lang_Tagged.csv'")
