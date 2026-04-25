import streamlit as st
from FlightRadar24 import FlightRadar24API

st.set_page_config(page_title="راداري الذكي", page_icon="✈️")
st.title("✈️ راداري الخاص (نسخة احترافية)")

if st.button('ابحث عن طائرة وحللها'):
    try:
        fr = FlightRadar24API()
        flights = fr.get_flights()
        
        if flights:
            f = flights[0]
            st.success("✅ تم العثور على طائرة!")
            
            # عرض البيانات بطريقة "آمنة" تتجنب الانهيار
            col1, col2 = st.columns(2)
            with col1:
                # نستخدم .get() أو getattr() لتجنب الـ AttributeError
                st.metric("رقم الرحلة", getattr(f, 'callsign', 'غير متوفر'))
                st.metric("الارتفاع", f"{getattr(f, 'altitude', 0)} قدم")
            
            with col2:
                st.metric("السرعة", f"{getattr(f, 'ground_speed', 0)} عقدة")
                # حل المشكلة التي في صورتك: نجرب عدة مسميات لنوع الطائرة
                type_info = "غير متوفر"
                for key in ['aircraft_code', 'model', 'typecode']:
                    if hasattr(f, key):
                        type_info = getattr(f, key)
                        break
                st.metric("نوع الطائرة", type_info)
            
            # تحليل تلقائي ذكي
            st.subheader("📝 حالة الطائرة:")
            alt = getattr(f, 'altitude', 0)
            if alt < 1000:
                st.write("🤖 **التحليل:** الطائرة قريبة جداً من الأرض، من المحتمل أنها في طور الإقلاع أو الهبوط.")
            else:
                st.write("🤖 **التحليل:** الطائرة تحلق في الأجواء بشكل مستقر.")
                
        else:
            st.warning("لا توجد طائرات حالياً في النطاق.")
    except Exception as e:
        st.error(f"تنبيه تقني: {e}")
