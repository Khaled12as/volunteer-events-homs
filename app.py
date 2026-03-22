import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from streamlit_lottie import st_lottie

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="تطوع في مكتب الفعاليات - كلية الهندسة الزراعية | جامعة حمص",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==================== CSS احترافي + ألوان الزراعة + حركات ====================
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        background: linear-gradient(to bottom, #E8F5E9, #F1F8E9);
        font-family: 'Arial', sans-serif;
    }
    .main-header {
        text-align: center;
        color: #2E7D32;
        font-size: 2.8rem;
        font-weight: bold;
        text-shadow: 2px 2px 10px rgba(46, 125, 50, 0.3);
        margin-bottom: 10px;
    }
    .form-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(46, 125, 50, 0.15);
        margin: 20px 0;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        height: 55px;
        font-size: 1.2rem;
        transition: all 0.4s ease;
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
    }
    .stButton > button:hover {
        background-color: #388E3C;
        transform: scale(1.08) rotate(2deg);
    }
    .success-msg {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# ==================== الشعار (استبدل المسار) ====================
logo_url = "https://i.postimg.cc/025Yjq3T/Logo.png"   # ← حط الرابط الحقيقي هنا
...
st.image(logo_url, width=180)

# ==================== تحميل الأنيميشن Lottie ====================
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

# أنيميشن نبات زراعي في البداية + احتفال
plant_lottie = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_2d9b3j.json")  # نبات ينمو
success_lottie = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_jrpz9l0u.json")  # علامة صح + احتفال

# ==================== الهيدر ====================
col1, col2 = st.columns([1, 4])
with col1:
    if logo_path:
        st.image(logo_path, width=180)
with col2:
    st.markdown('<h1 class="main-header">انضم إلى مكتب الفعاليات 🌱🎉</h1>', unsafe_allow_html=True)
    st.markdown("**كلية الهندسة الزراعية - جامعة حمص**")

st_lottie(plant_lottie, height=180, key="plant_header")

st.markdown("""
### مرحباً بك في فريق النشاط والترفيه!  
هنا تصنع الذكريات، تطور مهاراتك، وتساهم في أجمل الفعاليات الجامعية.  
اختر لجنتك وشاركنا طاقتك 🌾✨
""")

# ==================== النموذج ====================
st.markdown('<div class="form-card">', unsafe_allow_html=True)

with st.form("volunteer_form"):
    st.subheader("استبيان التطوع الرسمي")
    
    name = st.text_input("الاسم الثلاثي *", placeholder="أحمد محمد علي")
    year = st.selectbox("السنة الدراسية *", ["الأولى", "الثانية", "الثالثة", "الرابعة", "الخامسة"])
    phone = st.text_input("رقم الهاتف *", placeholder="0987654321")
    
    committees = st.multiselect(
        "اختر اللجان التي ترغب في التطوع بها *",
        ["لجنة التنظيم واللوجستيات", 
         "لجنة الإعلام والتسويق الرقمي", 
         "لجنة التصميم والديكور", 
         "لجنة البرامج والتكنولوجيا", 
         "لجنة الترفيه والأنشطة الثقافية"]
    )
    
    skills = st.text_area("المهارات والخبرات التي تمتلكها *", 
                         placeholder="مثال: تصميم جرافيك، تنظيم فعاليات، تصوير، برمجة، قيادة فريق...")

    submitted = st.form_submit_button("🚀 أرسل طلب التطوع الآن")

st.markdown('</div>', unsafe_allow_html=True)

# ==================== معالجة الإرسال ====================
data_file = "registrations.csv"

try:
    df = pd.read_csv(data_file)
except:
    df = pd.DataFrame(columns=["الاسم", "السنة", "رقم الهاتف", "اللجان", "المهارات", "تاريخ"])

if submitted:
    if name and year and phone and skills and committees:
        new_row = {
            "الاسم": name,
            "السنة": year,
            "رقم الهاتف": phone,
            "اللجان": ", ".join(committees),
            "المهارات": skills,
            "تاريخ": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(data_file, index=False)
        
        # الإيموشن الخارقة
        st.balloons()
        st_lottie(success_lottie, height=220, key="success_anim")
        
        st.markdown("""
        <h2 style="text-align:center; color:#2E7D32; animation: pulse 2s infinite;" class="success-msg">
            شكراً لتسجيلك! 🌱🎉<br>
            سنتواصل معك في أقرب وقت ممكن
        </h2>
        """, unsafe_allow_html=True)
        
    else:
        st.error("❌ يرجى ملء جميع الحقول المطلوبة")

# ==================== لوحة الإدارة (في الشريط الجانبي) ====================
st.sidebar.header("🔑 لوحة الإدارة")
admin_pass = st.sidebar.text_input("كلمة المرور الإدارية", type="password")

if admin_pass == "admin2025":  # ← غيّرها إلى كلمة سر قوية
    st.sidebar.success("✅ مرحباً بالإدارة!")
    if not df.empty:
        st.sidebar.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="📥 تحميل كل التسجيلات (CSV)",
            data=csv,
            file_name=f"تسجيلات_الفعاليات_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
else:
    st.sidebar.info("أدخل كلمة المرور لعرض البيانات")

st.sidebar.caption("صمم بحب لكلية الهندسة الزراعية - جامعة حمص ❤️🌾")
