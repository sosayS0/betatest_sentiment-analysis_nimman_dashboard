import pandas as pd

print("🔄 กำลังเริ่มกระบวนการประกอบร่างไฟล์...")

try:
    # 1. โหลดไฟล์ Master และไฟล์ Claude
    df_master = pd.read_csv('Model_Comparison_Full_Results.csv')
    df_claude = pd.read_csv('Anno_Claude.csv')

    print(f"📊 จำนวนรีวิวใน Master File: {len(df_master)} แถว")
    print(f"📊 จำนวนรีวิวใน Claude File: {len(df_claude)} แถว")

    # เช็กว่าจำนวนข้อเท่ากันไหม
    if len(df_master) == len(df_claude):
        print("✅ จำนวนแถวตรงกันเป๊ะ! ดำเนินการต่อ...")
        
        # 2. ดึงเฉพาะคอลัมน์คำตอบจาก Claude 
        # อ้างอิงจากตัวอย่างที่คุณ Tak ให้มา คอลัมน์ชื่อ FOOD, SERVICE, ATMOS, PRICE
        claude_answers = df_claude[['FOOD', 'SERVICE', 'ATMOS', 'PRICE']].copy()
        
        # เปลี่ยนชื่อคอลัมน์ให้เข้าพวกกับค่ายอื่น
        claude_answers.columns = [
            'claude-4.5-haiku_FOOD', 
            'claude-4.5-haiku_SERVICE', 
            'claude-4.5-haiku_ATMOS', 
            'claude-4.5-haiku_PRICE'
        ]
        
        # ลบคอลัมน์ Claude อันเก่าใน Master File ทิ้ง (ถ้ามีค้างอยู่ จะได้ไม่ซ้ำซ้อน)
        cols_to_drop = [col for col in df_master.columns if 'claude' in col.lower()]
        if cols_to_drop:
            df_master.drop(columns=cols_to_drop, inplace=True)
            
        # 3. เอามาต่อท้ายกัน (แกน Column)
        final_df = pd.concat([df_master, claude_answers], axis=1)
        
        # 4. เซฟทับไฟล์ Master 
        final_df.to_csv('Model_Comparison_Full_Results.csv', index=False, encoding='utf-8-sig')
        print("🎉 ประกอบร่างสำเร็จ! ไฟล์ Model_Comparison_Full_Results.csv มีข้อมูลครบ 3 ค่ายพร้อมประเมินผลแล้ว!")
        
    else:
        print("❌ จำนวนแถวไม่เท่ากันครับ! กรุณาตรวจสอบไฟล์ Anno_Claude.csv อีกครั้ง")

except Exception as e:
    print(f"❌ เกิดข้อผิดพลาด: {e}")