import pandas as pd
from sklearn.metrics import f1_score, accuracy_score, classification_report
import warnings

warnings.filterwarnings('ignore')

# 🚨 พระเอกขี่ม้าขาวอยู่ตรงนี้ครับ: keep_default_na=False
df_gold = pd.read_csv('Gold_Standard_Final.csv', keep_default_na=False)
models = {
    'Gemini 1.5 Flash': pd.read_csv('Anno_Gemini.csv', keep_default_na=False),
    'ChatGPT (Free)': pd.read_csv('Anno_ChatGPT.csv', keep_default_na=False),
    'Claude 3.5 Haiku': pd.read_csv('Anno_Claude.csv', keep_default_na=False)
}

aspect_mapping = {'human_food': 'FOOD', 'human_service': 'SERVICE', 'human_atmos': 'ATMOS', 'human_price': 'PRICE'}

for model_name, df_pred in models.items():
    print(f"\n" + "="*50)
    print(f"🤖 ผลสอบของ: {model_name}")
    print("="*50)
    
    y_true_all = []
    y_pred_all = []
    
    for gold_col, pred_col in aspect_mapping.items():
        y_true = df_gold[gold_col].astype(str).str.strip().str.upper()
        y_pred = df_pred[pred_col].astype(str).str.strip().str.upper()
        
        y_true_all.extend(y_true)
        y_pred_all.extend(y_pred)
    
    acc = accuracy_score(y_true_all, y_pred_all)
    macro_f1 = f1_score(y_true_all, y_pred_all, average='macro', labels=['POS', 'NEG', 'NEU', 'N/A'])
    
    print(f"🎯 ความแม่นยำรวม (Accuracy): {acc:.4f} ({acc*100:.2f}%)")
    print(f"📊 Average Macro F1: {macro_f1:.4f}")
    print("-" * 50)
    print("เจาะลึกคะแนนรายคลาส (Classification Report):")
    print(classification_report(y_true_all, y_pred_all, labels=['POS', 'NEG', 'NEU', 'N/A']))