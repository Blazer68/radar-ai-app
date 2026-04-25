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
            
            # استخدام الخصائص الأساسية المتوفرة دائماً
            col1, col2 = st.columns(2)
            with col1:
                # التأكد من وجود Callsign أو عرض 'غير معروف'
                callsign = f.callsign if f.callsign else "N/A"
                st.metric("رقم الرحلة", callsign)
                st.metric("الارتفاع", f"{f.altitude} قدم")
            with col2:
                st.metric("السرعة", f"{f.ground_speed} عقدة")
                # هنا قمنا بإزالة .model التي كانت تسبب الخطأ واستبدالها بـ .aircraft_code
                st.metric("رمز الطائرة", getattr(f, 'aircraft_code', 'غير معروف'))
            
            # تحليل مدمج ذكي وبسيط
            st.subheader("📝 التحليل الفني:")
            altitude = int(f.altitude)
            if altitude < 1000:
                تحليل = "الطائرة في وضعية منخفضة جداً، غالباً في مرحلة الإقلاع أو الهبوط النهائي."
            elif altitude > 30000:
                تحليل = "تحليق في الارتفاع القياسي للرحلات الطويلة. استقرار تام."
            else:
                تحليل = "تحليق في ارتفاع متوسط. الرحلة مستمرة كالمعتاد."
                
            st.write(f"🤖 **الرادار يقول:** {تحليل}")
            
        else:
            st.warning("لا توجد طائرات حالياً في النطاق.")
    except Exception as e:
        # هذا السطر سيطبع الخطأ إذا حدث لتعرف مكانه، ولكن الكود أعلاه سيتجنبه
        st.error(f"تنبيه تقني: {e}")
