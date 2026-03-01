import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

# โหลดไฟล์ที่ใช้รัน Excel เมื่อกี้
df = pd.read_csv('Final_Model_Data.csv')

# เลือกเฉพาะคอลัมน์ตัวแปรอิสระ X
X = df[['Avg_Food', 'Avg_Service', 'Avg_Atmos', 'Price_Level']].dropna()

# เพิ่มค่าคงที่ (Intercept) เข้าไปตามหลักสถิติ
X = add_constant(X)

# คำนวณ VIF
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

print(vif_data)