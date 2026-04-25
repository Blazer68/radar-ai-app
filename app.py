import streamlit as st
from FlightRadar24 import FlightRadar24API
import folium
from streamlit_folium import st_folium

# 1. إعدادات الصفحة
st.set_page_config(page_title="رادار الزيبان الاحترافي", layout="wide")
st.title("📍 رادار تتبع الطائرات - منطقة بسكرة")

# إحداثيات بسكرة المركزية
HOME_LAT, HOME_LON = 34.85, 5.72

# زر التحديث
if st.button('تحديث مسح الأجواء الآن'):
    try:
        fr = FlightRadar24API()
        # مسح منطقة واسعة (200 كلم)
        bounds = fr.get_bounds_by_point(HOME_LAT, HOME_LON, 200000)
        flights = fr.get_flights(bounds = bounds)

        if flights:
            st.success(f"تم رصد {len(flights)} طائرة حالياً")

            # 2. إنشاء الخريطة الجغرافية الحقيقية (Folium)
            m = folium.Map(location=[HOME_LAT, HOME_LON], zoom_start=8, tiles="OpenStreetMap")

            # إضافة نقطة مركزية لمدينة بسكرة
            folium.Marker(
                [HOME_LAT, HOME_LON], 
                popup="مدينة بسكرة",
                icon=folium.Icon(color="blue", icon="home")
            ).add_to(m)

            for f in flights:
                # جلب البيانات بأمان
                callsign = getattr(f, 'callsign', 'Unknown')
                aircraft = getattr(f, 'model', '✈️')
                altitude = getattr(f, 'altitude', 0)
                
                # إضافة الطائرات كنقاط حمراء مع ملصقات نصية
                label = f"{callsign} | {aircraft}"
                folium.CircleMarker(
                    location=[f.latitude, f.longitude],
                    radius=7,
                    popup=f"الرحلة: {callsign}<br>النوع: {aircraft}<br>الارتفاع: {altitude} قدم",
                    color="red",
                    fill=True,
                    fill_color="red",
                    fill_opacity=0.7,
                    tooltip=label # يظهر الاسم عند تمرير الفأرة أو الضغط
                ).add_to(m)

            # 3. عرض الخريطة في التطبيق
            st_folium(m, width=900, height=500)

            # عرض القائمة التفصيلية بالأسفل
            st.subheader("📋 تفاصيل الرحلات المرصودة:")
            for f in flights:
                with st.expander(f"✈️ {getattr(f, 'callsign', 'N/A')}"):
                    st.write(f"**نوع الطائرة:** {getattr(f, 'model', 'N/A')}")
                    st.write(f"**الارتفاع:** {f.altitude} قدم")
                    st.write(f"**السرعة:** {f.ground_speed} عقدة")

        else:
            st.warning("لا توجد طائرات مرصودة في المجال الجوي حالياً.")

    except Exception as e:
        st.error(f"حدث خطأ فني: {e}")
