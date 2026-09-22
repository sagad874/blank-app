import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="BYD Iraq Team - الورشة الذكية",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 الورشة الذكية لفريق BYD العراق")
st.caption("النسخة الميدانية التفاعلية | شجرة التشخيص المباشرة القائمة على نتائج الفحص")

st.markdown("---")

# --- 2. حاسبة التوفير ---
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

# --- 3. محرك توليد أشجار التشخيص المخصصة بدقة لكل نوع عطل ---

@st.cache_data
def build_custom_tree(code, title_desc):
    category = code[0]
    
    # ------------------ أكواد خاصة ومحددة جداً ------------------
    if code == "P0AA6":
        return {
            "title": f"{code} - تسريب فولتية عالية في الهيكل",
            "danger": "🚨 تحذير أمان صارم: خطورة عالية من كهرباء الضغط العالي. لا تلمس الكيبلات البرتقالية بدون عزل!",
            "step_1": {
                "question": "الخطوة 1: قم بفصل مقبس الأمان البرتقالي (HV Service Plug). ما هي نتيجة الفحص الميداني؟",
                "options": {
                    "تم فصل المقبس بنجاح وانتظار 5 دقائق": "step_2",
                    "تعذر سحب المقبس أو القفل مكسور": "out_plug_err"
                }
            },
            "step_2": {
                "question": "الخطوة 2: افحص الكيبلات البرتقالية أسفل السيارة وبجوار الكمبريسور. ماذا تلاحظ؟",
                "options": {
                    "توجد رطوبة أو ماء داخل فيشة الكمبريسور": "out_wet",
                    "توجد جروح أو احتكاك بالأسلاك مع الشاصي": "out_wire",
                    "جميع الأسلاك جافة وسليمة تماماً": "step_3"
                }
            },
            "step_3": {
                "question": "الخطوة 3: افحص مقاومة العزل بجهاز الملتيميتر. ما هي القراءة؟",
                "options": {
                    "المقاومة عالية وسليمة (أعلى من 500 كيلو أوم)": "out_pass",
                    "المقاومة منخفضة (يوجد تسريب داخلي)": "out_internal"
                }
            },
            "outcomes": {
                "out_plug_err": "⚠️ حذارِ من استخدام القوة المفرطة. استخدم عتلة الأمان المخصصة وارتدِ قفازات العزل 1000V.",
                "out_wet": "🛠️ الحل: نظف الفيشة بماء مقطر ثم جففها تماماً وبخها ببخاخ تنظيف الإلكترونيات.",
                "out_wire": "🛠️ الحل: قم بعزل الجزء المجروح من الكيبل بتيب حراري عازل للضغط العالي.",
                "out_internal": "🚨 العطل داخلي في أنفرتر محرك الدفع أو خلايا البطارية الرئيسية، يحتاج فحص مختص.",
                "out_pass": "✅ تم التأكد من سلامة العزل! يمكنك إعادة المقبس ومسح الكود بـ OBD2."
            },
            "video": "https://www.youtube.com/watch?v=0h94Lh1a6_s"
        }

    # ------------------ مولد الأشجار المخصصة بحسب نوع الكود ------------------
    
    # 1. أكواد التفتفة والسلندرات (P0300 - P0304)
    if code.startswith("P030"):
        return {
            "title": f"{code} - {title_desc}",
            "danger": "⚠️ هذا العطل يسبب احتراقاً غير كامل واهتزازاً في المحرك وتأخيراً في التسارع.",
            "step_1": {
                "question": f"الخطوة 1 (فحص الكويل والبلكات): افحص الكويل والبلك الخاص بالسلندر المذكور. ماذا تلاحظ؟",
                "options": {
                    "البلك مستهلك أو عليه آثار زيت/كربون": "out_spark",
                    "الكويل لا يخرج شرارة كهربائية": "out_coil",
                    "البلك والكويل بحالة ممتازة": "step_2"
                }
            },
            "step_2": {
                "question": "الخطوة 2 (فحص نوزل الوقود): قم بقياس إشارة نوزل البنزين للسلندر. ما هي النتيجة؟",
                "options": {
                    "الفيشة تسرب بنزين أو لا تصلها إشارة": "out_nozzle",
                    "النوزل يعمل بشكل سليم": "out_comp"
                }
            },
            "outcomes": {
                "out_spark": "🛠️ الحل: استبدل طقم البلكات (شمعات الاحتراق) بنوعية أصلية مطابقة لسيارات BYD.",
                "out_coil": "🛠️ الحل: استبدل الكويل التالف وافحص الفيشة الموصلة له.",
                "out_nozzle": "🛠️ الحل: نظف نوزل الوقود أو استبدل الفيشة المتضررة.",
                "out_comp": "⚠️ المشكلة قد تكون انخفاض ضغط السلندر (Compression)، افحص ضغط السلندر في الورشة."
            },
            "video": f"https://www.youtube.com/results?search_query=BYD+{code}+{title_desc}"
        }

    # 2. أكواد الفرامل والـ ABS (تبدأ بـ C)
    elif category == "C":
        return {
            "title": f"{code} - {title_desc}",
            "danger": "⚠️ هذا العطل يؤثر على نظام الفرامل مانع الانغلاق وثبات السيارة.",
            "step_1": {
                "question": f"الخطوة 1 (فحص حساس السرعة على العجلات): افحص الفيشة والأسلاك المتصلة بعجلات السيارة. ماذا تلاحظ؟",
                "options": {
                    "توجد أتربة كثيفة أو رايش حديد على الحساس": "out_clean_abs",
                    "السلك الموصل للحساس مقطوع أو مجروح": "out_wire_abs",
                    "الحساس والأسلاك نظيفة وسليمة ظاهرياً": "step_2"
                }
            },
            "step_2": {
                "question": "الخطوة 2 (فحص تغذية كمبيوتر ABS): قس الفولتية الواصلة لفيشة الـ ABS الرئيسية. كم هي القراءة؟",
                "options": {
                    "أقل من 12 فولت (تغذية ضعيفة)": "out_fuse_abs",
                    "12 فولت كاملة وسليمة": "out_unit_abs"
                }
            },
            "outcomes": {
                "out_clean_abs": "🛠️ الحل: نظف رأس الحساس ومكان القراءة على العجلة ببخاخ تنظيف ورش الفيشة.",
                "out_wire_abs": "🛠️ الحل: قم بإصلاح وتلحيم سلك الحساس وعزله جيداً عن الماء.",
                "out_fuse_abs": "🛠️ الحل: افحص فيوز الـ ABS الرئيسي في علبة المحرك واستبدله إذا كان محترقاً.",
                "out_unit_abs": "⚠️ العطل في وحدة التحكم الهيدروليكية (ABS Module) نفسها وتطلب إعادة برمجة أو استبدال."
            },
            "video": f"https://www.youtube.com/results?search_query=BYD+{code}+ABS"
        }

    # 3. أكواد شبكة الاتصالات CAN-Bus (تبدأ بـ U)
    elif category == "U":
        return {
            "title": f"{code} - {title_desc}",
            "danger": "⚠️ عطل في شبكة الاتصال الرقمية يسبب توقف انتقال البيانات بين عقول السيارة.",
            "step_1": {
                "question": f"الخطوة 1 (فحص التوصيلات): افصل الفيشة الرئيسية للعقل المعني. ما هي حالتها؟",
                "options": {
                    "توجد رطوبة، كلس أبيض، أو دبابيس متثنية": "out_pins",
                    "الفيشة نظيفة ومثبتة بإحكام": "step_2"
                }
            },
            "step_2": {
                "question": "الخطوة 2 (فحص مقاومة خطوط CAN): قس المقاومة بين خطي (CAN-H و CAN-L) بمنفذ OBD2 والسيارة مطفأة. كم القراءة؟",
                "options": {
                    "تقريباً 60 أوم (القراءة المثالية)": "out_restart",
                    "120 أوم أو مفتوحة (يوجد انقطاع بالشبكة)": "out_can_cut"
                }
            },
            "outcomes": {
                "out_pins": "🛠️ الحل: عدل الدبابيس المتثنية بحذر ونظف الكلس ببخاخ إلكترونيات جاف.",
                "out_can_cut": "🛠️ الحل: يوجد انقطاع في أحد أسلاك شبكة الـ CAN، تتبع الأسلاك المجدولة للبحث عن القطع.",
                "out_restart": "✅ خطوط الاتصال سليمة، أعد فصل بطارية 12V لمدة 5 دقائق لإعادة تعيين العقول ثم امسح الكود."
            },
            "video": f"https://www.youtube.com/results?search_query=BYD+{code}+CAN+bus"
        }

    # 4. الشجرة العامة لأكواد الحساسات والمحرك (تبدأ بـ P أو B)
    else:
        return {
            "title": f"{code} - {title_desc}",
            "danger": "ℹ️ اتبع الخطوات الميدانية المخصصة لهذا الحساس لتحديد سبب المشكلة بدقة.",
            "step_1": {
                "question": f"الخطوة 1 (فحص فيشة وسلك القطعة): حدد موقع القطعة الخاصة بـ ({title_desc}) وافحص الفيشة. ماذا تلاحظ؟",
                "options": {
                    "توجد أتربة، رطوبة، أو الفيشة مرخية": "out_clean",
                    "يوجد سلك مقطوع أو مجروح": "out_wire",
                    "الفيشة موصولة بإحكام والأسلاك ممتازة": "step_2"
                }
            },
            "step_2": {
                "question": "الخطوة 2 (فحص التغذية والفيوز): قس الفولتية الواصلة للفيشة باستخدام الملتيميتر. كم هي القراءة؟",
                "options": {
                    "لا توجد تغذية (0 فولت)": "out_fuse",
                    "توجد تغذية سليمة (5 فولت أو 12 فولت حسب الحساس)": "out_sensor"
                }
            },
            "outcomes": {
                "out_clean": "🛠️ الحل: بَخ داخل الفيشة ببخاخ تنظيف الإلكترونيات واكبس القفل بإحكام.",
                "out_wire": "🛠️ الحل: أصلح السلك المقطوع واعزله جيداً لمنع التماسه مع الشاصي.",
                "out_fuse": "🛠️ الحل: راجع مخطط علبة الفيوزات واستبدل الفيوز التالف المخصص لهذه الدائرة.",
                "out_sensor": "⚠️ التغذية والأسلاك سليمة تماماً. العطل داخلي في الحساس نفسه ويحتاج استبدال قطعة جديدة."
            },
            "video": f"https://www.youtube.com/results?search_query=BYD+{code}+{title_desc}"
        }

# --- 4. تحميل قاعدة البيانات ---

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
        db[f"{code_key} - {name_key}"] = build_custom_tree(code_key, name_key)
    return db

workshop_db = load_database()

# --- 5. واجهة البحث والاختيار ---
st.header("🔧 الموسوعة الميدانية الشاملة للأعطال")

search_query = st.text_input("🔍 ابحث برقم الكود مباشرة (مثال: P0301, C1241, U0100, P0AA6):").strip()

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

# --- 6. التشغيل التفاعلي لشجرة القرارات المخصصة ---
if chosen_data:
    st.markdown("---")
    st.subheader(chosen_data["title"])
    st.error(chosen_data["danger"])
    
    st.markdown("### 🛠️ شجرة التشخيص التفاعلية:")

    # إدارة حالة العقدة الحالية داخل الجلسة
    if "current_step" not in st.session_state or st.session_state.get("active_code") != chosen_data["title"]:
        st.session_state.current_step = "step_1"
        st.session_state.active_code = chosen_data["title"]

    step_key = st.session_state.current_step

    # 1. إذا كنا في مرحلة سؤال واختيارات
    if step_key in chosen_data:
        step_data = chosen_data[step_key]
        
        st.info(f"**{step_data['question']}**")
        
        # الخيارات التفاعلية المخصصة لهذه الخطوة
        user_choice = st.radio("حدد النتيجة أو القراءة الميدانية:", list(step_data["options"].keys()))
        
        if st.button("تأكيد النتيجة والانتقال للخطوة التالية 🔗"):
            next_target = step_data["options"][user_choice]
            st.session_state.current_step = next_target
            st.rerun()

    # 2. إذا وصل التشخيص إلى النتيجة النهائية (Outcome)
    elif step_key in chosen_data["outcomes"]:
        outcome_text = chosen_data["outcomes"][step_key]
        
        if "🛠️" in outcome_text:
            st.warning(outcome_text)
            if st.button("تم تطببق الإصلاح، انتقل لمسح الكود ➡️"):
                st.session_state.current_step = "out_pass" if "out_pass" in chosen_data["outcomes"] else "pass_generic"
                st.rerun()
        elif "🚨" in outcome_text or "⚠️" in outcome_text:
            st.error(outcome_text)
        else:
            st.success(outcome_text)
            st.balloons()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 إعادة تشخيص هذا الكود من البداية"):
            st.session_state.current_step = "step_1"
            st.rerun()

    elif step_key == "pass_generic":
        st.success("✅ تم معالجة السبب بنجاح! قم الآن بمسح الكود بواسطة جهاز OBD2 واختبار السيارة.")
        st.balloons()
        if st.button("🔄 إعادة التشخيص"):
            st.session_state.current_step = "step_1"
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
