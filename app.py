import streamlit as st
from FlightRadar24 import FlightRadar24API
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="رادار  الذكي", page_icon="🔔", layout="wide")
st.title("🔔 رادار الذكاء - نظام التنبيه المبكر")

# الموقع المرجعي (وسط مدينة بسكرة)
HOME_LAT, HOME_LON = 34.85, 5.72

if st.button('تحديث ومسح الأجواء'):
    try:
        fr = FlightRadar24API()
        # مسح نطاق 200 كلم حول بسكرة كما حددنا سابقاً
        bounds = fr.get_bounds_by_point(HOME_LAT, HOME_LON, 200000)
        flights = fr.get_flights(bounds = bounds)
        
        if flights:
            st.success(f"✅ تم رصد {len(flights)} طائرة في النطاق المحلي")
            
            # --- ميزة التنبيهات الجديدة ---
            near_flights = []
            for f in flights:
                # حساب المسافة التقريبية (فرق الإحداثيات البسيط)
                dist = ((f.latitude - HOME_LAT)**2 + (f.longitude - HOME_LON)**2)**0.5
                if dist < 0.1: # نطاق قريب جداً (حوالي 10-15 كلم من وسط بسكرة)
                    near_flights.append(f)
            
            if near_flights:
                st.toast("⚠️ تنبيه: طائرة تقترب من موقعك الآن!", icon='✈️')
                st.warning(f"🚨 يوجد {len(near_flights)} طائرة في سماء المدينة حالياً!")
                # إضافة صوت تنبيه بسيط (اختياري عبر HTML)
                st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)
            
            # --- عرض الخريطة ---
            map_data = [{'lat': f.latitude, 'lon': f.longitude, 'name': getattr(f, 'callsign', 'N/A')} for f in flights]
            st.map(pd.DataFrame(map_data))
            
            # --- تفاصيل الرحلات ---
            for f in flights:
                with st.expander(f"✈️ تفاصيل الرحلة: {getattr(f, 'callsign', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    col1.metric("الارتفاع", f"{f.altitude} قدم")
                    col2.metric("السرعة", f"{f.ground_speed} عقدة")
        else:
            st.info("السماء صافية حالياً فوق بسكرة.")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
