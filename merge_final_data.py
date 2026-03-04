import pandas as pd

print("🔄 กำลังรวมร่างข้อมูล NASS เข้ากับข้อมูลเฉลี่ยของร้าน (Avg_Rating, Price_Level)...")

# 1. โหลดไฟล์ทั้งสองขึ้นมา
df_nass = pd.read_csv('restaurant_summary.csv')
df_meta = pd.read_csv('Google_Maps_125_Final_Model_Data.csv')

# 2. ทำการ Merge โดยใช้ Restaurant_Name เป็นกุญแจหลัก (Key)
# ใช้ how='inner' เพื่อเอาเฉพาะร้านที่มีข้อมูลครบทั้งสองฝั่ง
df_final = pd.merge(df_nass, df_meta[['Restaurant_Name', 'Avg_Rating', 'Price_Level']], 
                    on='Restaurant_Name', 
                    how='inner')

# 3. จัดการคอลัมน์ซ้ำซ้อน (เพราะใน df_nass อาจจะมี Avg_Rating ที่เป็นค่าว่างติดมาตอนแรก)
# เราจะใช้ Avg_Rating จากไฟล์ df_meta แทน เพราะมันมีตัวเลขที่ถูกต้อง
if 'Avg_Rating_x' in df_final.columns and 'Avg_Rating_y' in df_final.columns:
    df_final['Avg_Rating'] = df_final['Avg_Rating_y']
    df_final.drop(columns=['Avg_Rating_x', 'Avg_Rating_y'], inplace=True)
elif 'Avg_Rating' in df_nass.columns:
    # ถ้าตอนแรกมี Avg_Rating ที่เป็นค่าว่างใน df_nass เราจะทับมันด้วยของใหม่เลย
    pass 

# 4. จัดเรียงคอลัมน์ให้ดูง่ายๆ สำหรับทำ Dashboard
cols_order = [
    'Restaurant_Name', 'Total_Reviews', 'Price_Level', 'Avg_Rating',
    'NASS_FOOD', 'NASS_SERVICE', 'NASS_ATMOS', 'NASS_PRICE'
]
# ดึงเฉพาะคอลัมน์ที่มีอยู่จริง
final_cols = [c for c in cols_order if c in df_final.columns]
df_final = df_final[final_cols]

# 5. ปัดเศษ Avg_Rating ให้เหลือ 2 ตำแหน่งจะได้สวยๆ บนหน้าเว็บ
df_final['Avg_Rating'] = df_final['Avg_Rating'].round(2)

# เซฟเป็นไฟล์เตรียมขึ้น Web
df_final.to_csv('Dashboard_Master_Data.csv', index=False, encoding='utf-8-sig')

print(f"✅ รวมร่างสำเร็จ! ได้ร้านอาหารที่มีข้อมูลครบถ้วนจำนวน {len(df_final)} ร้าน")
print("🎉 ไฟล์ 'Dashboard_Master_Data.csv' พร้อมสำหรับนำไปทำ Web Dashboard ใน Cursor แล้วครับ!")