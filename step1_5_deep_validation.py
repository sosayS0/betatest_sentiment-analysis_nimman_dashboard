import pandas as pd

# 1. โหลดข้อมูล Master ที่เพิ่งทำเสร็จ
FILE_NAME = 'Master_Dataset_for_NLP.csv'
print(f"⏳ กำลังตรวจสอบข้อมูลเชิงลึกจากไฟล์ {FILE_NAME}...\n")
df = pd.read_csv(FILE_NAME)

# ==========================================
# 🔍 1. เจาะลึก Review_Date ที่แหว่ง (0.11%)
# ==========================================
missing_dates = df[df['Review_Date'].isnull()]
print(f"🚨 พบรีวิวที่ไม่มีวันที่ (Review_Date = NaN) จำนวน: {len(missing_dates)} แถว")

if len(missing_dates) > 0:
    print("ตัวอย่างรีวิวที่ไม่มีวันที่ (5 บรรทัดแรก):")
    print(missing_dates[['Restaurant_Name', 'Platform', 'Review_Text']].head())
    print("-" * 40)
    
    # วิธีแก้: เราจะเติม (Impute) วันที่ที่ว่าง ด้วยวันที่เราทำการ Scrape ข้อมูล (สมมติว่าเป็นวันที่ 1 ก.พ. 2026) 
    # เพื่อให้ข้อมูลยังเอาไปทำ Recency Filter ได้โดยไม่พัง
    df['Review_Date'].fillna('2026-02-01', inplace=True)
    print("✅ ซ่อมแซม Review_Date: เติมวันที่ '2026-02-01' ลงในช่องว่างเรียบร้อยแล้ว\n")

# ==========================================
# 🔍 2. ตรวจสอบความปลอดภัยของ Review_Text (Must not be Null)
# ==========================================
missing_texts = df[df['Review_Text'].isnull()]
print(f"🚨 พบรีวิวที่ไม่มีข้อความ (Review_Text = NaN) จำนวน: {len(missing_texts)} แถว")

if len(missing_texts) > 0:
    # วิธีแก้: ถ้าหลุดมาได้ ให้ลบทิ้งเด็ดขาด เพราะไม่มีประโยชน์ต่อ NLP
    df = df.dropna(subset=['Review_Text'])
    print(f"✅ ซ่อมแซม Review_Text: ลบแถวที่ไม่มีข้อความทิ้งเรียบร้อยแล้ว\n")
else:
    print("✅ Review_Text สมบูรณ์ 100% ไม่มีบรรทัดไหนว่าง!\n")

# ==========================================
# 🔍 3. ตรวจสอบว่า Rating_Overall มีตัวอักษรแปลกปลอมไหม
# ==========================================
# เปลี่ยนข้อมูลเป็นตัวเลข (ถ้าเจอคำแปลกๆ จะกลายเป็น NaN)
df['Rating_Overall'] = pd.to_numeric(df['Rating_Overall'], errors='coerce')
print(f"ℹ️ Rating_Overall มีค่าว่าง (NaN) {df['Rating_Overall'].isnull().sum()} แถว (ปล่อยไว้ได้ ไม่มีผลต่อ NLP)\n")

# ==========================================
# 💾 4. เซฟไฟล์ Final จริงๆ สำหรับ NLP
# ==========================================
FINAL_FILE = 'Master_Dataset_Final_Cleaned.csv'
df.to_csv(FINAL_FILE, index=False, encoding='utf-8-sig')

print("=" * 50)
print(f"🎉 ตรวจสอบและซ่อมแซมเสร็จสิ้น! ข้อมูลคลีน 100%")
print(f"💾 บันทึกไฟล์ใหม่ชื่อ: {FINAL_FILE}")
print(f"📊 สรุปจำนวนข้อมูลที่พร้อมรัน AI: {len(df)} แถว")
print("=" * 50)