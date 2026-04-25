import streamlit as st
from FlightRadar24 import FlightRadar24API
import google.generativeai as genai

st.title("✈️ راداري الذكي الآمن")

# الاتصال الآمن بالمفتاح
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # الحل هنا: جربنا gemini-pro لأنه الأكثر استقراراً وقبولاً في كافة النسخ
        model = genai.GenerativeModel('gemini-pro')
    else:
        st.error("يرجى التأكد من إضافة GEMINI_KEY في إعدادات Secrets")
except Exception as e:
    st.error(f"خطأ في الإعداد: {e}")

if st.button('تحليل الرحلة الحالية'):
    fr = FlightRadar24API()
    try:
        flights = fr.get_flights()
        if flights:
            f = flights[0]
            # الارتفاع وصل الآن لـ 804 قدم كما في صورتك الأخيرة
            st.info(f"تم رصد طائرة بارتفاع {f.altitude} قدم")
            
            # محاولة التحليل
            response = model.generate_content(f"حلل بذكاء طائرة بارتفاع {f.altitude} قدم.")
            st.success(response.text)
        else:
            st.warning("لا توجد طائرات حالياً في الرادار.")
    except Exception as e:
        # إذا فشل gemini-pro، هذا الكود سيخبرنا بالسبب الدقيق خلف الستار
        st.error(f"حدث خطأ تقني في التحليل: {e}")
