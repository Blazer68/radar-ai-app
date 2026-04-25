import streamlit as st
from FlightRadar24 import FlightRadar24API
import google.generativeai as genai

st.title("✈️ راداري الذكي الآمن")

# قراءة المفتاح من الخزنة السرية لـ Streamlit
try:
    my_api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=my_api_key)
    # استخدام اسم النموذج بدقة
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    st.error("يرجى إعداد GEMINI_KEY في إعدادات Secrets")

if st.button('تحليل الرحلة الحالية'):
    fr = FlightRadar24API()
    flights = fr.get_flights()
    if flights:
        f = flights[0]
        # عرض الارتفاع كما في تجربتك السابقة (791 قدم)
        st.info(f"تم رصد طائرة بارتفاع {f.altitude} قدم")
        
        try:
            prompt = f"حلل بأسلوب ممتع طائرة بارتفاع {f.altitude} قدم وسرعة {f.ground_speed}."
            response = model.generate_content(prompt)
            st.success(response.text)
        except Exception as e:
            st.error(f"خطأ في التحليل: {e}")
    else:
        st.warning("لا توجد طائرات مكتشفة.")
