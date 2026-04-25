import streamlit as st
from FlightRadar24 import FlightRadar24API
import google.generativeai as genai

# إعداد واجهة التطبيق
st.set_page_config(page_title="راداري الذكي", page_icon="✈️")
st.title("✈️ راداري الذكي الآمن")

# الاتصال بـ Gemini باستخدام الخزنة السرية
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("الرجاء إضافة المفتاح في إعدادات Secrets")
except Exception as e:
    st.error(f"خطأ في الإعداد: {e}")

if st.button('إبدأ تحليل السماء الآن'):
    fr = FlightRadar24API()
    try:
        flights = fr.get_flights()
        if flights:
            f = flights[0]
            st.info(f"تم العثور على طائرة! الارتفاع: {f.altitude} قدم")
            
            # طلب التحليل من الذكاء الاصطناعي
            prompt = f"أنت خبير طيران، حلل بأسلوب مشوق طائرة بارتفاع {f.altitude} قدم."
            response = model.generate_content(prompt)
            st.success(response.text)
        else:
            st.warning("السماء صافية حالياً، لا توجد طائرات.")
    except Exception as e:
        st.error(f"حدث خطأ تقني: {e}")
