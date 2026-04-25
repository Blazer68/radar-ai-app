import streamlit as st
from FlightRadar24 import FlightRadar24API
import pandas as pd
import pydeck as pdk

# 1. إعدادات واجهة التطبيق الاحترافية
st.set_page_config(page_title="رادار  الذكي", page_icon="📍", layout="wide")
st.title("📍 رادار - نظام التتبع والتنبيه الاحترافي")

# إحداثيات بسكرة (المركز)
HOME_LAT, HOME_LON = 34.85, 5.72

if st.button('تحديث ومسح الأجواء الآن'):
    try:
        fr = FlightRadar24API()
        
        # 2. مسح نطاق 200 كلم حول بسكرة
        bounds = fr.get_bounds_by_point(HOME_LAT, HOME_LON, 200000)
        flights = fr.get_flights(bounds = bounds)
        
        if flights:
            # 3. نظام التنبيه الذكي (نطاق 30 كلم)
            near_flights = []
            map_data = []
            
            for f in flights:
                # جلب البيانات بأمان لتجنب الـ AttributeError
                callsign = getattr(f, 'callsign', 'N/A')
                # محاولة جلب نوع الطائرة من عدة مسميات محتملة
                aircraft = "N/A"
                for attr in ['model', 'aircraft_code', 'typecode']:
                    if hasattr(f, attr):
                        aircraft = getattr(f, attr)
                        break
                
                # إضافة البيانات للقائمة
                map_data.append({
                    'lat': f.latitude,
                    'lon': f.longitude,
                    'info': f"{callsign} | {aircraft}"
                })
                
                # حساب المسافة للتنبيه (حساسية 0.3 درجة جغرافية)
                dist = ((f.latitude - HOME_LAT)**2 + (f.longitude - HOME_LON)**2)**0.5
                if dist < 0.3:
                    near_flights.append(callsign)
            
            # عرض التنبيهات إذا وجدت طائرات قريبة
            if near_flights:
                st.error(f"🚨 تنبيه: {len(near_flights)} طائرة في محيط مدينة بسكرة الآن!")
                for nf in near_flights:
                    st.toast(f"الطائرة {nf} تقترب!", icon='⚠️')

            # 4. الخريطة الاحترافية (PyDeck) مع الأسماء فوق الطائرات
            df_map = pd.DataFrame(map_data)
            view_state = pdk.ViewState(latitude=HOME_LAT, longitude=HOME_LON, zoom=8, pitch=0)

            # طبقة النقاط الحمراء
            layer_points = pdk.Layer(
                "ScatterplotLayer",
                df_map,
                get_position='[lon, lat]',
                get_color='[255, 0, 0, 200]', # أحمر قوي
                get_radius=2500,
            )

            # طبقة الأسماء البيضاء فوق النقاط
            layer_text = pdk.Layer(
                "TextLayer",
                df_map,
                get_position='[lon, lat]',
                get_text='info',
                get_size=18,
                get_color=[255, 255, 255],
                get_alignment_baseline="'bottom'",
            )

            st.pydeck_chart(pdk.Deck(
                layers=[layer_points, layer_text],
                initial_view_state=view_state,
                map_style='mapbox://styles/mapbox/dark-v10'
            ))

            # 5. عرض التفاصيل في الأسفل
            st.subheader("📋 قائمة الرحلات المرصودة:")
            for f in flights:
                with st.expander(f"✈️ رحلة: {getattr(f, 'callsign', 'N/A')}"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("الارتفاع", f"{f.altitude} قدم")
                    c2.metric("السرعة", f"{f.ground_speed} عقدة")
                    c3.write(f"**الموقع:** {f.latitude:.2f}, {f.longitude:.2f}")

        else:
            st.warning("الأجواء هادئة حالياً فوق بسكرة والزيبان.")

    except Exception as e:
        st.error(f"تنبيه تقني: {e}")
