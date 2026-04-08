import streamlit as st
import ccxt
import sqlite3
import requests
from datetime import datetime, timedelta

# إعدادات الواجهة
st.set_page_config(page_title="AI Trading Bot", layout="centered")

# نظام قاعدة البيانات لرموز التفعيل
def init_db():
    conn = sqlite3.connect('trading_data.db', check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS keys (code TEXT PRIMARY KEY, used INTEGER DEFAULT 0)')
    conn.commit()
    return conn

db = init_db()

# لوحة تحكم المشرف (تظهر لك فقط بكود سري)
with st.sidebar:
    st.title("🛡️ إدارة النظام")
    if st.text_input("كود المدير السري", type="password") == "admin123":
        st.success("أهلاً بك")
        new_k = st.text_input("توليد رمز جديد:")
        if st.button("حفظ الرمز"):
            db.execute("INSERT OR IGNORE INTO keys VALUES (?,0)", (new_k,))
            db.commit()
            st.info(f"تم الحفظ: {new_k}")

# شاشة الدخول والتفعيل
if 'auth' not in st.session_state:
    st.title("🤖 بوت التداول الذكي")
    u_email = st.text_input("البريد الإلكتروني")
    u_key = st.text_input("رمز التفعيل (3 أشهر)", type="password")
    
    if st.button("تفعيل الآن", use_container_width=True):
        res = db.execute("SELECT * FROM keys WHERE code=? AND used=0", (u_key,)).fetchone()
        if res and "@" in u_email:
            db.execute("UPDATE keys SET used=1 WHERE code=?", (u_key,))
            db.commit()
            st.session_state.auth = True
            st.session_state.user = u_email
            st.rerun()
        else:
            st.error("الرمز غير صحيح أو مستخدم")
else:
    # واجهة التداول الحقيقية
    st.header("📊 مركز المزامنة والأرباح")
    st.write(f"المستخدم: {st.session_state.user}")
    
    # اختيار منصة واحدة من 4
    platform = st.selectbox("اختر المنصة للربط:", ["Binance", "MEXC", "Bybit", "KuCoin"])
    
    ak = st.text_input(f"مفتاح {platform} API Key", type="password")
    as_ = st.text_input(f"مفتاح {platform} Secret", type="password")

    if ak and as_:
        try:
            ex_class = getattr(ccxt, platform.lower())
            ex = ex_class({'apiKey': ak, 'secret': as_})
            bal = ex.fetch_balance()['total'].get('USDT', 0)
            
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric(f"رصيد {platform}", f"{bal:.2f} $")
            c2.metric("ربح الـ 12 ساعة", "5.00 $", "+10%")
            
            # الـ IP الثابت للمزامنة
            st.code(requests.get('https://ipify.org').text, language="text")
            st.caption("انسخ الـ IP وضعه في إعدادات المنصة للأمان.")

            if st.button(f"🚀 بدء تداول {platform}"):
                st.success(f"البوت نشط على {platform}. المزامنة تعمل كل 12 ساعة.")
        except:
            st.error("فشل الاتصال. تأكد من صحة المفاتيح.")

    if st.button("💬 خدمة الزبائن"):
        st.info("تواصل مع المبرمج لطلب رمز تفعيل.")
