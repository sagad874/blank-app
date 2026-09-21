import streamlit as st

st.set_page_config(page_title="BYD Iraq Team", page_icon="🚗", layout="centered")

st.title("🚗 تطبيق فريق BYD العراق")
st.write("أهلاً بك! تطبيق بسيط لمساعدتك في حساب التوفير ومعرفة أعطال السيارة.")

st.markdown("---")

st.header("🧮 حاسبة التوفير البنزين مقابل الكهرباء")
st.write("حرك الشريط بالأسفل لاختيار المسافة التي تقطعها يومياً:")

km = st.slider("المسافة اليومية (كيلومتر):", min_value=10, max_value=200, value=50, step=5)

cost_gasoline = (km / 10) * 1000 * 30
cost_ev = (km / 6) * 50 * 30
savings = cost_gasoline - cost_ev

st.subheader("النتيجة الشهرية:")
st.success(f"💰 التوفير الشهري المتوقع: {int(savings):,} دينار عراقي")

with st.expander("🔍 اضغط هنا لرؤية تفاصيل التكلفة"):
    st.write(f"- تكلفة البنزين لسيارة العادية: {int(cost_gasoline):,} دينار/شهر")
    st.write(f"- تكلفة شحن BYD بالكهرباء: {int(cost_ev):,} دينار/شهر")

st.markdown("---")

st.header("🛠️ دليل رموز الأعطال الشائعة")
st.write("ابحث عن الكود الذي يظهر في شاشة السيارة:")

dtc_codes = {
    "OK": "السيارة بحالة ممتازة ولا توجد أخطاء.",
    "P0A80": "تنبيه: يفصل بطارية الهجين أو تحتاج فحص عند المختص.",
    "TPMS": "تنبيه: ضغط الهواء في أحد الإطارات منخفض.",
    "Ready": "السيارة جاهزة للتحرك (ليست مشكلة)."
}

code_search = st.selectbox("اختر رمز التنبيه:", list(dtc_codes.keys()))
st.info(f"**الشرح:** {dtc_codes[code_search]}")

st.markdown("---")
st.caption("إهداء خاص إلى قائد وأعضاء فريق BYD العراق ❤️")
