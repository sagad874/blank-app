import streamlit as st

# ═══════════════════════════════════════════════
# إعداد الصفحة
# ═══════════════════════════════════════════════

st.set_page_config(
    page_title="BYD Iraq | الورشة الذكية",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 الورشة الذكية لفريق BYD العراق")
st.caption("نظام تشخيص تفاعلي — الكود ← الفحص ← النتيجة ← الفحص التالي")

st.markdown("---")


# ═══════════════════════════════════════════════
# أدوات الواجهة
# ═══════════════════════════════════════════════

def step(no, arabic, english=""):
    st.markdown(
        f"""
        <div style="
            background:#222;
            color:white;
            padding:9px;
            border-radius:10px;
            text-align:center;
            font-size:20px;
            font-weight:bold;
            margin-top:15px;
            margin-bottom:10px;">
            STEP {no}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            direction:rtl;
            text-align:right;
            font-size:18px;
            padding:10px;
            border:1px solid #444;
            border-radius:8px;">
            🔧 {arabic}
        </div>
        """,
        unsafe_allow_html=True
    )

    if english:
        st.code(english, language="text")


def result(title, text, kind="success"):
    if kind == "error":
        st.error(f"🛑 {title}\n\n{text}")
    elif kind == "warning":
        st.warning(f"⚠️ {title}\n\n{text}")
    else:
        st.success(f"✅ {title}\n\n{text}")


# ═══════════════════════════════════════════════
# قاعدة الأكواد
# ═══════════════════════════════════════════════

raw_codes = [

    # ───────── Engine ─────────
    ("P0100", "حساس تدفق الهواء MAF"),
    ("P0101", "أداء حساس MAF"),
    ("P0102", "إشارة MAF منخفضة"),
    ("P0103", "إشارة MAF عالية"),
    ("P0110", "حساس حرارة الهواء IAT"),
    ("P0115", "حساس حرارة المحرك ECT"),
    ("P0120", "حساس الدعسة / TPS"),
    ("P0130", "حساس الأوكسجين O2"),
    ("P0300", "تفتفة عشوائية"),
    ("P0301", "تفتفة الأسطوانة 1"),
    ("P0302", "تفتفة الأسطوانة 2"),
    ("P0303", "تفتفة الأسطوانة 3"),
    ("P0304", "تفتفة الأسطوانة 4"),
    ("P0420", "كفاءة المحول الحفاز منخفضة"),
    ("P0500", "حساس سرعة السيارة"),

    # ───────── EV / HV ─────────
    ("P0A1F", "وحدة التحكم بطاقة البطارية"),
    ("P0A78", "إنفرتر محرك الدفع"),
    ("P0A7F", "تدهور بطارية HV"),
    ("P0A81", "مروحة تبريد بطارية HV"),
    ("P0A9C", "حساس حرارة بطارية HV"),
    ("P0AA6", "HV Isolation Fault"),
    ("P0C73", "مضخة تبريد الإنفرتر"),
    ("P0D01", "شاحن السيارة"),

    # ───────── Communication ─────────
    ("U0100", "فقدان الاتصال مع ECM"),
    ("U0101", "فقدان الاتصال مع TCM"),
    ("U0110", "فقدان الاتصال مع محرك الدفع"),
    ("U0111", "فقدان الاتصال مع BMS"),
    ("U0121", "فقدان الاتصال مع ABS"),
    ("U0140", "فقدان الاتصال مع BCM"),
    ("U0155", "فقدان الاتصال مع العدادات"),
    ("U0298", "فقدان الاتصال مع DC/DC"),

    # ───────── Chassis ─────────
    ("C1201", "نظام ABS / الثبات"),
    ("C1241", "جهد ABS منخفض"),
    ("C1300", "عطل داخلي ABS"),
    ("C1511", "حساس عزم المقود"),

    # ───────── Body ─────────
    ("B1000", "عطل وحدة Airbag"),
    ("B1211", "دائرة حزام الأمان"),
    ("B2799", "نظام مانع السرقة")
]


# أكواد إضافية للقائمة
for i in range(1, 65):
    code = f"P0{200+i:03d}"
    raw_codes.append(
        (code, f"Diagnostic Code {code}")
    )

codes = dict(raw_codes)


# ═══════════════════════════════════════════════
# محرك التشخيص
# ═══════════════════════════════════════════════

def diagnose(code):

    # ╔══════════════════════════════════════════╗
    # P0AA6
    # ╚══════════════════════════════════════════╝

    if code == "P0AA6":

        st.subheader("P0AA6 — HV Isolation Fault")

        st.error(
            "🚨 تحذير HV: هذا الكود مرتبط بعزل منظومة الجهد العالي. "
            "لا تلمس مكونات HV أو الكابلات البرتقالية بدون "
            "إجراء BYD الصحيح ومعدات السلامة المناسبة."
        )

        step(
            1,
            "هل توجد أكواد أخرى مسجلة مع P0AA6؟",
            "Are there additional HV-related DTCs?"
        )

        a = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="p0aa6_1"
        )

        if a == "نعم":
            result(
                "ابدأ بالكود المصاحب",
                "الكود المصاحب قد يحدد النظام أو الجزء المسؤول بشكل أدق. "
                "لا تعتمد على P0AA6 وحده.",
                "warning"
            )
            return

        step(
            2,
            "هل ظهر العطل بعد ماء أو غسيل أو حادث أو صيانة؟",
            "Did the fault appear after water exposure, impact, or service?"
        )

        b = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="p0aa6_2"
        )

        if b == "نعم":
            result(
                "مسار الرطوبة / الضرر",
                "افحص آثار الرطوبة أو الضرر الخارجي واتبع إجراء BYD "
                "الخاص بالموديل قبل أي عمل على HV.",
                "warning"
            )
            return

        step(
            3,
            "هل يعود الكود مباشرة بعد المسح؟",
            "Does P0AA6 return immediately after clearing?"
        )

        c = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="p0aa6_3"
        )

        if c == "نعم":
            result(
                "العطل مستمر",
                "يلزم اختبار عزل HV حسب إجراء المصنع. "
                "لا تستبدل قطعة عشوائياً.",
                "error"
            )
        else:
            result(
                "العطل متقطع",
                "سجّل ظروف ظهور الكود وراقب عودته. "
                "اختفاء الكود لا يعني بالضرورة انتهاء السبب."
            )

        return


    # ╔══════════════════════════════════════════╗
    # U0298
    # ╚══════════════════════════════════════════╝

    if code == "U0298":

        st.subheader("U0298 — DC/DC Communication")

        step(
            1,
            "هل توجد أكواد U أخرى أو أكواد مرتبطة بـ 12V؟",
            "Are there additional communication or 12V-related DTCs?"
        )

        a = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="u0298_1"
        )

        if a == "نعم":
            result(
                "ابدأ بالأكواد المصاحبة",
                "وجود أكثر من كود اتصال قد يغيّر اتجاه التشخيص.",
                "warning"
            )
            return

        step(
            2,
            "هل بطارية 12V وتغذيتها ضمن المواصفات؟",
            "Is the 12V battery and its supply within specification?"
        )

        b = st.radio(
            "النتيجة:",
            ["نعم", "لا", "غير متأكد"],
            key="u0298_2"
        )

        if b == "لا":
            result(
                "ابدأ بمنظومة 12V",
                "عالج مشكلة البطارية أو التغذية أولاً ثم أعد الفحص."
            )
            return

        if b == "غير متأكد":
            result(
                "تحقق من 12V أولاً",
                "لا تنتقل لاستبدال وحدة DC/DC قبل التأكد من التغذية "
                "والأرضي حسب مواصفات السيارة.",
                "warning"
            )
            return

        step(
            3,
            "هل فيوزات وتغذية DC/DC سليمة؟",
            "Are the DC/DC power supply and fuses OK?"
        )

        c = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="u0298_3"
        )

        if c == "لا":
            result(
                "مسار التغذية",
                "شخّص الفيوز والتغذية والأسلاك حسب مخطط السيارة."
            )
            return

        step(
            4,
            "هل الوحدة لا تتصل رغم سلامة التغذية؟",
            "Is communication still lost despite correct power?"
        )

        d = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="u0298_4"
        )

        if d == "نعم":
            result(
                "مسار CAN / الوحدة",
                "انتقل إلى فحص شبكة CAN والتوصيلات والوحدة "
                "وفق مخطط BYD."
            )
        else:
            result(
                "العطل يحتاج بيانات إضافية",
                "افحص الأكواد وLive Data قبل استبدال أي قطعة.",
                "warning"
            )

        return


    # ╔══════════════════════════════════════════╗
    # MAF
    # ╚══════════════════════════════════════════╝

    if code in ["P0100", "P0101", "P0102", "P0103"]:

        st.subheader(f"{code} — MAF Sensor")

        step(
            1,
            "هل توجد أكواد أخرى مرتبطة بالمحرك؟",
            "Are there additional engine-related DTCs?"
        )

        a = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key=f"{code}_1"
        )

        if a == "نعم":
            result(
                "افحص الأكواد المصاحبة",
                "قد يكون الكود المصاحب هو المفتاح لتحديد السبب."
            )
            return

        step(
            2,
            "هل فيشة MAF والأسلاك سليمة بصرياً؟",
            "Are the MAF connector and wiring visually OK?"
        )

        b = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key=f"{code}_2"
        )

        if b == "لا":
            result(
                "ابدأ بالتوصيلات",
                "أصلح مشكلة الفيشة أو الأسلاك ثم أعد الفحص."
            )
            return

        step(
            3,
            "هل قراءة MAF في Live Data منطقية؟",
            "Is the MAF Live Data plausible?"
        )

        c = st.radio(
            "النتيجة:",
            ["نعم", "لا", "غير متأكد"],
            key=f"{code}_3"
        )

        if c == "نعم":
            result(
                "ابحث عن سبب آخر",
                "لا تستبدل الحساس لمجرد وجود الكود إذا كانت القراءة منطقية."
            )

        elif c == "لا":
            result(
                "مسار MAF",
                "افحص التغذية والأرضي والإشارة والأسلاك حسب مخطط السيارة."
            )

        else:
            result(
                "نحتاج Live Data",
                "احصل على قراءة MAF وقارنها بمواصفات BYD.",
                "warning"
            )

        return


    # ╔══════════════════════════════════════════╗
    # جميع أكواد U
    # ╚══════════════════════════════════════════╝

    if code.startswith("U"):

        st.subheader(f"{code} — Communication Fault")

        step(
            1,
            "هل توجد أكواد U أخرى؟",
            "Are there additional communication DTCs?"
        )

        a = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key=f"{code}_u1"
        )

        if a == "نعم":
            result(
                "افحص شبكة الاتصال أولاً",
                "وجود عدة وحدات متأثرة قد يشير إلى مشكلة مشتركة "
                "في التغذية أو شبكة الاتصال."
            )
            return

        step(
            2,
            "هل الوحدة المتأثرة لديها Power وGround صحيحان؟",
            "Does the affected module have correct power and ground?"
        )

        b = st.radio(
            "النتيجة:",
            ["نعم", "لا", "غير متأكد"],
            key=f"{code}_u2"
        )

        if b == "لا":
            result(
                "مسار التغذية",
                "افحص الفيوز والتغذية والأرضي حسب مخطط السيارة."
            )
            return

        if b == "غير متأكد":
            result(
                "تحقق من Power / Ground",
                "تأكد من التغذية والأرضي قبل الحكم على الوحدة.",
                "warning"
            )
            return

        step(
            3,
            "هل فقدان الاتصال متقطع؟",
            "Is the communication loss intermittent?"
        )

        c = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key=f"{code}_u3"
        )

        if c == "نعم":
            result(
                "مسار اتصال متقطع",
                "افحص الأسلاك والفيش وشبكة CAN حسب مخطط السيارة."
            )
        else:
            result(
                "مسار فقدان اتصال ثابت",
                "انتقل إلى فحص CAN والوحدة والتغذية وفق إجراء المصنع."
            )

        return


    # ╔══════════════════════════════════════════╗
    # المسار العام لبقية الأكواد
    # ╚══════════════════════════════════════════╝

    st.subheader(f"{code} — {codes.get(code, 'Diagnostic Code')}")

    step(
        1,
        "هل توجد أكواد أخرى مرتبطة بنفس النظام؟",
        "Are there additional DTCs related to the same system?"
    )

    a = st.radio(
        "النتيجة:",
        ["نعم", "لا"],
        key=f"{code}_g1"
    )

    if a == "نعم":
        result(
            "ابدأ بالكود المصاحب",
            "الكود المصاحب قد يحدد السبب بشكل أدق.",
            "warning"
        )
        return

    step(
        2,
        "هل العطل موجود حالياً أم الكود تاريخي فقط؟",
        "Is the fault currently present or only stored?"
    )

    b = st.radio(
        "النتيجة:",
        ["موجود حالياً", "تاريخي فقط"],
        key=f"{code}_g2"
    )

    if b == "تاريخي فقط":
        result(
            "راقب العطل",
            "بعد اتباع إجراء المسح المناسب، راقب هل يعود الكود."
        )
        return

    step(
        3,
        "هل الفيوزات والتوصيلات المرتبطة بالنظام سليمة؟",
        "Are the related fuses and connectors OK?"
    )

    c = st.radio(
        "النتيجة:",
        ["نعم", "لا"],
        key=f"{code}_g3"
    )

    if c == "لا":
        result(
            "ابدأ بالتغذية والتوصيلات",
            "أصلح المشكلة ثم أعد الفحص قبل استبدال المكونات."
        )
    else:
        result(
            "انتقل للاختبار المتخصص",
            "استخدم Live Data أو اختبار الوحدة أو مخطط المصنع "
            "حسب نوع النظام.",
            "warning"
        )


# ═══════════════════════════════════════════════
# اختيار الكود
# ═══════════════════════════════════════════════

st.header("🔎 تشخيص العطل")

search = st.text_input(
    "🔍 اكتب الكود يدوياً:",
    placeholder="مثال: P0AA6 أو U0298"
).strip().upper()

selected = st.selectbox(
    "📋 أو اختر الكود من القائمة:",
    ["اختر كود العطل..."] +
    [f"{c} — {n}" for c, n in raw_codes]
)

if search:
    chosen_code = search
elif selected != "اختر كود العطل...":
    chosen_code = selected.split(" — ")[0]
else:
    chosen_code = ""

if chosen_code:

    if chosen_code in codes:

        st.markdown("---")

        st.info(
            f"🔎 **الكود:** {chosen_code}\n\n"
            f"📌 **الوصف:** {codes[chosen_code]}"
        )

        diagnose(chosen_code)

    else:

        st.error(
            f"❌ الكود {chosen_code} غير موجود في قاعدة البيانات."
        )


# ═══════════════════════════════════════════════
# حاسبة التوفير
# ═══════════════════════════════════════════════

st.markdown("---")

with st.expander("📊 حاسبة التوفير عبر العداد"):

    col1, col2 = st.columns(2)

    with col1:
        previous = st.number_input(
            "قراءة العداد السابقة:",
            value=10000,
            step=100
        )

    with col2:
        current = st.number_input(
            "قراءة العداد الحالية:",
            value=11500,
            step=100
        )

    if current > previous:

        distance = current - previous

        gasoline = (distance / 10) * 1000
        electric = (distance / 6) * 50
        saving = gasoline - electric

        st.success(
            f"💰 التوفير لمسافة {distance:,} كم: "
            f"{int(saving):,} د.ع"
        )

    elif current < previous:

        st.warning("قراءة العداد الحالية أقل من السابقة.")


# ═══════════════════════════════════════════════
# النهاية
# ═══════════════════════════════════════════════

st.markdown("---")

st.caption(
    "❤️ BYD Iraq Team | الورشة الذكية "
    "— التشخيص التفاعلي الميداني"
)
