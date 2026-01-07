import streamlit as st
import pubchempy as pcp
import time
import qrcode
from io import BytesIO

# ۱. تنظیمات صفحه و استایل حرفه‌ای
st.set_page_config(page_title="دستیار هوشمند شیمی", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* انیمیشن پالس برای باکس خطر */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
        70% { transform: scale(1.02); box-shadow: 0 0 0 10px rgba(255, 75, 75, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
    }
    
    .stButton>button {
        width: 100%; border-radius: 15px; height: 3.5em;
        background-color: #ff4b4b; color: white; font-weight: bold;
        border: 2px solid #ff4b4b; transition: all 0.4s ease-in-out;
    }
    
    .stButton>button:hover { 
        background-color: #ffffff; color: #ff4b4b; 
        transform: scale(1.05); border: 2px solid #ff4b4b;
    }
    
    .danger-box {
        padding: 25px; border-radius: 15px; border: 3px dashed #ff4b4b;
        background-color: rgba(255, 75, 75, 0.15); text-align: center;
        animation: pulse 2s infinite; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ۲. منوی سمت چپ و QR Code
st.sidebar.header("🧪 پنل مدیریت پروژه")
choice = st.sidebar.selectbox("انتخاب بخش کاری:", ["جستجوی اطلاعات ماده", "تحلیل تداخلات خطرناک"])

st.sidebar.markdown("---")
st.sidebar.subheader("📱 دسترسی سریع موبایل")
site_url = "https://cheraghpour-hasani-lab.streamlit.app"
qr_img = qrcode.make(site_url)
buf = BytesIO()
qr_img.save(buf, format="PNG")
buf.seek(0)
st.sidebar.image(buf, caption="اسکن کنید و روی موبایل باز کنید")

# ۳. بدنه اصلی برنامه
st.title("🧪 سامانه هوشمند ایمنی و تداخلات شیمیایی")

if choice == "جستجوی اطلاعات ماده":
    st.subheader("🔍 جستجوی ساختار و مشخصات در دیتابیس جهانی")
    compound_name = st.text_input("نام انگلیسی ماده (مثلاً Benzene):")
    
    if compound_name:
        try:
            compounds = pcp.get_compounds(compound_name, 'name')
            if compounds:
                c = compounds[0]
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"✅ اطلاعات {compound_name} استخراج شد")
                    st.write(f"**فرمول:** {c.molecular_formula}")
                    st.write(f"**وزن مولکولی:** {c.molecular_weight}")
                    st.markdown(f"🔗 [مشاهده جزئیات کامل در PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/{c.cid})")
                with col2:
                    st.image(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{c.cid}/PNG")
            else:
                st.error("❌ ماده یافت نشد.")
        except:
            st.error("⚠️ خطا در اتصال به دیتابیس.")

elif choice == "تحلیل تداخلات خطرناک":
    st.subheader("⚠️ آنالیز هوشمند تداخلات")
    m1 = st.text_input("نام ماده اول (مثلاً Acid):")
    m2 = st.text_input("نام ماده دوم (مثلاً Bleach):")
    
    if st.button("شروع آنالیز ایمنی"):
        if m1 and m2:
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # تبدیل به حروف کوچک برای مقایسه دقیق
            m1_l, m2_l = m1.lower().strip(), m2.lower().strip()
            
            # تعریف لیست خطرات با منطق منعطف
            hazards = [
                ({"acid", "bleach"}, "تولید گاز کلر بسیار سمی و کشنده", "سطح خطر: بسیار بالا"),
                ({"sodium", "water"}, "واکنش انفجاری سریع و آزاد شدن هیدروژن", "سطح خطر: بحرانی"),
                ({"acid", "base"}, "واکنش شدید گرمازا و احتمال پاشش مواد", "سطح خطر: متوسط")
            ]
            
            found = False
            user_input_set = {m1_l, m2_l}
            
            for hazard_set, msg, lvl in hazards:
                # چک کردن اینکه آیا هر دو ماده ورودی در مجموعه خطر هستند یا خیر
                if hazard_set.issubset(user_input_set) or hazard_set == user_input_set:
                    found = True
                    st.error(f"❌ {lvl}")
                    st.markdown(f'''
                        <div class="danger-box">
                            <h2 style="color:#ff4b4b; margin:0;">{lvl}</h2>
                            <p style="color:white; font-size:1.3em; font-weight:bold;">{msg}</p>
                        </div>
                    ''', unsafe_allow_html=True)
                    st.download_button("📥 دریافت گزارش ایمنی", f"هشدار تداخل: ترکیب {m1} و {m2} خطرناک است.\nعلت: {msg}", file_name="Safety_Report.txt")
                    break
            
            if not found:
                st.balloons()
                st.success("✅ تداخل خطرناکی بین این دو ماده در دیتابیس ثبت نشده است.")
        else:
            st.warning("لطفاً نام هر دو ماده را وارد کنید.")

st.markdown("---")

st.caption("🧪 سامانه پایش ایمنی | طراحی شده با Python برای محیط‌های آزمایشگاهی هوشمند")
