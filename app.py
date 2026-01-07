import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION (ตั้งค่าหน้าเว็บ)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Nimman Insights Dashboard",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS เพื่อความสวยงาม (ปรับ Font และสี)
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stProgress > div > div > div > div {
        background-color: #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. MOCK DATA (จำลองข้อมูลรีวิว)
# ---------------------------------------------------------
# ในโปรเจกต์จริง ข้อมูลตรงนี้จะมาจากการ Load CSV ที่ได้จาก Project 2
def get_mock_data():
    data = {
        "Shop A (Kua Gai Nimman)": {
            "reviews": 142,
            "rating": 4.2,
            "sentiment_score": 3.8,
            "sentiment_trend": -5,
            "price_level": "฿฿",
            "aspects": {"Food": 4.5, "Atmosphere": 3.2, "Service": 2.1, "Value": 4.0},
            "complaints": ["Staff ignores customers", "Food served slowly", "No parking space"]
        },
        "Shop B (Khao Soi Mae Sai)": {
            "reviews": 320,
            "rating": 4.8,
            "sentiment_score": 4.6,
            "sentiment_trend": +12,
            "price_level": "฿",
            "aspects": {"Food": 4.8, "Atmosphere": 4.0, "Service": 4.2, "Value": 4.9},
            "complaints": ["Queue is too long", "Too spicy", "Crowded"]
        },
        "Shop C (Tong Tem Toh)": {
            "reviews": 510,
            "rating": 4.0,
            "sentiment_score": 3.5,
            "sentiment_trend": -2,
            "price_level": "฿฿฿",
            "aspects": {"Food": 4.1, "Atmosphere": 4.5, "Service": 3.0, "Value": 3.2},
            "complaints": ["Expensive", "Small portion", "Loud music"]
        }
    }
    return data

data = get_mock_data()

# ---------------------------------------------------------
# 3. SIDEBAR (แถบเมนูซ้ายมือ)
# ---------------------------------------------------------
with st.sidebar:
    st.title("🦁 NIMMAN INSIGHTS")
    st.caption("Econ CMU Cooperative Project")
    
    st.markdown("---")
    
    # Dropdown เลือกร้าน
    selected_shop = st.selectbox(
        "Select Restaurant:",
        options=list(data.keys())
    )
    
    # ตัวเลือกช่วงเวลา (Simulation)
    data_range = st.radio(
        "Data Range:",
        ["Last 3 Months", "Last 6 Months", "Last 1 Year (Auto)"]
    )
    
    st.markdown("---")
    st.info("💡 **Model Info:**\n\nNLP Engine: WangchanBERTa\nRegression: OLS Hedonic Pricing")
    
    # ปุ่มกด (หลอกๆ เพื่อความ Interactive)
    if st.button("Refresh Data 🔄"):
        st.success("Data Updated!")

# ดึงข้อมูลร้านที่เลือกมาแสดง
shop_data = data[selected_shop]

# ---------------------------------------------------------
# 4. MAIN DASHBOARD (หน้าจอหลัก)
# ---------------------------------------------------------

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title(f"📊 Analysis: {selected_shop.split('(')[0]}")
    st.markdown(f"📍 **Location:** Nimman Soi 17 | 💰 **Price Level:** {shop_data['price_level']} | 📅 **Reviews:** {shop_data['reviews']} items")

with col2:
    st.markdown("### Price Perception Status")
    if shop_data['aspects']['Value'] >= 4.0:
        st.success("✅ **HIGH VALUE**")
    elif shop_data['aspects']['Value'] >= 3.0:
        st.warning("⚠️ **MODERATE**")
    else:
        st.error("❌ **LOW VALUE**")

st.markdown("---")

# --- KPI CARDS (Interactive Metrics) ---
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        label="⭐ Google Rating",
        value=f"{shop_data['rating']} / 5.0",
        delta="0.1"
    )

with c2:
    st.metric(
        label="❤️ AI Sentiment Score",
        value=f"{shop_data['sentiment_score']} / 5.0",
        delta=f"{shop_data['sentiment_trend']}% vs last month",
        delta_color="normal" if shop_data['sentiment_trend'] > 0 else "inverse"
    )

with c3:
    st.metric(
        label="💰 Value Score",
        value=f"{shop_data['aspects']['Value']} / 5.0",
        help="Calculated from Hedonic Pricing Model"
    )

with c4:
    # แสดง Aspect ที่แย่ที่สุด
    min_aspect = min(shop_data['aspects'], key=shop_data['aspects'].get)
    st.metric(
        label="🚨 Weakest Point",
        value=min_aspect,
        delta=f"Score: {shop_data['aspects'][min_aspect]}",
        delta_color="inverse"
    )

# --- CHARTS SECTION (Interactive Plotly Charts) ---

tab1, tab2 = st.tabs(["📈 Aspect Analysis", "💬 Customer Voice"])

with tab1:
    st.subheader("Deep Dive: Why do customers feel this way?")
    
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        # Create Bar Chart
        df_aspects = pd.DataFrame({
            "Aspect": list(shop_data['aspects'].keys()),
            "Score": list(shop_data['aspects'].values())
        })
        
        fig_bar = px.bar(
            df_aspects, 
            x="Score", 
            y="Aspect", 
            orientation='h', 
            color="Score",
            color_continuous_scale=["red", "yellow", "green"],
            range_x=[0, 5],
            text_auto=True,
            title="Sentiment Score by Aspect (AI Detected)"
        )
        fig_bar.update_layout(height=350)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_chart2:
        # Create Radar Chart (Spider Web)
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=list(shop_data['aspects'].values()),
            theta=list(shop_data['aspects'].keys()),
            fill='toself',
            name=selected_shop
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=False,
            title="Performance Radar",
            height=350
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # --- AI RECOMMENDATION BOX ---
    st.markdown("### 💡 AI Strategic Suggestion")
    
    # Logic จำลอง (Project 2 Result Simulation)
    if shop_data['aspects']['Service'] < 3.0:
        st.error(f"""
        **🔴 CRITICAL ACTION REQUIRED: IMPROVE SERVICE**
        
        จากการวิเคราะห์ Regression Model พบว่า **"Service"** มีค่า Beta สูงถึง **0.45** (มีผลต่อความคุ้มค่ามากที่สุด)
        แต่คะแนนปัจจุบันอยู่ที่ **{shop_data['aspects']['Service']}** ซึ่งต่ำกว่าค่าเฉลี่ยตลาด (Benchmark 3.5)
        
        **แนะนำ:**
        1. เพิ่มพนักงานช่วง Peak Hour (18:00 - 20:00)
        2. ปรับปรุงระบบคิวเพื่อลดความหงุดหงิด
        """)
    elif shop_data['aspects']['Food'] < 4.0:
        st.warning("""
        **🟡 WARNING: FOOD CONSISTENCY**
        ลูกค้าเริ่มบ่นเรื่องรสชาติที่ไม่นิ่ง แนะนำให้ตรวจสอบ QC ในครัว
        """)
    else:
        st.success("""
        **🟢 EXCELLENT PERFORMANCE**
        ร้านของคุณทำได้ดีมาก! สามารถพิจารณา **"ปรับราคาขึ้น (Price Premium)"** ได้ 5-10% เนื่องจาก Value Score สูงมาก
        """)

with tab2:
    st.subheader("Top Complaints (Voice of Customer)")
    
    # แสดงคำบ่น
    for i, complaint in enumerate(shop_data['complaints']):
        st.info(f"🗣️ **Customer {i+1}:** \"{complaint}\"")
    
    st.markdown("---")
    st.caption("*Data scraping from Google Maps Reviews (Last updated: Today)*")