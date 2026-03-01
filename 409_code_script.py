import pandas as pd
import numpy as np

# 1. โหลดข้อมูลของคุณ (เปลี่ยนชื่อไฟล์ให้ตรง)
df = pd.read_csv('Nimman_ShopList_126store_Output_409.csv')

# 2. ฟังก์ชันซ่อมและแปลง Price Range
def fix_and_map_price(text):
    if pd.isna(text): return np.nan
    
    # ลบช่องว่างและลูกน้ำทิ้งให้หมดเพื่อให้อ่านง่ายขึ้น
    text = str(text).replace(' ', '').replace(',', '')
    
    # ดักจับเคสที่พังๆ ที่คุณเจอ
    if '800–1' in text or '800-1' in text: return 5  # ฿800-1,000
    if '000+' in text: 
        if '2' in text: return 11 # เดาว่าเป็น 2,000+
        return 6                  # เดาว่าเป็น 1,000+
        
    # เคสปกติที่ดึงมาได้
    if '1–200' in text or '1-200' in text: return 1
    elif '200–400' in text or '200-400' in text: return 2
    elif '400–600' in text or '400-600' in text: return 3
    elif '600–800' in text or '600-800' in text: return 4
    elif '800–1000' in text or '800-1000' in text: return 5
    elif '1000–1200' in text or '1000-1200' in text: return 6
    elif '1200–1400' in text or '1200-1400' in text: return 7
    elif '1400–1600' in text or '1400-1600' in text: return 8
    elif '1600–1800' in text or '1600-1800' in text: return 9
    elif '1800–2000' in text or '1800-2000' in text: return 10
    elif '2000+' in text: return 11
    
    return np.nan

# สร้างคอลัมน์ใหม่ที่ซ่อมแล้ว
df['Price_Level'] = df['Price_Range'].apply(fix_and_map_price)

# 3. แปลงคอลัมน์คะแนนให้เป็นตัวเลข (ป้องกัน error ถ้ามีตัวอักษรปนมา)
cols_to_numeric = ['Rating', 'Score_Food', 'Score_Service', 'Score_Atmosphere']
for col in cols_to_numeric:
    # errors='coerce' คือถ้าเจอคำแปลกๆ ให้เปลี่ยนเป็นค่าว่าง (NaN) ไปเลย
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 4. ยุบรวมข้อมูล (หาค่าเฉลี่ยรายร้าน)
final_df = df.groupby('Restaurant_Name').agg(
    Total_Reviews=('Rating', 'count'),          # นับจำนวนรีวิว
    Avg_Rating=('Rating', 'mean'),              # Y: คะแนนรวมเฉลี่ย
    Avg_Food=('Score_Food', 'mean'),            # X1: อาหาร
    Avg_Service=('Score_Service', 'mean'),      # X2: บริการ
    Avg_Atmos=('Score_Atmosphere', 'mean'),     # X3: บรรยากาศ
).reset_index()

# 5. ดึง Price_Level ที่เจอบ่อยที่สุดของแต่ละร้านมาใส่ (เพราะ 1 ร้านควรมีราคาเดียว)
def get_mode_price(x):
    modes = x.mode()
    return modes.iloc[0] if not modes.empty else np.nan

price_df = df.dropna(subset=['Price_Level']).groupby('Restaurant_Name')['Price_Level'].agg(get_mode_price).reset_index()

# รวมตารางค่าเฉลี่ย กับ ตารางระดับราคา เข้าด้วยกัน
final_df = pd.merge(final_df, price_df, on='Restaurant_Name', how='left')

# 6. บันทึกผลลัพธ์
final_df.to_csv('Final_Model_Data.csv', index=False, encoding='utf-8-sig')

print(f"แปลงข้อมูลสำเร็จ! ได้มา {len(final_df)} ร้าน พร้อมรันโมเดลครับ")