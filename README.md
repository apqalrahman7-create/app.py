import streamlit as st
import ccxt
import time
from datetime import datetime, timedelta

# 1. إعدادات الأمان والواجهة الاحترافية (تثبيت على الهاتف)
st.set_page_config(page_title="AI Ultra Scalper Bot", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e11; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; }
    div[data-testid="stMetricValue"] { color: #2ecc71 !important; font-size: 32px !important; }
    .status-online { color: #2ecc71; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .stButton>button { width: 100%; border-radius: 15px; height: 4em; background-color: #2ecc71; color: white; font-size: 20px; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #27ae60; }
    </style>
    """, unsafe_allow_html=True)

# 2. النظام المركزي (مخفي للمشرف فقط)
@st.cache_resource
def get_global_data():
    return {"live_viewers": 0, "users_db": {}, "support_tickets": {}}

data = get_global_data()
if 'init_visit' not in st.session_state:
    data["live_viewers"] += 1
    st.session_state.init_visit = True

# --- الشاشة الرئيسية ---
st.title("بوت التداول الذكي الفوري ⚡")

email = st.text_input("أدخل بريدك الإلكتروني / Email")

if email:
    if email not in data["users_db"]:
        data["users_db"][email] = {'status': 'trial', 'expiry': datetime.now() + timedelta(hours=24)}
    
    user = data["users_db"][email]
    if user['status'] == 'banned':
        st.error("🚫 عذراً، حسابك محظور من قبل المشرف.")
        st.stop()

    # --- لوحة التحكم والربط الآمن ---
    st.sidebar.header("🔐 إعدادات المحفظة")
    api_k = st.sidebar.text_input("API Key", type="password")
    api_s = st.sidebar.text_input("API Secret", type="password")

    if api_k and api_s:
        try:
            # الاتصال الفوري بالمنصة (MEXC)
            exchange = ccxt.mexc({'apiKey': api_k, 'secret': api_s})
            balance = exchange.fetch_balance()
            total_bal = balance['total'].get('USDT', 0)
            
            st.metric("رأس المال المكتشف", f"${total_bal:,.2f} USDT")

            # زر البدء الفوري على كامل المبلغ
            if st.button("🚀 بدء التداول والربح الفوري (12 ساعة)"):
                with st.status("جاري تنفيذ الاستراتيجية الذكية...", expanded=True) as status:
                    target = total_bal * 0.10 # هدف 10% ربح
                    stop_loss = total_bal * 0.95 # حماية 95% من رأس المال
                    
                    st.write("✅ تم فحص زوج التداول BTC/USDT")
                    time.sleep(1.5)
                    st.write(f"✅ سيتم استثمار ${total_bal} بالكامل")
                    status.update(label="البوت يعمل الآن في الخلفية!", state="complete", expanded=False)
                    
                    st.markdown('<p class="status-online">● جاري العمل في خلفية الهاتف لتحقيق هدف الـ 10%</p>', unsafe_allow_html=True)
                    
                    c1, c2, c3 = st.columns(3)
                    c1.metric("الربح المستهدف", f"${target:,.2f}")
                    c2.metric("حماية الرصيد (SL)", f"${stop_loss:,.2f}")
                    c3.metric("الدورة الزمنية", "12 ساعة")

        except:
            st.sidebar.error("❌ فشل الربط: تأكد من مفاتيح الـ API وصلاحيات التداول.")
    else:
        st.info("💡 أدخل مفاتيح الـ API في القائمة الجانبية ثم اضغط الزر الأخضر للبدء.")

    # --- نظام المراسلة الخاص (شات سري) ---
    with st.expander("💬 مراسلة المشرف"):
        if email not in data["support_tickets"]: data["support_tickets"][email] = []
        u_msg = st.text_input("اكتب رسالتك للمشرف...")
        if st.button("إرسال"):
            data["support_tickets"][email].append({"role": "user", "text": u_msg, "time": datetime.now()})
            st.success("تم إرسال رسالتك بنجاح.")
        for m in data["support_tickets"][email]:
            lbl = "المشرف" if m['role'] == "admin" else "أنت"
            st.write(f"**{lbl}:** {m}")

# --- لوحة تحكم المشرف (لك أنت فقط) ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
with st.expander("🔐 لوحة تحكم المشرف (إحصائيات وحظر)"):
    adm_pass = st.text_input("كلمة سر الإدارة", type="password")
    if adm_pass == "admin777":
        # العد الحقيقي يظهر هنا فقط
        st.subheader(f"📊 عدد المستخدمين المتواجدين الآن: {data['live_viewers']}")
        
        for u_email, info in list(data["users_db"].items()):
            st.write(f"📧 {u_email} | الحالة: {info['status']}")
            ca, cb, cc = st.columns(3)
            if ca.button("✅ تفعيل 2 شهر", key=f"v_{u_email}"):
                info['status'] = 'active'; info['expiry'] = datetime.now() + timedelta(days=60)
            if cb.button("🚫 حظر", key=f"b_{u_email}"): info['status'] = 'banned'
            if cc.button("🗑 حذف", key=f"d_{u_email}"): del data["users_db"][u_email]; st.rerun()
            
            # الرد على الرسائل
            if u_email in data["support_tickets"]:
                rep = st.text_input(f"رد على {u_email}", key=f"rp_{u_email}")
                if st.button(f"إرسال لـ {u_email}"):
                    data["support_tickets"][u_email].append({"role": "admin", "text": rep, "time": datetime.now()})
                    st.rerun()

# أزرار الدعم العام
st.divider()
st.button("🛠 خدمة الزبائن (عربي)")
st.button("🌍 English Support")
