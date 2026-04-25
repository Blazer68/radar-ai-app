import streamlit as st
import google.generativeai as genai
from FlightRadar24 import FlightRadar24API

st.title("✈️ راداري الذكي")

# إعداد الاتصال بالمفتاح السري
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # تغيير اسم النموذج إلى gemini-pro لحل مشكلة الـ 404 نهائياً
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("يرجى إضافة GEMINI_KEY في قسم Secrets")

if st.button('ابحث عن طائرة وحللها'):
    fr = FlightRadar24API()
    try:
        flights = fr.get_flights()
        if flights:
            f = flights[0]
            st.info(f"تم رصد طائرة بارتفاع {f.altitude} قدم")
            
            # طلب التحليل
            response = model.generate_content(f"حلل بأسلوب ممتع حالة طائرة بارتفاع {f.altitude} قدم.")
            st.success(response.text)
        else:
            st.warning("لا توجد طائرات حالياً.")
    except Exception as e:
        st.error(f"عذراً، حدث خطأ: {e}")
