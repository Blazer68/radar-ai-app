import streamlit as st
from FlightRadar24 import FlightRadar24API
import folium
from streamlit_folium import st_folium

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="رادار الزيبان المستقر", layout="wide")
st.title("📍 رادار تتبع الطائرات - منطقة بسكرة")

# إحداثيات بسكرة
HOME_LAT, HOME_LON = 34.85, 5.72

# 2. تهيئة "مخزن البيانات" (Session State) لمنع الاختفاء
if 'flights_data' not in st.session_state:
    st.session_state.flights_data = []

# زر التحديث
if st.button('تحديث ومسح الأجواء الآن'):
    with st.spinner('جاري جلب بيانات الطائرات...'):
        try:
            fr = FlightRadar24API()
            bounds = fr.get_bounds_by_point(HOME_LAT, HOME_LON, 200000)
            # تخزين البيانات في المخزن لتبقى ثابتة
            st.session_state.flights_data = fr.get_flights(bounds = bounds)
            if not st.session_state.flights_data:
                st.warning("لا توجد طائرات حالياً في النطاق.")
        except Exception as e:
            st.error(f"خطأ في الاتصال: {e}")

# 3. عرض الخريطة والقائمة (فقط إذا كانت هناك بيانات مخزنة)
if st.session_state.flights_data:
    flights = st.session_state.flights_data
    
    # إنشاء الخريطة
    m = folium.Map(location=[HOME_LAT, HOME_LON], zoom_start=8)
    
    # إضافة علامة مدينة بسكرة
    folium.Marker([HOME_LAT, HOME_LON], popup="Biskra", icon=folium.Icon(color="blue")).add_to(m)

    for f in flights:
        # جلب المعلومات مع معالجة الأخطاء السابقة (AttributeError)
        callsign = getattr(f, 'callsign', 'Unknown')
        aircraft = getattr(f, 'model', 'N/A')
        
        folium.CircleMarker(
            location=[f.latitude, f.longitude],
            radius=8,
            color="red",
            fill=True,
            fill_opacity=0.7,
            popup=f"الرحلة: {callsign}<br>الطائرة: {aircraft}",
            tooltip=callsign
        ).add_to(m)

    # عرض الخريطة بشكل مستقر
    st_folium(m, width=900, height=500, key="main_radar_map")

    # 4. عرض القائمة التفصيلية بالأسفل
    st.subheader(f"📋 تم رصد {len(flights)} طائرة:")
    cols = st.columns(2) # توزيع البيانات على عمودين لتنظيم المظهر
    for index, f in enumerate(flights):
        with cols[index % 2].expander(f"✈️ رحلة رقم: {getattr(f, 'callsign', 'N/A')}"):
            st.write(f"**الارتفاع:** {f.altitude} قدم")
            st.write(f"**السرعة:** {f.ground_speed} عقدة")
            st.write(f"**الموديل:** {getattr(f, 'model', 'غير متوفر')}")
