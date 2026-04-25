import streamlit as st
from FlightRadar24 import FlightRadar24API
import google.generativeai as genai

st.title("✈️ راداري الذكي")

# إعداد المفتاح الذي استخدمته بنجاح سابقاً
genai.configure(api_key="AIzaSyBMUU43qGG09zfsua9O86oP1kOyy9Bv-PQ")
model = genai.GenerativeModel('gemini-1.5-flash')

if st.button('ابحث عن طائرة وحللها'):
    fr = FlightRadar24API()
    flights = fr.get_flights()
    if flights:
        f = flights[0]
        st.write(f"تم العثور على طائرة بارتفاع {f.altitude} قدم.")
        response = model.generate_content(f"اشرح بأسلوب ممتع حالة طائرة على ارتفاع {f.altitude} قدم.")
        st.success(response.text)
    else:
        st.warning("لا توجد طائرات حالياً.")
