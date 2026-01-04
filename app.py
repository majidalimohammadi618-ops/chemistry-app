import streamlit as st
import pubchempy as pcp
import time
import qrcode
from io import BytesIO

# تنظیمات اصلی صفحه
st.set_page_config(page_title="دستیار هوشمند شیمی", page_icon="🧪", layout="wide")

# استایل‌دهی ظاهری
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%; border-radius: 15px; height: 3.5em;
        background-color: #ff4b4b; color: white; font-weight: bold;
        border: 2px solid #ff4b4b; transition: all 0.4s ease-in-out;
    }
    .stButton>button:hover { background-color: #ffffff; color: #ff4b4b; transform: scale(1.05); }
    .danger-box {
        padding: 20px; border-radius: 10px; border: 2px dashed #ff4b4b;
        background-color: rgba(255, 75, 75, 0.1); text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- بخش منوی سمت چپ (Sidebar) ---
st.sidebar.header("🧪 پنل مدیریت پروژه")
choice = st.sidebar.selectbox("انتخاب بخش کاری:", ["جستجوی اطلاعات ماده", "تحلیل تداخلات خطرناک"])

# بخش QR Code (نسخه اصلاح شده با buf.seek)
st.sidebar.markdown("---")
st.sidebar.subheader("📱 دسترسی سریع موبایل")

site_url = "https://chemistry-app-3thnjf2avnzzwhjtr9chdb.streamlit.app"
qr_img = qrcode.make(site_url)
buf = BytesIO()
qr_img.save(buf, format="PNG")
buf.seek(0)  # خط حیاتی برای نمایش صحیح تصویر در سایت

st.sidebar.image(buf, caption="اسکن کنید و روی موبایل باز کنید")

# --- محتوای اصلی برنامه ---
st.title("🧪 سامانه هوشمند ایمنی و تداخلات شیمیایی")

if choice == "جستجوی اطلاعات ماده":
    st.subheader("🔍 جستجوی ساختار و مشخصات")
    compound_name = st.text_input("نام انگلیسی ماده (مثلاً Aspirin):")
    
    if compound_name:
        try:
            compounds = pcp.get_compounds(compound_name, 'name')
            if compounds:
                c = compounds[0]
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"✅ اطلاعات ماده {compound_name} یافت شد")
                    st.write(f"**فرمول مولکولی:** {c.molecular_formula}")
                    st.write(f"**وزن مولکولی:** {c.molecular_weight}")
                with col2:
                    st.image(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{c.cid}/PNG", caption=f"ساختار دو بعدی {compound_name}")
            else:
                st.error("❌ متأسفانه ماده‌ای با این نام یافت نشد.")
        except:
            st.error("⚠️ خطا در برقراری ارتباط با دیتابیس PubChem.")

elif choice == "تحلیل تداخلات خطرناک":
    st.subheader("⚠️ آنالیز هوشمند تداخلات")
    m1 = st.text_input("نام ماده اول:")
    m2 = st.text_input("نام ماده دوم:")
    
    if st.button("شروع آنالیز ایمنی"):
        if m1 and m2:
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            m1_l, m2_l = m1.lower(), m2.lower()
            hazards = [
                (["acid", "bleach"], "تولید گاز کلر بسیار سمی", "High Risk"),
                (["sodium", "water"], "انفجار سریع و اشتعال شدید", "Critical"),
                (["acid", "base"], "واکنش خنثی‌سازی همراه با گرمای شدید", "Medium Risk")
            ]
            
            found = False
            for (m1_check, m2_check), msg, lvl in hazards:
                if (m1_l in m1_check and m2_l in m2_check) or (m1_l in m2_check and m2_l in m1_l):
                    found = True
                    st.error(f"❌ سطح خطر: {lvl}")
                    st.markdown(f'<div class="danger-box"><h2 style="color:white; margin:0;">{lvl}</h2><p style="color:white;">{msg}</p></div>', unsafe_allow_html=True)
                    st.download_button("📥 دریافت فایل گزارش ایمنی", f"گزارش نهایی: ترکیب {m1} و {m2} منجر به {msg} می‌گردد.", file_name="Chemical_Safety_Report.txt")
                    break
            
            if not found:
                st.balloons()
                st.success("✅ هیچ تداخل خطرناک شناخته شده‌ای بین این دو ماده یافت نشد.")
        else:
            st.warning("لطفاً نام هر دو ماده را برای آنالیز وارد نمایید.")

st.markdown("---")
st.caption("🧪 دستیار دیجیتال ایمنی شیمی | پایش هوشمند تداخلات بر پایه داده‌های جهانی 🧬")