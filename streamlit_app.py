import streamlit as st
import json

st.set_page_config(page_title="BYD Iraq Team", page_icon="🚗", layout="centered")

st.title("🚗 موسوعة فريق BYD العراق الشاملة")
st.write("النسخة المتقدمة | حاسبة التوفير ودليل الأعطال الشامل")

st.markdown("---")

# --- 1. حاسبة التوفير ---
st.header("📊 حاسبة التوفير عبر العداد")
col1, col2 = st.columns(2)
with col1:
    prev_km = st.number_input("قراءة العداد السابقة (كم):", value=10000, step=100)
with col2:
    current_km = st.number_input("قراءة العداد الحالية (كم):", value=11500, step=100)

if current_km > prev_km:
    total_km = current_km - prev_km
    cost_gasoline = (total_km / 10) * 1000
    cost_ev = (total_km / 6) * 50
    savings = cost_gasoline - cost_ev

    st.success(f"💰 التوفير المالي للمسافة ({total_km:,} كم): **{int(savings):,} دينار عراقي**")

st.markdown("---")

# --- 2. دليل الأعطال الشامل (البحث المتقدم) ---
st.header("🛠️ دليل الأعطال الكبرى (البحث عن الكود)")

# قاعدة بيانات نموذجية يمكن توسيعها لـ 1000 كود عبر ملف JSON
faults_db = {
    "P0A80": {
        "title": "P0A80 - Replace High Voltage Battery Pack",
        "desc": "ضعف أو تلف في خلايا حزمة بطارية الهجين/الضغط العالي.",
        "fix": "1. تنظيف مروحة تبريد البطارية.\n2. فحص فولتية الخلايا عبر جهاز GDS/OBD.\n3. استبدال الخلايا التالفة.",
        "video": "https://www.youtube.com/watch?v=R39S_kIna3k"
    },
    "TPMS": {
        "title": "TPMS - Tire Pressure Monitoring System",
        "desc": "انخفاض ضغط الهواء في أحد الإطارات.",
        "fix": "1. اضبط ضغط الإطارات على 34 PSI.\n2. اقطع مسافة 3 كم لإعادة معايرة الحساس.",
        "video": "https://www.youtube.com/watch?v=0h94Lh1a6_s"
    },
    "P0101": {
        "title": "P0101 - Mass Air Flow (MAF) Circuit Range/Performance",
        "desc": "خلل في قراءة حساس تدفق الهواء (خاص بمحركات البنزين/الهجين).",
        "fix": "1. تنظيف حساس الـ MAF بخاخ خاص.\n2. التأكد من سلامة فلتر الهواء.",
        "video": "https://www.youtube.com/watch?v=xQGskW1316E"
    }
}

search_query = st.text_input("🔍 اكتب رمز العطل هنا (مثال: P0A80, TPMS, P0101):", "").strip().upper()

if search_query:
    if search_query in faults_db:
        data = faults_db[search_query]
        st.subheader(data["title"])
        st.error(f"**الوصف:** {data['desc']}")
        st.warning(f"**طريقة التصليح:**\n{data['fix']}")
        if data["video"]:
            st.write("🎥 **فيديو توضيحي للحل:**")
            st.video(data["video"])
    else:
        st.info(f"لم نجد الكود ({search_query}) مسجلاً. يمكنك البحث عنه تلقائياً في يوتيوب عبر الرابط:")
        st.markdown(f"[🔍 اضغط هنا للبحث عن فيديو تصليح {search_query} على يوتيوب](https://www.youtube.com/results?search_query=BYD+{search_query}+repair)")
else:
    st.write("👈 أدخل رمز العطل في مربع البحث أعلاه لمشاهدة التفاصيل والفيديو.")

st.markdown("---")
st.caption("إهداء خاص إلى قائد وأعضاء فريق BYD العراق ❤️")
