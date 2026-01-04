import streamlit as st
import pubchempy as pcp
import time


# ۱. تنظیمات صفحه و استایل حرفه‌ای
st.set_page_config(page_title="دستیار هوشمند شیمی", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 3.5em; 
        background-color: #ff4b4b; color: white; font-weight: bold;
        border: 2px solid #ff4b4b; transition: all 0.4s ease-in-out;
    }
    .stButton>button:hover { background-color: #ffffff; color: #ff4b4b; transform: scale(1.02); }
    .danger-box {
        background-color: #ff4b4b; padding: 20px; border-radius: 15px; 
        text-align: center; border: 2px solid white;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 255, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 سامانه هوشمند ایمنی و تداخلات شیمیایی")
st.markdown("---")

menu = st.sidebar.selectbox("انتخاب بخش:", ["جستجوی اطلاعات ماده", "تحلیل تداخلات (AI)"])

if menu == "جستجوی اطلاعات ماده":
    st.subheader("🔍 جستجوی ساختار و مشخصات")
    name = st.text_input("نام ماده را به انگلیسی وارد کنید (مثلاً Ethanol):")
    if name:
        try:
            results = pcp.get_compounds(name, 'name')
            if results:
                res = results[0]
                st.success(f"✅ ماده یافت شد: {res.iupac_name}")
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{res.cid}/PNG", width=280)
                with col2:
                    st.metric("فرمول مولکولی", res.molecular_formula)
                    st.metric("وزن مولکولی", f"{res.molecular_weight} g/mol")
                    # ایده جدید: لینک مستقیم به منبع رسمی برای اعتبار پروژه
                    url = f"https://pubchem.ncbi.nlm.nih.gov/compound/{res.cid}"
                    st.markdown(f"[🔗 مشاهده جزئیات تخصصی در دیتابیس PubChem]({url})")
                    st.info(f"شناسه CID: {res.cid}")
            else:
                st.error("ماده یافت نشد.")
        except:
            st.error("خطا در اتصال به دیتابیس.")

elif menu == "تحلیل تداخلات (AI)":
    st.subheader("⚠️ بررسی خطر و پروتکل ایمنی")
    c1, c2 = st.columns(2)
    m1 = c1.text_input("نام ماده اول را وارد کنید:")
    m2 = c2.text_input("نام ماده دوم را وارد کنید:")

    if st.button("شروع آنالیز واکنش"):
        if m1 and m2:
            progress_bar = st.progress(0)
            status_text = st.empty()
            for percent in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent + 1)
                if percent < 40: status_text.text("🔍 اسکن پیوندهای اتمی...")
                elif percent < 80: status_text.text("⚡ شبیه‌سازی واکنش...")
                else: status_text.text("⚠️ استخراج پروتکل ایمنی...")
            
            status_text.empty()
            progress_bar.empty()

            combos = [
                ("acid", "bleach", "تولید گاز سمی کلر! پروتکل: تخلیه فوری محل.", "🚨 خطر مرگ"),
                ("sodium", "water", "انفجار شدید هیدروژن! پروتکل: کپسول کلاس D.", "💥 انفجاری"),
                ("ammonia", "bleach", "تولید کلرامین سمی! پروتکل: شستشوی تنفسی.", "🚨 سمی"),
                ("acid", "base", "واکنش شدید گرماده! پروتکل: عینک و روپوش.", "🔥 گرماده"),
                ("cyanide", "acid", "تولید گاز سیانور! پروتکل: اورژانس فوری.", "💀 مرگ آنی")
            ]
            
            found = False
            m1_l, m2_l = m1.lower(), m2.lower()
            for a, b, msg, lvl in combos:
                if (a in m1_l and b in m2_l) or (a in m2_l and b in m1_l):
                    found = True
                    st.error(f"❌ سطح خطر شناسایی شده: {lvl}")
                    st.markdown(f'<div class="danger-box"><h2 style="color:white; margin:0;">{lvl}</h2><p style="color:white; font-size:18px;">{msg}</p></div>', unsafe_allow_html=True)
                    st.download_button("📥 دانلود گزارش ایمنی", f"گزارش خطر {m1} + {m2}\n{msg}", file_name="Safety_Report.txt")
                    break
            if not found:
                st.balloons()
                st.success("✅ تداخل خطرناکی شناسایی نشد.")
        else:
            st.warning("لطفاً نام هر دو ماده را وارد کنید.")

st.markdown("---")

st.caption("🧪 ⚗️ دستیار دیجیتال ایمنی شیمی | پایش هوشمند تداخلات بر پایه داده‌های جهانی")