import streamlit as st
from FlightRadar24 import FlightRadar24API
import google.generativeai as genai

st.title("✈️ راداري الذكي الآمن")

# استخدام طريقة الاتصال الأكثر استقراراً
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # حذفنا كلمة 'latest' و 'v1beta' لتجنب خطأ 404
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("الرجاء إضافة GEMINI_KEY في إعدادات Secrets")
except Exception as e:
    st.error(f"خطأ في الإعداد: {e}")

if st.button('تحليل الرحلة الحالية'):
    fr = FlightRadar24API()
    try:
        flights = fr.get_flights()
        if flights:
            f = flights[0]
            # عرض الارتفاع الحالي (الذي وصل الآن لـ 801 قدم!)
            st.info(f"تم رصد طائرة بارتفاع {f.altitude} قدم")
            
            # طلب التحليل بأسلوب بسيط
            response = model.generate_content(f"حلل هذه البيانات بأسلوب مشوق: طائرة بارتفاع {f.altitude} قدم.")
            st.success(response.text)
        else:
            st.warning("لا توجد طائرات حالياً.")
    except Exception as e:
        st.error(f"عذراً، حدث خطأ أثناء جلب البيانات أو التحليل: {e}")
