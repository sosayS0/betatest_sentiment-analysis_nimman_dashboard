import pandas as pd
from sklearn.metrics import confusion_matrix
import warnings

warnings.filterwarnings('ignore')

# 1. โหลดข้อมูล (อย่าลืม keep_default_na=False ป้องกันบั๊ก N/A)
df_gold = pd.read_excel('Gold_Standard_Final.xlsx', keep_default_na=False)
models = {
    'Gemini 1.5 Flash': pd.read_csv('Anno_Gemini.csv', keep_default_na=False),
    'ChatGPT (Free)': pd.read_csv('Anno_ChatGPT.csv', keep_default_na=False),
    'Claude 3.5 Haiku': pd.read_csv('Anno_Claude.csv', keep_default_na=False)
}

aspect_mapping = {'human_food': 'FOOD', 'human_service': 'SERVICE', 'human_atmos': 'ATMOS', 'human_price': 'PRICE'}
labels_order = ['POS', 'NEG', 'NEU', 'N/A']

print("="*60)
print("🔍 ชำแหละพฤติกรรม AI ด้วย CONFUSION MATRIX")
print("="*60)

for model_name, df_pred in models.items():
    print(f"\n🤖 โมเดล: {model_name}")
    print("-" * 50)
    
    y_true_all = []
    y_pred_all = []
    
    # รวบรวมข้อมูลทั้ง 4 แกนมาต่อกัน
    for gold_col, pred_col in aspect_mapping.items():
        y_true_all.extend(df_gold[gold_col].astype(str).str.strip().str.upper())
        y_pred_all.extend(df_pred[pred_col].astype(str).str.strip().str.upper())
    
    # สร้าง Confusion Matrix
    cm = confusion_matrix(y_true_all, y_pred_all, labels=labels_order)
    
    # แปลงเป็น DataFrame ให้ดูง่ายๆ
    cm_df = pd.DataFrame(cm, 
                         index=['(คนเฉลย) True POS', '(คนเฉลย) True NEG', '(คนเฉลย) True NEU', '(คนเฉลย) True N/A'],
                         columns=['(AI ทาย) Pred POS', '(AI ทาย) Pred NEG', '(AI ทาย) Pred NEU', '(AI ทาย) Pred N/A'])
    
    print(cm_df)

print("\n" + "="*60)
print("💡 วิธีอ่าน: ให้ดูที่แถว '(คนเฉลย) True NEU' ว่าตัวเลขมันกระจายไปตกที่คอลัมน์ไหนของ AI มากที่สุด!")
print("="*60)