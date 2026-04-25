import streamlit as st
from FlightRadar24 import FlightRadar24API

st.set_page_config(page_title="رادار بسكرة المحلي", page_icon="📍", layout="wide")
st.title("📍 رادار بسكرة والأجواء المجاورة (200 كلم)")

if st.button('تحديث حركة طيران بسكرة'):
    try:
        fr = FlightRadar24API()
        
        # تحديد منطقة بسكرة بقطر تقريبي 200 كلم
        # الإحداثيات: شمال، جنوب، غرب، شرق
        bounds = fr.get_bounds_by_point(34.85, 5.72, 200000) # 200,000 متر = 200 كلم
        flights = fr.get_flights(bounds = bounds)
        
        if flights:
            st.success(f"✅ تم رصد {len(flights)} طائرة فوق منطقة بسكرة حالياً")
            
            for f in flights:
                with st.expander(f"✈️ رحلة: {getattr(f, 'callsign', 'N/A')}"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("الارتفاع", f"{f.altitude} قدم")
                    with c2:
                        st.metric("السرعة", f"{f.ground_speed} عقدة")
                    with c3:
                        # عرض الوجهة إذا توفرت
                        st.write(f"**من:** {getattr(f, 'origin_airport_iota', 'غير معروف')}")
                        st.write(f"**إلى:** {getattr(f, 'destination_airport_iota', 'غير معروف')}")
                    
                    # تنبيه إذا كانت الطائرة قريبة جداً من الأرض (احتمال مطار بسكرة)
                    if int(f.altitude) < 5000:
                        st.warning("⚠️ هذه الطائرة في ارتفاع منخفض، قد تكون متجهة لمطار محمد خيضر أو أقلعت منه!")
        else:
            st.warning("لا توجد طائرات حالياً في نطاق 200 كلم حول بسكرة.")
            
    except Exception as e:
        st.error(f"خطأ تقني: {e}")
