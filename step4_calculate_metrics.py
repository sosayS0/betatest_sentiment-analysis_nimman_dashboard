import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, f1_score

# 1. โหลดข้อมูลผลการทดสอบ
INPUT_FILE = 'Model_Comparison_Full_Results.csv'
try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    print(f"🚨 ไม่พบไฟล์ {INPUT_FILE} ตรวจสอบให้แน่ใจว่าอยู่ในโฟลเดอร์เดียวกันครับ")
    exit()

# กำหนดตัวแปร
ASPECTS = ['FOOD', 'SERVICE', 'ATMOS', 'PRICE']
MODELS = ['gemini-2.5-flash', 'gpt-4o-mini']
LABELS = ['POS', 'NEG', 'NEU', 'N/A'] # ลำดับคลาสที่จะใช้โชว์ในกราฟ

# เตรียมตารางเก็บผลคะแนนรวม
summary_metrics = []

# ตั้งค่าฟอนต์กราฟให้รองรับภาษาไทย (ถ้าจำเป็น) และปรับสไตล์
plt.rcParams['font.sans-serif'] = ['Tahoma', 'Arial Unicode MS', 'sans-serif']
sns.set_theme(style="whitegrid")

# สร้าง Figure แผ่นใหญ่สำหรับวาด Confusion Matrix (2 แถว x 4 คอลัมน์)
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(20, 10))
fig.suptitle('Confusion Matrices: Gemini 2.5 Flash vs GPT-4o-mini', fontsize=20, fontweight='bold', y=1.02)

print("="*60)
print("📊 เริ่มคำนวณ F1-Score และสร้าง Confusion Matrix")
print("="*60)

# 2. ลูปคำนวณทีละโมเดล และทีละ Aspect
for row_idx, model in enumerate(MODELS):
    print(f"\n🚀 สรุปผลงานของ: {model}")
    print("-" * 40)
    
    all_actual = []
    all_pred = []
    
    for col_idx, aspect in enumerate(ASPECTS):
        actual_col = f"Actual_{aspect}"
        pred_col = f"{model}_{aspect}"
        
        # ดึงข้อมูลมาคลีน (เผื่อมีค่าว่าง)
        y_true = df[actual_col].fillna('N/A').astype(str).str.strip().str.upper()
        y_pred = df[pred_col].fillna('N/A').astype(str).str.strip().str.upper()
        
        # เก็บสะสมไว้คิดภาพรวม (Overall) ของโมเดลนั้นๆ
        all_actual.extend(y_true)
        all_pred.extend(y_pred)
        
        # --- สร้าง Confusion Matrix สำหรับ Aspect นี้ ---
        cm = confusion_matrix(y_true, y_pred, labels=LABELS)
        
        # วาดกราฟลงใน Subplot ที่กำหนด
        ax = axes[row_idx, col_idx]
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues' if row_idx==0 else 'Oranges', 
                    xticklabels=LABELS, yticklabels=LABELS, ax=ax, cbar=False)
        ax.set_title(f"{model} - {aspect}", fontsize=12, fontweight='bold')
        if col_idx == 0:
            ax.set_ylabel('Actual (เฉลย)', fontsize=10)
        if row_idx == 1:
            ax.set_xlabel('Predicted (คำทำนาย)', fontsize=10)
            
        # คำนวณ F1-Score (Macro) เฉพาะมิตินี้
        f1 = f1_score(y_true, y_pred, labels=LABELS, average='macro', zero_division=0)
        summary_metrics.append({
            'Model': model,
            'Aspect': aspect,
            'F1_Macro': round(f1, 4)
        })

    # --- คำนวณภาพรวม (Overall) ของโมเดล ---
    overall_f1 = f1_score(all_actual, all_pred, labels=LABELS, average='macro', zero_division=0)
    summary_metrics.append({
        'Model': model,
        'Aspect': 'OVERALL (รวม 4 มิติ)',
        'F1_Macro': round(overall_f1, 4)
    })
    
    print(classification_report(all_actual, all_pred, labels=LABELS, zero_division=0))

# 3. เซฟรูปกราฟ
plt.tight_layout()
plot_filename = 'Final_Confusion_Matrices.png'
plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
print(f"📸 บันทึกรูปกราฟ Confusion Matrix สำเร็จ: {plot_filename}")

# 4. เซฟตารางสรุปคะแนน
metrics_df = pd.DataFrame(summary_metrics)
# หมุนตารางให้ดูง่ายขึ้น (Pivot)
pivot_df = metrics_df.pivot(index='Aspect', columns='Model', values='F1_Macro')
pivot_df = pivot_df.reindex(['FOOD', 'SERVICE', 'ATMOS', 'PRICE', 'OVERALL (รวม 4 มิติ)'])

csv_filename = 'Final_F1_Scores_Summary.csv'
pivot_df.to_csv(csv_filename, encoding='utf-8-sig')

print("\n🏆 ตารางเปรียบเทียบ F1-Score (Macro) สุดท้าย:")
print("="*40)
print(pivot_df)
print("="*40)
print(f"💾 บันทึกตารางสรุปคะแนนสำเร็จ: {csv_filename}")
print("\n🎉 MISSION COMPLETE! นำกราฟและตารางไปใส่เล่มโปรเจกต์ได้เลยครับ!")