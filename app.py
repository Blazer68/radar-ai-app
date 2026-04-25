import streamlit as st
from FlightRadar24 import FlightRadar24API

st.set_page_config(page_title="راداري الذكي", page_icon="✈️")
st.title("✈️ راداري الخاص (النسخة المستقرة)")

if st.button('ابحث عن طائرة وحللها'):
    try:
        fr = FlightRadar24API()
        flights = fr.get_flights()
        
        if flights:
            f = flights[0]
            st.success("✅ تم العثور على طائرة!")
            
            # عرض البيانات المتوفرة فقط وتجنب الأخطاء
            col1, col2 = st.columns(2)
            with col1:
                # التأكد من وجود رقم الرحلة
                callsign = getattr(f, 'callsign', 'غير معروف')
                st.metric("رقم الرحلة", callsign)
                
                # التأكد من وجود الارتفاع
                altitude = getattr(f, 'altitude', 0)
                st.metric("الارتفاع", f"{altitude} قدم")
            
            with col2:
                # التأكد من وجود السرعة
                speed = getattr(f, 'ground_speed', 0)
                st.metric("السرعة", f"{speed} عقدة")
                
                # حل مشكلة الـ Attribute Error نهائياً
                # سنحاول جلب أي معلومة عن نوع الطائرة، وإذا لم نجد سنكتب "غير متوفر"
                aircraft = "غير متوفر"
                for attr in ['model', 'aircraft_code', 'typecode']:
                    if hasattr(f, attr):
                        aircraft = getattr(f, attr)
                        break
                st.metric("نوع الطائرة", aircraft)
            
            # تحليل بسيط يعتمد على الارتفاع المتاح
            st.subheader("📝 حالة الرحلة:")
            if altitude < 1000:
                msg = "الطائرة قريبة جداً من الأرض (إقلاع أو هبوط)."
            elif altitude > 20000:
                msg = "الطائرة في مرحلة التحليق العالي."
            else:
                msg = "الطائرة في مرحلة انتقالية أو تحليق منخفض."
            st.write(f"🤖 **التحليل:** {msg}")
            
        else:
            st.warning("لا توجد طائرات حالياً في النطاق.")
    except Exception as e:
        st.error(f"حدث خطأ غير متوقع: {e}")
