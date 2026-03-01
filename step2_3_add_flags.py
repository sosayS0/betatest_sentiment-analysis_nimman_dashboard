import pandas as pd
import numpy as np

# 1. โหลดไฟล์ข้อสอบที่คุณเพิ่งสร้างเสร็จ
df = pd.read_excel('Gold_Standard_100.xlsx')

# 2. สร้างคอลัมน์ Note เปล่าๆ รอไว้
df['annotation_note'] = ''

# 3. ใส่เงื่อนไข (แปลงเป็น string ก่อน เพื่อป้องกัน Error ถ้าเจอช่องว่าง)
is_truncated = df['Review_Text'].astype(str).str.endswith(('…', '...'))
is_short = df['Review_Text'].astype(str).str.len() < 20

# 4. ประทับตรา Flag ลงไปในคอลัมน์ Note (ใช้ += เผื่อมีบางรีวิวเป็นทั้งคู่)
df.loc[is_truncated, 'annotation_note'] += '[TRUNCATED] '
df.loc[is_short, 'annotation_note'] += '[SHORT]'

# 5. เซฟเป็นไฟล์ v2 ที่สมบูรณ์แบบ
OUTPUT_FILE = 'Gold_Standard_100_v2.xlsx'
df.to_excel(OUTPUT_FILE, index=False)

print("="*50)
print("✅ อัปเกรดไฟล์เรียบร้อย! เพิ่มคอลัมน์ 'annotation_note' แล้ว")
print(f"💾 ไปเปิดไฟล์ที่ชื่อว่า: {OUTPUT_FILE} แล้วเริ่มทำเฉลยได้เลยครับ!")
print("="*50)