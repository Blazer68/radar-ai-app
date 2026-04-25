import streamlit as st
from FlightRadar24 import FlightRadar24API
import pandas as pd

st.set_page_config(page_title="رادار بسكرة", page_icon="📍")
st.title("📍 رادار الزيبان - بسكرة (200 كلم)")

if st.button('تحديث الرادار الآن'):
    try:
        fr = FlightRadar24API()
        # إحداثيات بسكرة مع نطاق 200 كلم
        bounds = fr.get_bounds_by_point(34.85, 5.72, 200000)
        flights = fr.get_flights(bounds = bounds)
        
        if flights:
            st.success(f"✅ تم رصد {len(flights)} طائرة حالياً")
            
            # إعداد بيانات الخريطة
            map_data = []
            for f in flights:
                map_data.append({
                    'lat': f.latitude,
                    'lon': f.longitude,
                    'name': getattr(f, 'callsign', 'N/A')
                })
            
            # رسم الخريطة
            df = pd.DataFrame(map_data)
            st.map(df)
            
            # عرض التفاصيل أسفل الخريطة
            for f in flights:
                with st.expander(f"✈️ {getattr(f, 'callsign', 'N/A')}"):
                    st.write(f"**الارتفاع:** {f.altitude} قدم")
                    st.write(f"**السرعة:** {f.ground_speed} عقدة")
        else:
            st.warning("الأجواء هادئة فوق بسكرة حالياً.")
    except Exception as e:
        st.error(f"تنبيه: {e}")
