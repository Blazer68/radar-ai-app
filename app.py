import streamlit as st
from FlightRadar24 import FlightRadar24API

st.set_page_config(page_title="راداري الذكي", page_icon="✈️")
st.title("✈️ راداري الخاص (نسخة مستقرة)")

if st.button('ابحث عن طائرة وحللها'):
    try:
        fr = FlightRadar24API()
        flights = fr.get_flights()
        
        if flights:
            f = flights[0]
            st.success(f"✅ تم العثور على طائرة!")
            
            # عرض البيانات بشكل أنيق بدلاً من الخطأ
            col1, col2 = st.columns(2)
            with col1:
                st.metric("رقم الرحلة", f.callsign)
                st.metric("الارتفاع", f"{f.altitude} قدم")
            with col2:
                st.metric("السرعة", f"{f.ground_speed} عقدة")
                st.metric("الطائرة", f.model)
            
            # تحليل "ذكي" مدمج (بدون الحاجة لـ Gemini المتقلب)
            st.subheader("📝 التحليل الفني:")
            if f.altitude < 1000:
                تحليل = "الطائرة حالياً على مدرج المطار أو في مرحلة الإقلاع الأولي. المحركات تعمل بكامل طاقتها!"
            elif f.altitude > 30000:
                تحليل = "الطائرة في ارتفاع سحق السحب (Cruise)، الجو هادئ والركاب يستمتعون بالرحلة."
            else:
                تحليل = "الطائرة في مرحلة تغيير الارتفاع، إما للهبوط أو بعد الإقلاع."
                
            st.write(f"🤖 **الرادار يقول:** {تحليل}")
            
        else:
            st.warning("لا توجد طائرات حالياً في النطاق.")
    except Exception as e:
        st.error(f"حدث خطأ في الاتصال بالرادار: {e}")
