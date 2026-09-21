import streamlit as st

# إعدادات الصفحة
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

# --- 2. قاعدة بيانات الأعطال الكبرى (قائمة + بحث) ---
st.header("🛠️ دليل أعطال سيارات BYD والكهرباء")

# قاعدة بيانات موسعة لأكواد الأعطال (تضم أكواد P, U, C, B وأعطال شائعة)
faults_db = {
    "اختر كود من القائمة...": {
        "title": "", "desc": "", "fix": "", "video": ""
    },
    "U0298 - انقطاع الاتصال بمحول DC-DC": {
        "title": "U0298 - Lost Communication With DC/DC Converter",
        "desc": "🚨 خطأ نادر وجسيم: انقطاع الاتصال بين عقل السيارة ومحول الطاقة (DC-DC Converter). يؤدي لتوقف شحن بطارية الـ 12V الصغرى وانطفاء الأنظمة الإلكترونية.",
        "fix": "1. افحص فيوزات نظام الـ DC-DC والمحولات العالية الفولتية في صندوق الفيوزات الرئيسي.\n2. افحص فيشة الاتصال الخاصة بشبكة CAN-Bus الواصلة إلى وحدة المحول وتأكد من عدم وجود كلس أو رطوبة.\n3. قياس فولتية بطارية الـ 12V (إذا كانت أقل من 10V يجب شحنها خارجياً أولاً لإعادة الاتصال).\n4. إذا استمرت المشكلة، يتطلب الأمر إعادة برمجة وحدة التوزيع (PDU) أو فحص المحول عند مركز صيانة متقدم.",
        "video": "https://www.youtube.com/watch?v=2eO712Pq6yU"
    },
    "P0AA6 - تسريب فولتية عالية في الهيكل (HV Isolation Fault)": {
        "title": "P0AA6 - Hybrid Battery System Isolation Fault",
        "desc": "🚨 خطأ أمان حرج: وجود تسريب في الكهرباء العالية إلى جسم السيارة الخارجي، وتتوقف السيارة عن التشغيل لحماية الركاب.",
        "fix": "1. افصل مقبس الأمان العالي (HV Service Plug) فوراً قبل العمل.\n2. افحص العازلية باستعمال مقياس Megger 1000V.\n3. ابحث عن أي كبل عالي الفولتية ممزق أو رطوبة في صندوق البطارية أو الكمبريسور الكهربائي.",
        "video": "https://www.youtube.com/watch?v=0h94Lh1a6_s"
    },
    "P0A80 - استبدال/ضعف حزمة بطارية الهجين": {
        "title": "P0A80 - Replace Hybrid Battery Pack",
        "desc": "ضعف أو تباين الفولتية بين خلايا حزمة بطارية الضغط العالي.",
        "fix": "1. تنظيف مروحة تبريد البطارية المنسدة.\n2. فحص فولتية الخلايا عبر جهاز GDS/OBD لمشاهدة الخلايا الضعيفة.\n3. موازنة الخلايا أو استبدال التالف منها.",
        "video": "https://www.youtube.com/watch?v=R39S_kIna3k"
    },
    "P0A81 - عطل مروحة تبريد البطارية": {
        "title": "P0A81 - Hybrid Battery Pack Cooling Fan Control Circuit",
        "desc": "توقف أو ضعف مروحة تبريد البطارية الرئيسية، مما يؤدي لارتفاع حرارة البطارية وانخفاض عزم السيارة.",
        "fix": "1. تفقد وجود أتربة أو أوساخ تسد مجرى الهواء خلف المقاعد.\n2. فحص ريلي (Relay) المروحة وفيوز التغذية.\n3. تنظيف المروحة أو استبدالها في حال توقف المحرك الخاص بها.",
        "video": "https://www.youtube.com/watch?v=R39S_kIna3k"
    },
    "P0C73 - عطل مضخة تبريد نظام EV / الانفرتر": {
        "title": "P0C73 - Coolant Pump A Control Circuit Performance",
        "desc": "خلل في مضخة مياه التبريد الكهربائية الخاصة بالإنفرتر ومحرك الكهرباء.",
        "fix": "1. افحص مستوى سائل التبريد (Coolant) الخاص بنظام الـ EV.\n2. تفقد فيوز ريلي المضخة.\n3. تأكد من خروج الهواء من دورة التبريد (Bleeding).",
        "video": "https://www.youtube.com/watch?v=2eO712Pq6yU"
    },
    "P0A7F - تدهور كفاءة البطارية": {
        "title": "P0A7F - Hybrid Battery Pack Deterioration",
        "desc": "ارتفاع المقاومة الداخلية للبطارية مما يقلل المدى الشحني (Range) للسيارة.",
        "fix": "1. عمل إعادة معايرة لشحن البطارية (Cell Balancing).\n2. التأكد من تحديث السوفتوير الخاص بنظام إدارة البطارية (BMS).",
        "video": "https://www.youtube.com/watch?v=R39S_kIna3k"
    },
    "U0100 - انقطاع الاتصال مع عقل المحرك (ECM/PCM)": {
        "title": "U0100 - Lost Communication with ECM/PCM A",
        "desc": "عدم وجود استجابة من الكمبيوتر الرئيسي للسيارة عبر شبكة الـ CAN Bus.",
        "fix": "1. افحص سلامة بطارية 12V الصغرى ونظف أقطابها.\n2. افحص فيوزات العقل الرئيسي في صندوق الفيوزات.\n3. التأكد من سلامة التوصيلات وتأريض الكيبل الأرضي (Ground).",
        "video": "https://www.youtube.com/watch?v=2eO712Pq6yU"
    },
    "TPMS - تنبيه ضغط الهواء في الإطارات": {
        "title": "TPMS - Tire Pressure Monitoring System",
        "desc": "انخفاض الضغط في أحد الإطارات أو تلف حساس الإطار.",
        "fix": "1. اضبط ضغط الإطارات على 34 PSI.\n2. قيادة السيارة لمسافة 3-5 كم لإعادة المعايرة تلقائياً.\n3. إعادة ضبط من شاشة BYD الرئيسية.",
        "video": "https://www.youtube.com/watch?v=0h94Lh1a6_s"
    },
    "P0101 - خلل حساس تدفق الهواء (MAF)": {
        "title": "P0101 - Mass Air Flow Sensor Circuit Range/Performance",
        "desc": "قراءة غير صحيحة لحساس الهواء للمحركات الهجينة/البنزين.",
        "fix": "1. تنظيف حساس MAF بخاخ الكترونيات خاص (CRC).\n2. استبدال فلتر الهواء إذا كان متسخاً.",
        "video": "https://www.youtube.com/watch?v=xQGskW1316E"
    }
}

# --- أسلوب العرض 1: الاختيار من القائمة ---
selected_from_list = st.selectbox("📌 اختر كود العطل من القائمة السريعة:", list(faults_db.keys()))

# --- أسلوب العرض 2: البحث الكتابي ---
search_input = st.text_input("🔍 أو اكتب رمز العطل يدوياً للبحث (مثال: U0298, P0AA6):", "").strip().upper()

# تحديد الكود المراد عرضه
data_to_show = None

if search_input:
    # البحث المباشر بالنص
    found = False
    for key, data in faults_db.items():
        if search_input in key:
            data_to_show = data
            found = True
            break
    if not found:
        st.info(f"لم نجد الكود ({search_input}) مسجلاً في القائمة المحلية.")
        st.markdown(f"[🔍 اضغط هنا للبحث عن فيديو تصليح {search_input} على يوتيوب](https://www.youtube.com/results?search_query=BYD+{search_input}+repair)")

elif selected_from_list and selected_from_list != "اختر كود من القائمة...":
    data_to_show = faults_db[selected_from_list]

# عرض تفاصيل الكود إن وجد
if data_to_show and data_to_show["title"]:
    st.subheader(data_to_show["title"])
    st.error(f"**الوصف:**\n{data_to_show['desc']}")
    st.warning(f"**طريقة التصليح الخطوة بخطوة:**\n{data_to_show['fix']}")
    if data_to_show["video"]:
        st.write("🎥 **فيديو توضيحي للحل:**")
        st.video(data_to_show["video"])

st.markdown("---")
st.caption("إهداء خاص إلى قائد وأعضاء فريق BYD العراق ❤️")
