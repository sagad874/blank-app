import streamlit as st

st.set_page_config(
    page_title="BYD Iraq | الورشة الذكية",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 الورشة الذكية | BYD Iraq")
st.caption("نظام تشخيص تفاعلي: الكود → الفحص → النتيجة → الفحص التالي")
st.markdown("---")


# ═══════════════════════════════════════════════
# أدوات الواجهة
# ═══════════════════════════════════════════════

def step(no, ar, en=""):
    st.markdown(
        f"""
        <div style="font-size:24px;font-weight:bold;
        padding:8px 14px;border-radius:10px;
        background:#222;color:white;text-align:center">
        STEP {no}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"### 🔧 {ar}")

    if en:
        st.code(en, language="text")


def finish(title, text, color="green"):
    if color == "red":
        st.error(f"🛑 {title}\n\n{text}")
    elif color == "yellow":
        st.warning(f"⚠️ {title}\n\n{text}")
    else:
        st.success(f"✅ {title}\n\n{text}")


# ═══════════════════════════════════════════════
# مسارات التشخيص
# ═══════════════════════════════════════════════

def diagnose(code):

    # ───────────────────────────────────────────
    # P0AA6
    # ───────────────────────────────────────────

    if code == "P0AA6":

        st.subheader("P0AA6 — HV Isolation Fault")

        st.error(
            "🚨 عطل متعلق بعزل منظومة الجهد العالي. "
            "لا يتم فتح أو لمس مكونات HV إلا بواسطة فني مؤهل "
            "وبحسب إجراء BYD الخاص بالموديل."
        )

        step(
            1,
            "هل توجد أكواد جهد عالٍ أخرى مسجلة مع P0AA6؟",
            "Are there additional HV-related DTCs?"
        )

        a = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="p0aa6_1"
        )

        if a == "نعم":
            finish(
                "ابدأ بالكود المصاحب",
                "الكود المصاحب قد يحدد الجزء أو الوحدة المسؤولة. "
                "لا تعتمد على P0AA6 وحده لتحديد القطعة."
            )
            return

        step(
            2,
            "هل ظهر العطل مباشرة بعد حادث، ماء، غسيل قوي، أو صيانة؟",
            "Did the fault appear after water exposure, impact, or service?"
        )

        b = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="p0aa6_2"
        )

        if b == "نعم":
            finish(
                "مسار فحص البيئة/التوصيلات",
                "افحص آثار الرطوبة أو الضرر الخارجي بواسطة فني مؤهل "
                "واتبع مخطط BYD للموديل."
            )
            return

        step(
            3,
            "هل يعود P0AA6 مباشرة بعد مسحه؟",
            "Does P0AA6 return immediately after clearing?"
        )

        c = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="p0aa6_3"
        )

        if c == "نعم":
            finish(
                "العطل مستمر",
                "وجود العطل مباشرة بعد المسح يشير إلى أن المشكلة ما زالت موجودة. "
                "يلزم اختبار العزل حسب إجراء المصنع."
            )
        else:
            finish(
                "العطل متقطع",
                "راقب عودة الكود وسجّل ظروف ظهوره. "
                "لا تعتبر اختفاء الكود دليلاً على انتهاء المشكلة."
            )

        return


    # ───────────────────────────────────────────
    # U0298
    # ───────────────────────────────────────────

    if code == "U0298":

        st.subheader("U0298 — Lost Communication With DC/DC Converter")

        step(
            1,
            "هل توجد أكواد U أو أكواد مرتبطة بـ 12V؟",
            "Are there additional communication or 12V-related DTCs?"
        )

        a = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="u0298_1"
        )

        if a == "نعم":
            finish(
                "ابدأ بالأكواد المصاحبة",
                "وجود أكواد اتصال أو تغذية إضافية قد يغيّر مسار التشخيص."
            )
            return

        step(
            2,
            "هل جهد بطارية 12V ضمن المجال الطبيعي حسب مواصفات السيارة؟",
            "Is the 12V battery voltage within specification?"
        )

        b = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="u0298_2"
        )

        if b == "لا":
            finish(
                "ابدأ بمنظومة 12V",
                "يجب معالجة مشكلة بطارية 12V أو تغذيتها أولاً، "
                "ثم إعادة فحص الأكواد."
            )
            return

        step(
            3,
            "هل يوجد فقدان تغذية أو فيوز مرتبط بالـ DC/DC؟",
            "Is there a power supply or fuse issue related to the DC/DC system?"
        )

        c = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="u0298_3"
        )

        if c == "نعم":
            finish(
                "افحص دائرة التغذية",
                "شخّص دائرة التغذية والفيوز حسب مخطط السيارة."
            )
            return

        step(
            4,
            "هل الاتصال مع وحدة DC/DC مفقود بينما التغذية سليمة؟",
            "Is communication with the DC/DC unit lost while power is present?"
        )

        d = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key="u0298_4"
        )

        if d == "نعم":
            finish(
                "مسار الاتصال",
                "انتقل إلى فحص CAN والتوصيلات الخاصة بالوحدة "
                "وفق مخطط BYD."
            )
        else:
            finish(
                "يلزم تشخيص أعمق",
                "افحص الأكواد الحالية وبيانات Live Data ومخطط النظام "
                "قبل استبدال أي قطعة."
            )

        return


    # ───────────────────────────────────────────
    # P0100 / P0101 / P0102 / P0103
    # ───────────────────────────────────────────

    if code in ["P0100", "P0101", "P0102", "P0103"]:

        st.subheader(f"{code} — MAF Sensor")

        step(
            1,
            "هل توجد أكواد أخرى مرتبطة بالمحرك أو الحساسات؟",
            "Are there additional engine or sensor-related DTCs?"
        )

        a = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key=f"{code}_1"
        )

        if a == "نعم":
            finish(
                "افحص الأكواد المصاحبة أولاً",
                "الأكواد المصاحبة قد تكون سبباً أو نتيجة للكود الحالي."
            )
            return

        step(
            2,
            "هل فيشة حساس MAF متصلة وسليمة بصرياً؟",
            "Is the MAF connector physically connected and undamaged?"
        )

        b = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key=f"{code}_2"
        )

        if b == "لا":
            finish(
                "ابدأ بالتوصيل",
                "أصلح مشكلة التوصيل ثم أعد الفحص."
            )
            return

        step(
            3,
            "هل قيمة MAF في Live Data منطقية مقارنة بحالة المحرك؟",
            "Is the MAF Live Data plausible for the current engine state?"
        )

        c = st.radio(
            "النتيجة:",
            ["نعم", "لا", "غير متأكد"],
            key=f"{code}_3"
        )

        if c == "لا":
            finish(
                "مسار حساس MAF",
                "افحص التغذية والأرضي والإشارة والأسلاك حسب مخطط السيارة "
                "قبل استبدال الحساس."
            )
        elif c == "نعم":
            finish(
                "ابحث عن سبب آخر",
                "إذا كانت قراءة MAF منطقية، فلا تستبدل الحساس لمجرد وجود الكود."
            )
        else:
            finish(
                "نحتاج Live Data",
                "افتح بيانات Live Data وسجّل قراءة MAF ثم قارنها بمواصفات BYD."
            )

        return


    # ───────────────────────────────────────────
    # أكواد الاتصال U
    # ───────────────────────────────────────────

    if code.startswith("U"):

        st.subheader(f"{code} — Communication Fault")

        step(
            1,
            "هل توجد أكواد U أخرى في نفس الفحص؟",
            "Are there other communication DTCs?"
        )

        a = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key=f"{code}_1"
        )

        if a == "نعم":
            finish(
                "افحص شبكة الاتصال أولاً",
                "وجود عدة وحدات تفقد الاتصال قد يشير إلى مشكلة مشتركة "
                "في التغذية أو شبكة الاتصال."
            )
            return

        step(
            2,
            "هل الوحدة المتأثرة تعمل ولديها تغذية كهربائية صحيحة؟",
            "Does the affected module have proper power and ground?"
        )

        b = st.radio(
            "النتيجة:",
            ["نعم", "لا", "غير متأكد"],
            key=f"{code}_2"
        )

        if b == "لا":
            finish(
                "مسار التغذية",
                "ابدأ بفحص التغذية والأرضي والفيوزات حسب مخطط المصنع."
            )
            return

        if b == "غير متأكد":
            finish(
                "تحقق من التغذية",
                "لا تنتقل إلى استبدال الوحدة قبل التأكد من Power/Ground."
            )
            return

        step(
            3,
            "هل الاتصال مع الوحدة يعود ويختفي؟",
            "Is communication intermittent?"
        )

        c = st.radio(
            "النتيجة:",
            ["نعم", "لا"],
            key=f"{code}_3"
        )

        if c == "نعم":
            finish(
                "مسار اتصال متقطع",
                "افحص التوصيلات والأسلاك وشبكة CAN حسب مخطط السيارة."
            )
        else:
            finish(
                "مسار فقدان اتصال ثابت",
                "انتقل إلى فحص CAN والتغذية والوحدة نفسها وفق إجراء BYD."
            )

        return


    # ───────────────────────────────────────────
    # بقية الأكواد
    # ───────────────────────────────────────────

    step(
        1,
        "هل يوجد كود مصاحب لنفس النظام؟",
        "Is there another DTC related to the same system?"
    )

    a = st.radio(
        "النتيجة:",
        ["نعم", "لا"],
        key=f"{code}_generic_1"
    )

    if a == "نعم":
        finish(
            "ابدأ بالكود المصاحب",
            "الكود المصاحب قد يحدد الجزء المسؤول بشكل أدق."
        )
        return

    step(
        2,
        "هل المشكلة ظاهرة حالياً أم أن الكود تاريخي فقط؟",
        "Is the fault currently present or only stored/history?"
    )

    b = st.radio(
        "النتيجة:",
        ["ظاهرة حالياً", "تاريخية فقط"],
        key=f"{code}_generic_2"
    )

    if b == "تاريخية فقط":
        finish(
            "راقب العطل",
            "امسح الكود فقط وفق الإجراء المناسب ثم راقب عودته."
        )
        return

    step(
        3,
        "هل التوصيلات والفيوزات المرتبطة بالنظام سليمة؟",
        "Are the related connectors and fuses OK?"
    )

    c = st.radio(
        "النتيجة:",
        ["نعم", "لا"],
        key=f"{code}_generic_3"
    )

    if c == "لا":
        finish(
            "ابدأ بالتوصيلات والتغذية",
            "أصلح المشكلة ثم أعد الفحص قبل استبدال أي مكون."
        )
    else:
        finish(
            "انتقل إلى الاختبار المتخصص",
            "استخدم Live Data أو اختبار الوحدة أو مخطط المصنع "
            "بحسب نوع الكود."
        )


# ═══════════════════════════════════════════════
# قاعدة الأكواد
# ═══════════════════════════════════════════════

codes = {
    "P0AA6": "HV Isolation Fault",
    "U0298": "Lost Communication With DC/DC Converter",
    "P0100": "MAF Circuit",
    "P0101": "MAF Performance",
    "P0102": "MAF Low Input",
    "P0103": "MAF High Input",
    "U0100": "Lost Communication With ECM",
    "U0101": "Lost Communication With TCM",
    "U0110": "Lost Communication With Drive Motor",
    "U0111": "Lost Communication With BMS",
    "U0121": "Lost Communication With ABS",
    "U0140": "Lost Communication With BCM",
    "C1201": "ABS / Stability Control",
    "C1241": "ABS Low Voltage",
    "B1000": "Airbag ECU Fault",
    "B1211": "Seat Belt Circuit",
    "B2799": "Immobilizer System"
}


# ═══════════════════════════════════════════════
# اختيار الكود
# ═══════════════════════════════════════════════

st.header("🔎 تشخيص العطل")

search = st.text_input(
    "اكتب كود العطل:",
    placeholder="مثال: P0AA6"
).strip().upper()

if search:

    if search in codes:
        st.markdown("---")
        diagnose(search)
    else:
        st.warning(
            f"الكود {search} غير موجود حالياً في قاعدة البيانات."
        )
        st.info(
            "يمكن إضافة مسار تشخيص مستقل لهذا الكود داخل diagnose()."
        )

else:
    st.info("👆 اكتب كود DTC للبدء بالتشخيص التفاعلي.")


# ═══════════════════════════════════════════════
# حاسبة المسافة
# ═══════════════════════════════════════════════

with st.expander("📊 حاسبة التوفير"):

    col1, col2 = st.columns(2)

    with col1:
        prev = st.number_input(
            "العداد السابق",
            value=10000,
            step=100
        )

    with col2:
        curr = st.number_input(
            "العداد الحالي",
            value=11500,
            step=100
        )

    if curr > prev:
        km = curr - prev
        gasoline = (km / 10) * 1000
        ev = (km / 6) * 50
        saving = gasoline - ev

        st.success(
            f"💰 التوفير: {int(saving):,} د.ع لمسافة {km:,} كم"
        )


st.markdown("---")
st.caption("BYD Iraq Team ❤️ | Interactive Workshop")
