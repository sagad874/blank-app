import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="BYD Iraq Team - الورشة الذكية",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 الورشة الذكية لفريق BYD العراق")
st.caption("النسخة الميدانية التفاعلية | دليل تشخيصي قائم على خيارات ونتائج الفحص")

st.markdown("---")

# --- 2. دليل العدة المطلوبة ---
with st.expander("🛠️ دليل العدة المطلوبة وأماكن القطع الأساسية"):
    st.markdown("""
    قبل أن تبدأ بأي عطل، تأكد من توفر هذه العدة البسيطة بجانبك في الكراج:
    - مفكات براغي ومفتاح ربط (تثبيت) قياس 10 ملم.
    - بخاخ تنظيف إلكترونيات (Contact Cleaner) لتنظيف الفيش من الرطوبة والكلس.
    - جهاز فحص OBD2 بلوتوث لمسح الأخطاء.
    - جهاز الفولتميتر (Multimeter) لقياس الجهد.
    """)

st.markdown("---")

# --- 3. حاسبة التوفير ---
st.header("📊 حاسبة التوفير عبر العداد")
col1, col2 = st.columns(2)
with col1:
    prev_km = st.number_input("قراءة العداد السابقة (كم):", value=10000, step=100, min_value=0)
with col2:
    current_km = st.number_input("قراءة العداد الحالية (كم):", value=11500, step=100, min_value=0)

if current_km > prev_km:
    total_km = current_km - prev_km
    cost_gasoline = (total_km / 10) * 1000
    cost_ev = (total_km / 6) * 50
    savings = cost_gasoline - cost_ev
    st.success(f"💰 التوفير المالي للمسافة ({total_km:,} كم): **{int(savings):,} دينار عراقي**")

st.markdown("---")

# --- 4. بناء الدالة الديناميكية العامة لجميع الأكواد مع المنطق التفاعلي ---

@st.cache_data
def build_interactive_guide(code, title_desc):
    category = code[0]
    
    # تفاصيل خاصة بالأكواد الحرجة
    if code == "P0AA6":
        return {
            "title": f"{code} - تسريب فولتية عالية في الهيكل (HV Isolation Fault)",
            "danger": "🚨 تحذير أمان صارم: هذا العطل يتعلق بتسرب كهرباء الضغط العالي إلى هيكل السيارة. لا تلمس أي كيبل برتقالي أبداً قبل إتمام فصل المقبس!",
            "node_1": {
                "question": "الخطوة 1: افصل مقبس الأمان البرتقالي (HV Service Plug) وانتظر 5 دقائق. هل تم فصل التيار بنجاح؟",
                "options": {
                    "نعم، تم الفصل بأمان": "node_2",
                    "لا، توجد مشكلة في سحب المقبس": "fail_plug"
                }
            },
            "node_2": {
                "question": "الخطوة 2: افحص الكيبلات البرتقالية تحت السيارة. ماذا تلاحظ؟",
                "options": {
                    "توجد رطوبة أو ماء حول الفيش": "fix_wet",
                    "توجد أسلاك مجروحة تحت الشاصي": "fix_wire",
                    "جميع الكيبلات سليمة وظاهرياً ممتازة": "node_3"
                }
            },
            "node_3": {
                "question": "الخطوة 3: قس مقاومة العزل أو نظف فيش الكمبريسور. هل زال التماس؟",
                "options": {
                    "نعم، العزل ممتاز الآن": "pass_clear",
                    "لا، التماس ما زال قائماً": "fail_deep"
                }
            },
            "outcomes": {
                "fail_plug": "⚠️ لا تضغط بالقوة، راجع دليل المقابض لتفادي كسر القفل وتأكد من ارتداء قفازات العزل.",
                "fix_wet": "🛠️ الإجراء: جفف الفيش تماماً واستخدم بخاخ تنظيف الإلكترونيات، ثم أعد التركيب.",
                "fix_wire": "🛠️ الإجراء: قم بعزل السلك المجروح بشريط عزل حراري مخصص للضغط العالي.",
                "fail_deep": "⚠️ العطل داخلي في الإنفرتر أو بطارية الضغط العالي نفسها، يتطلب فحص الخلايا.",
                "pass_clear": "✅ تم الإصلاح بنجاح! أرجع مقبس الأمان وقم بمسح الكود باستخدام OBD2."
            },
            "video": "https://www.youtube.com/watch?v=0h94Lh1a6_s"
        }

    # المنطق العام والشامل المطبق على باقي الـ 100+ كود أوتوماتيكياً
    type_explanations = {
        "P": "منظومة المحرك، البطارية، أو الإنفرتر الكهربائي",
        "U": "شبكة الاتصالات الرقمية (CAN-Bus) بين الكمبيوترات",
        "C": "أنظمة الثبات والفرامل (ABS) والتوجيه",
        "B": "المقصورة الداخلية والوسائد الهوائية والتكييف"
    }
    
    general_desc = type_explanations.get(category, "الحساسات الإلكترونية والدوائر الكهربائية")

    return {
        "title": f"{code} - {title_desc}",
        "danger": f"ℹ️ نطاق العطل: {general_desc}. اتبع شجرة التشخيص الميدانية لتحديد السبب فوراً.",
        "node_1": {
            "question": "الخطوة 1 (فحص فولتية البطارية 12V): قم بقياس جهد البطارية الصغرى بالملتيميتر. كم القراءة لديك؟",
            "options": {
                "أقل من 11.5 فولت (منخفضة / فرغ شحنها)": "v_low",
                "بين 12.0 و 14.2 فولت (ضمن النطاق الطبيعي)": "node_2",
                "أعلى من 14.5 فولت (شحن زائد / عطل منظم)": "v_high"
            }
        },
        "node_2": {
            "question": "الخطوة 2 (فحص الفيشة والحساس): افصل الفيشة الموصلة بالحساس أو العقل. ماذا تلاحظ بداخلها؟",
            "options": {
                "توجد أتربة، كلس، أو رطوبة بداخلها": "clean_harness",
                "يوجد سلك مقطوع أو مجروح ظاهرياً": "fix_wire",
                "الفيشة نظيفة والأسلاك سليمة تماماً": "node_3"
            }
        },
        "node_3": {
            "question": "الخطوة 3 (فحص الفيوزات والتغذية): افحص الفيوز المخصص للدارة في علبة الفيوزات. ما هي حالته؟",
            "options": {
                "الفيوز محترق أو تالف": "replace_fuse",
                "الفيوز سليم وتصل الطاقة للحساس": "replace_sensor"
            }
        },
        "outcomes": {
            "v_low": "⚠️ الفولتية منخفضة جداً وتسبب أخطاء وهمية في العقول! قم بشحن البطارية أو استبدالها ثم أعد الفحص.",
            "v_high": "⚠️ يوجد شحن زائد عن الحد المسموح! افحص محول DC-DC أو منظومة الشحن قبل اتلاف الكمبيوترات.",
            "clean_harness": "🛠️ قم برش بخاخ تنظيف الإلكترونيات داخل الفيشة، جففها جيداً ثم أعد تركيبها بإحكام.",
            "fix_wire": "🛠️ قم بإصلاح السلك المقطوع وعزله جيداً بشريط عازل لمنع التماسه مع الشاصي.",
            "replace_fuse": "🛠️ استبدل الفيوز التالف بفيوز جديد من نفس الأمبير المخصص له في علبة الفيوزات.",
            "replace_sensor": "⚠️ الدائرة الكهربائية والتغذية سليمة. العطل يتركز في الحساس/المكون نفسه ويحتاج استبدال.",
            "pass_clear": "✅ تم معالجة السبب الرئيسي! يمكنك الآن مسح الكود عبر جهاز OBD2 واختبار القيادة."
        },
        "video": f"https://www.youtube.com/results?search_query=BYD+{code}+{title_desc.replace(' ', '+')}"
    }

@st.cache_data
def load_database():
    raw_codes_list = [
        ("TPMS", "تنبيه ضغط الهواء في الإطارات"),
        ("P0100", "حساس تدفق الهواء الرئيسي MAF Sensor"), ("P0101", "أداء حساس تدفق الهواء غير منتظم"),
        ("P0102", "فولتية حساس الهواء منخفضة جداً"), ("P0103", "فولتية حساس الهواء عالية جداً"),
        ("P0110", "حساس حرارة الهواء الداخل للمحرك IAT"), ("P0115", "حساس حرارة مياه التبريد للمحرك ECT"),
        ("P0120", "حساس دعسة البنزين أو بوابة الهواء TPS"), ("P0130", "حساس الشكمان (الأكسجين) الأول O2 Sensor"),
        ("P0300", "تفتفة عشوائية في أسطوانات المحرك متعددة"), ("P0301", "تفتفة واضحة في السلندر رقم 1"),
        ("P0302", "تفتفة واضحة في السلندر رقم 2"), ("P0303", "تفتفة واضحة في السلندر رقم 3"),
        ("P0304", "تفتفة واضحة في السلندر رقم 4"), ("P0420", "كفاءة دبة الرصاص (الكاتاليزم) منخفضة"),
        ("P0500", "حساس سرعة السيارة متوقف عن القراءة"), ("P0A1F", "عطل في وحدة التحكم بطاقة البطارية الهجينة"),
        ("P0A78", "أداء غير منتظم في إنفرتر محرك الدفع الأمامي"), ("P0A7F", "تدهور عام في خلايا بطارية الضغط العالي"),
        ("P0A81", "عطل في دارة مروحة تبريد البطارية الرئيسية"), ("P0A9C", "حساس درجة حرارة بطارية الهايبْريد معطل"),
        ("P0C73", "أداء مضخة التبريد الكهربائية للإنفرتر ضعيف"), ("P0D01", "فولتية إدخال شاحن السيارة الكهربائي منخفضة"),
        ("U0100", "انقطاع الاتصال مع عقل المحرك الرئيسي ECM"), ("U0101", "انقطاع الاتصال مع عقل القير"),
        ("U0110", "انقطاع الاتصال مع عقل محرك الحركة الكهربائي"), ("U0111", "انقطاع الاتصال مع عقل إدارة البطارية BMS"),
        ("U0121", "انقطاع الاتصال مع عقل الفرامل ABS"), ("U0140", "انقطاع الاتصال مع عقل جسم السيارة BCM"),
        ("U0155", "انقطاع الاتصال مع شاشة العدادات الرئيسية"), ("C1201", "عطل عام في نظام التحكم بمحرك الـ ABS"),
        ("C1241", "جهد التغذية الكهربائية لوحدة الـ ABS منخفض جداً"), ("C1300", "عطل داخلي في كمبيوتر الفرامل ABS ECU"),
        ("C1511", "عطل في حساس العزم الخاص بمقود القيادة الكهربائي"), ("B1000", "عطل داخلي في عقل الوسائد الهوائية Airbag"),
        ("B1211", "دائرة شد أمان حزام الأمان مفتوحة أو تالفة"), ("B2799", "عطل في نظام مانع السرقة وبصمة التشغيل")
    ]

    for i in range(1, 65):
        extra_code = f"P0{200+i:03d}"
        raw_codes_list.append((extra_code, f"Diagnostic Code {extra_code} System Circuit"))

    db = {}
    for code_key, name_key in raw_codes_list:
        db[f"{code_key} - {name_key}"] = build_interactive_guide(code_key, name_key)
    return db

workshop_db = load_database()

# --- 5. قوائم الاختيار والبحث ---
st.header("🔧 الموسوعة الميدانية الشاملة للأعطال")

search_query = st.text_input("🔍 ابحث برقم الكود مباشرة (مثال: P0AA6, P0100, C1241):").strip()

chosen_data = None

if search_query:
    filtered_keys = [k for k in workshop_db.keys() if search_query.lower() in k.lower()]
    if filtered_keys:
        selected_code = st.selectbox("📌 النتائج المطابقة للبحث:", filtered_keys)
        chosen_data = workshop_db[selected_code]
    else:
        st.warning(f"لم نجد الكود ({search_query}) بالنظام.")
        st.markdown(f"[🔍 ابحث عن الشرح الميداني لـ {search_query} على يوتيوب](https://www.youtube.com/results?search_query=BYD+{search_query}+repair+guide)")
else:
    options = ["اختر كود من القائمة..."] + list(workshop_db.keys())
    selected_code = st.selectbox("📌 اختر كود العطل من القائمة (+100 كود):", options)
    if selected_code != "اختر كود من القائمة...":
        chosen_data = workshop_db[selected_code]

# --- 6. محرك التشخيص التفاعلي (Interactive Engine) ---
if chosen_data:
    st.markdown("---")
    st.subheader(chosen_data["title"])
    st.error(chosen_data["danger"])
    
    st.markdown("### 🛠️ شجرة التشخيص التفاعلية:")

    # إدارة حالة العقدة الحالية داخل الجلسة
    if "current_node" not in st.session_state or st.session_state.get("active_title") != chosen_data["title"]:
        st.session_state.current_node = "node_1"
        st.session_state.active_title = chosen_data["title"]

    node_key = st.session_state.current_node

    # إذا كانت العقدة الحالية سؤالاً تفاعلياً
    if node_key in chosen_data:
        node_info = chosen_data[node_key]
        
        st.info(f"**{node_info['question']}**")
        
        # عرض الاختيارات
        user_choice = st.radio("حدد النتيجة أو القراءة الميدانية:", list(node_info["options"].keys()))
        
        if st.button("تأكيد النتيجة والانتقال للخطوة التالية 🔗"):
            next_step = node_info["options"][user_choice]
            st.session_state.current_node = next_step
            st.rerun()

    # إذا وصل المستخدم إلى نتيجة تشخيصية (Outcome)
    elif node_key in chosen_data["outcomes"]:
        outcome_msg = chosen_data["outcomes"][node_key]
        
        if "✅" in outcome_msg:
            st.success(outcome_msg)
            st.balloons()
        elif "🛠️" in outcome_msg:
            st.warning(outcome_msg)
            if st.button("تم تطبيق الإصلاح، انتقال لمسح الكود ➡️"):
                st.session_state.current_node = "pass_clear"
                st.rerun()
        else:
            st.error(outcome_msg)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 إعادة تشخيص هذا الكود من البداية"):
            st.session_state.current_node = "node_1"
            st.rerun()

    # الفيديو التوضيحي
    if chosen_data.get("video"):
        st.markdown("---")
        st.write("🎥 **فيديو توضيحي تفصيلي للمساعدة:**")
        if "watch?v=" in chosen_data["video"]:
            st.video(chosen_data["video"])
        else:
            st.markdown(f"[▶️ اضغط هنا لمشاهدة فيديو الصيانة على يوتيوب]({chosen_data['video']})")

st.markdown("---")
st.caption("إهداء خاص إلى قائد وأعضاء فريق BYD العراق ❤️ - صُمم ليكون دليلك الميداني الأول")
