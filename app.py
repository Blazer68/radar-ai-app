import streamlit as st
from FlightRadar24 import FlightRadar24API

st.set_page_config(page_title="رادار الأجواء الحية", page_icon="✈️", layout="wide")
st.title("✈️ راداري المتطور - قائمة الرحلات الحالية")

if st.button('تحديث حركة الطيران الآن'):
    try:
        fr = FlightRadar24API()
        flights = fr.get_flights()
        
        if flights:
            st.success(f"✅ تم رصد {len(flights)} طائرة في الأجواء القريبة!")
            
            # عرض الطائرات في بطاقات أنيقة
            for i, f in enumerate(flights[:5]): # عرض أول 5 طائرات فقط للسرعة
                with st.expander(f"✈️ رحلة رقم: {getattr(f, 'callsign', 'N/A')}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("الارتفاع", f"{f.altitude} قدم")
                    with col2:
                        st.metric("السرعة", f"{f.ground_speed} عقدة")
                    with col3:
                        # جلب نوع الطائرة بأمان كما تعلمنا
                        aircraft = "غير معروف"
                        for key in ['model', 'aircraft_code', 'typecode']:
                            if hasattr(f, key):
                                aircraft = getattr(f, key)
                                break
                        st.write(f"**نوع الطائرة:** {aircraft}")
                    
                    # تحليل بسيط لكل طائرة على حدة
                    progress = min(int(f.altitude) / 40000, 1.0)
                    st.progress(progress, text="مستوى الارتفاع بالنسبة للحد الأقصى")
        else:
            st.warning("لا توجد طائرات حالياً.")
    except Exception as e:
        st.error(f"تنبيه: {e}")
