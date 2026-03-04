import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import f1_score

print("📊 กำลังสร้างกราฟสรุปผลแบบ 'ง่ายและชัดเจน'...")

# 1. โหลดข้อมูล
df = pd.read_csv('Model_Comparison_Full_Results.csv')
ASPECTS = ['FOOD', 'SERVICE', 'ATMOS', 'PRICE']
MODELS = {
    'Gemini 2.5 Flash': 'gemini-2.5-flash',
    'Claude 4.5 Haiku': 'claude-4.5-haiku',
    'ChatGPT (4o-mini)': 'gpt-4o-mini'
}
LABELS = ['POS', 'NEG', 'NEU', 'N/A']

# 2. คำนวณคะแนน F1-Score
results = []
for aspect in ASPECTS:
    true_col = f'Actual_{aspect}'
    if true_col not in df.columns: continue
    y_true = df[true_col].fillna('N/A').astype(str).str.upper().str.strip()

    for model_name, model_prefix in MODELS.items():
        pred_col = f'{model_prefix}_{aspect}'
        if pred_col not in df.columns: continue
        y_pred = df[pred_col].fillna('N/A').astype(str).str.upper().str.strip()
        y_pred = y_pred.apply(lambda x: x if x in LABELS else 'N/A')

        f1 = f1_score(y_true, y_pred, labels=LABELS, average='macro', zero_division=0)
        results.append({'Aspect': aspect, 'Model': model_name, 'F1_Score': f1})

df_metrics = pd.DataFrame(results)

# 3. วาดกราฟแท่งแบบมีตัวเลขกำกับ (Simple & Clear)
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid") # พื้นหลังตารางสะอาดๆ

# วาดกราฟ
ax = sns.barplot(data=df_metrics, x='Aspect', y='F1_Score', hue='Model', palette=['#1f77b4', '#ff7f0e', '#2ca02c'])

# เพิ่มตัวเลขบนยอดแท่งกราฟ
for container in ax.containers:
    ax.bar_label(container, fmt='%.3f', padding=3, fontsize=10, fontweight='bold')

# ตกแต่งความสวยงาม
plt.title('Performance Summary of AI Models (Macro F1-Score)', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Macro F1-Score', fontsize=12, fontweight='bold')
plt.xlabel('Restaurant Aspect', fontsize=12, fontweight='bold')
plt.ylim(0, 1.0) # ล็อกแกน Y ให้สูงสุดที่ 1.0 (คะแนนเต็ม)
plt.legend(title='AI Models', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('Final_Result_BarChart.png', dpi=300)
print("✅ เสร็จเรียบร้อย! สร้างไฟล์ Final_Result_BarChart.png ให้แล้วครับ")