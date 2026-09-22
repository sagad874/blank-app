import streamlit as st

# =========================================================
# BYD IRAQ SMART WORKSHOP V2
# Interactive Diagnostic Decision Tree
# =========================================================

st.set_page_config(
    page_title="BYD Iraq Team - الورشة الذكية",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.block-container {
    max-width: 1000px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* RTL */
.main-title {
    direction: rtl;
    text-align: center;
    font-size: 32px;
    font-weight: 800;
}

.subtitle {
    direction: rtl;
    text-align: center;
    opacity: 0.75;
    font-size: 16px;
    margin-bottom: 25px;
}

/* Step number is deliberately separated */
.step-number {
    direction: ltr;
    text-align: left;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 1px;
    opacity: 0.65;
    margin-bottom: 8px;
}

/* Arabic content */
.arabic-text {
    direction: rtl;
    text-align: right;
    font-size: 20px;
    line-height: 1.8;
    font-weight: 600;
}

/* English content */
.english-text {
    direction: ltr;
    text-align: left;
    font-size: 14px;
    opacity: 0.75;
    line-height: 1.5;
}

/* Code badge */
.code-badge {
    direction: ltr;
    text-align: center;
    font-family: monospace;
    font-size: 24px;
    font-weight: 800;
    padding: 12px;
    border-radius: 12px;
    background: rgba(100,100,100,0.15);
}

/* Result cards */
.result-good {
    direction: rtl;
    text-align: right;
    padding: 18px;
    border-radius: 12px;
    background: rgba(40, 180, 90, 0.15);
    border: 1px solid rgba(40, 180, 90, 0.35);
}

.result-warning {
    direction: rtl;
    text-align: right;
    padding: 18px;
    border-radius: 12px;
    background: rgba(240, 170, 30, 0.15);
    border: 1px solid rgba(240, 170, 30, 0.35);
}

.result-danger {
    direction: rtl;
    text-align: right;
    padding: 18px;
    border-radius: 12px;
    background: rgba(220, 60, 60, 0.15);
    border: 1px solid rgba(220, 60, 60, 0.35);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🚗 الورشة الذكية لفريق BYD العراق</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'نظام تشخيص تفاعلي — لا يعطيك الخطوة التالية إلا بعد تحديد نتيجة الفحص الحالية'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# =========================================================
# VEHICLE INFORMATION
# =========================================================

st.subheader("🚘 معلومات السيارة")

col1, col2 = st.columns(2)

with col1:
    powertrain = st.selectbox(
        "نوع منظومة السيارة",
        [
            "EV — كهربائية بالكامل",
            "DM-i / DM-p — هجينة",
            "ICE — محرك احتراق",
            "غير متأكد"
        ]
    )

with col2:
    model = st.text_input(
        "موديل BYD",
        placeholder="مثال: Atto 3 / Seal / Song Plus..."
    )

st.markdown("---")


# =========================================================
# DTC DATABASE
# =========================================================

CODES = {

    # ---------------- P CODES ----------------

    "P0100": {
        "title": "عطل دائرة حساس تدفق الهواء",
        "english": "Mass Air Flow Sensor Circuit",
        "system": "MAF",
        "risk": "MEDIUM",
        "powertrain": "ICE",
        "focus": "إشارة حساس تدفق الهواء",
    },

    "P0101": {
        "title": "أداء حساس تدفق الهواء خارج النطاق",
        "english": "Mass Air Flow Range / Performance",
        "system": "MAF",
        "risk": "MEDIUM",
        "powertrain": "ICE",
        "focus": "منطق قراءة MAF مقارنة بحالة المحرك",
    },

    "P0102": {
        "title": "إشارة حساس تدفق الهواء منخفضة",
        "english": "Mass Air Flow Circuit Low",
        "system": "MAF",
        "risk": "MEDIUM",
        "powertrain": "ICE",
        "focus": "انخفاض إشارة MAF",
    },

    "P0103": {
        "title": "إشارة حساس تدفق الهواء مرتفعة",
        "english": "Mass Air Flow Circuit High",
        "system": "MAF",
        "risk": "MEDIUM",
        "powertrain": "ICE",
        "focus": "ارتفاع إشارة MAF",
    },

    "P0110": {
        "title": "دائرة حساس حرارة هواء السحب",
        "english": "Intake Air Temperature Sensor Circuit",
        "system": "IAT",
        "risk": "MEDIUM",
        "powertrain": "ICE",
        "focus": "إشارة حرارة هواء السحب",
    },

    "P0115": {
        "title": "دائرة حساس حرارة سائل التبريد",
        "english": "Engine Coolant Temperature Sensor Circuit",
        "system": "ECT",
        "risk": "MEDIUM",
        "powertrain": "ICE",
        "focus": "إشارة حرارة سائل التبريد",
    },

    "P0120": {
        "title": "دائرة حساس وضع الخانق / دعسة التسارع",
        "english": "Throttle / Accelerator Position Sensor Circuit",
        "system": "TPS / APP",
        "risk": "HIGH",
        "powertrain": "ICE / Hybrid",
        "focus": "إشارة موضع الدعسة أو الخانق",
    },

    "P0130": {
        "title": "دائرة حساس الأكسجين",
        "english": "Oxygen Sensor Circuit",
        "system": "O2",
        "risk": "MEDIUM",
        "powertrain": "ICE / Hybrid",
        "focus": "إشارة حساس الأكسجين",
    },

    "P0300": {
        "title": "تفتفة عشوائية متعددة الأسطوانات",
        "english": "Random / Multiple Cylinder Misfire",
        "system": "Misfire",
        "risk": "HIGH",
        "powertrain": "ICE / Hybrid",
        "focus": "تحديد ما إذا كان التفتفة حقيقية وحالية",
    },

    "P0301": {
        "title": "تفتفة في الأسطوانة رقم 1",
        "english": "Cylinder 1 Misfire",
        "system": "Misfire",
        "risk": "HIGH",
        "powertrain": "ICE / Hybrid",
        "focus": "الأسطوانة 1",
    },

    "P0302": {
        "title": "تفتفة في الأسطوانة رقم 2",
        "english": "Cylinder 2 Misfire",
        "system": "Misfire",
        "risk": "HIGH",
        "powertrain": "ICE / Hybrid",
        "focus": "الأسطوانة 2",
    },

    "P0303": {
        "title": "تفتفة في الأسطوانة رقم 3",
        "english": "Cylinder 3 Misfire",
        "system": "Misfire",
        "risk": "HIGH",
        "powertrain": "ICE / Hybrid",
        "focus": "الأسطوانة 3",
    },

    "P0304": {
        "title": "تفتفة في الأسطوانة رقم 4",
        "english": "Cylinder 4 Misfire",
        "system": "Misfire",
        "risk": "HIGH",
        "powertrain": "ICE / Hybrid",
        "focus": "الأسطوانة 4",
    },

    "P0420": {
        "title": "كفاءة المحول الحفاز منخفضة",
        "english": "Catalyst System Efficiency Below Threshold",
        "system": "Catalyst",
        "risk": "MEDIUM",
        "powertrain": "ICE / Hybrid",
        "focus": "كفاءة المحول الحفاز",
    },

    "P0500": {
        "title": "إشارة سرعة السيارة غير متاحة",
        "english": "Vehicle Speed Sensor Malfunction",
        "system": "Vehicle Speed",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "مصدر سرعة السيارة",
    },

    "P0A1F": {
        "title": "عطل في وحدة التحكم بطاقة البطارية",
        "english": "Battery Energy Control Module",
        "system": "BMS",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid",
        "focus": "وحدة إدارة البطارية والاتصال معها",
    },

    "P0A78": {
        "title": "أداء دائرة إنفرتر محرك الدفع غير طبيعي",
        "english": "Drive Motor Inverter Performance",
        "system": "Inverter",
        "risk": "CRITICAL",
        "powertrain": "EV / Hybrid",
        "focus": "الإنفرتر ومحرك الدفع",
    },

    "P0A7F": {
        "title": "تدهور أداء بطارية الجهد العالي",
        "english": "High Voltage Battery Pack Deterioration",
        "system": "HV Battery",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid",
        "focus": "حالة بطارية الجهد العالي",
    },

    "P0A81": {
        "title": "دائرة مروحة تبريد بطارية الجهد العالي",
        "english": "Hybrid Battery Cooling Fan Circuit",
        "system": "Battery Cooling",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid",
        "focus": "تبريد البطارية",
    },

    "P0A9C": {
        "title": "حساس حرارة بطارية الجهد العالي",
        "english": "Hybrid Battery Temperature Sensor",
        "system": "HV Battery Temperature",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid",
        "focus": "قراءات حرارة البطارية",
    },

    "P0C73": {
        "title": "أداء مضخة تبريد الإنفرتر غير طبيعي",
        "english": "Inverter Cooling Pump Performance",
        "system": "Cooling",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid",
        "focus": "دورة تبريد الإنفرتر",
    },

    "P0D01": {
        "title": "فولتية إدخال شاحن السيارة منخفضة",
        "english": "On-Board Charger Input Voltage Low",
        "system": "OBC",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid",
        "focus": "دخل الشحن",
    },

    # ---------------- U CODES ----------------

    "U0100": {
        "title": "انقطاع الاتصال مع وحدة التحكم بالمحرك",
        "english": "Lost Communication With ECM / PCM",
        "system": "CAN",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "اتصال CAN مع وحدة التحكم",
    },

    "U0101": {
        "title": "انقطاع الاتصال مع وحدة ناقل الحركة",
        "english": "Lost Communication With Transmission Control Module",
        "system": "CAN",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "اتصال وحدة ناقل الحركة",
    },

    "U0110": {
        "title": "انقطاع الاتصال مع وحدة محرك الدفع",
        "english": "Lost Communication With Drive Motor Control Module",
        "system": "CAN",
        "risk": "CRITICAL",
        "powertrain": "EV / Hybrid",
        "focus": "اتصال وحدة محرك الدفع",
    },

    "U0111": {
        "title": "انقطاع الاتصال مع وحدة إدارة البطارية",
        "english": "Lost Communication With Battery Energy Control Module",
        "system": "CAN / BMS",
        "risk": "CRITICAL",
        "powertrain": "EV / Hybrid",
        "focus": "اتصال BMS",
    },

    "U0121": {
        "title": "انقطاع الاتصال مع وحدة ABS",
        "english": "Lost Communication With ABS Control Module",
        "system": "CAN / ABS",
        "risk": "CRITICAL",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "اتصال ABS",
    },

    "U0140": {
        "title": "انقطاع الاتصال مع وحدة التحكم بالهيكل",
        "english": "Lost Communication With Body Control Module",
        "system": "CAN / BCM",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "اتصال BCM",
    },

    "U0155": {
        "title": "انقطاع الاتصال مع لوحة العدادات",
        "english": "Lost Communication With Instrument Panel Cluster",
        "system": "CAN / Cluster",
        "risk": "MEDIUM",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "اتصال لوحة العدادات",
    },

    # ---------------- C CODES ----------------

    "C1201": {
        "title": "خلل في نظام التحكم المرتبط بالفرامل",
        "english": "ABS / Stability Control Related Fault",
        "system": "ABS / ESC",
        "risk": "CRITICAL",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "نظام ABS و ESC",
    },

    "C1241": {
        "title": "جهد تغذية وحدة ABS منخفض",
        "english": "Low Power Supply Voltage",
        "system": "ABS Power",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "تغذية وحدة ABS",
    },

    "C1300": {
        "title": "عطل داخلي في وحدة ABS",
        "english": "ABS ECU Internal Malfunction",
        "system": "ABS ECU",
        "risk": "CRITICAL",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "وحدة ABS",
    },

    "C1511": {
        "title": "عطل في حساس عزم المقود",
        "english": "Steering Torque Sensor",
        "system": "EPS",
        "risk": "CRITICAL",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "حساس عزم التوجيه",
    },

    # ---------------- B CODES ----------------

    "B1000": {
        "title": "عطل داخلي في وحدة الوسائد الهوائية",
        "english": "Airbag Control Module Internal Fault",
        "system": "SRS",
        "risk": "CRITICAL",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "SRS / Airbag",
    },

    "B1211": {
        "title": "دائرة شداد حزام الأمان مفتوحة",
        "english": "Seat Belt Pretensioner Circuit Open",
        "system": "SRS",
        "risk": "CRITICAL",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "شداد حزام الأمان",
    },

    "B2799": {
        "title": "خلل في نظام مانع السرقة",
        "english": "Immobilizer System Malfunction",
        "system": "Immobilizer",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid / ICE",
        "focus": "مانع السرقة / التعرف على المفتاح",
    },

    # ---------------- SPECIAL ----------------

    "P0AA6": {
        "title": "خلل عزل نظام الجهد العالي",
        "english": "Hybrid / EV Battery Voltage System Isolation Fault",
        "system": "HV Isolation",
        "risk": "CRITICAL",
        "powertrain": "EV / Hybrid",
        "focus": "عزل دائرة الجهد العالي عن الهيكل",
    },

    "U0298": {
        "title": "انقطاع الاتصال مع محول DC-DC",
        "english": "Lost Communication With DC-DC Converter",
        "system": "DC-DC",
        "risk": "HIGH",
        "powertrain": "EV / Hybrid",
        "focus": "اتصال وتغذية محول DC-DC",
    },

}


# =========================================================
# DIAGNOSTIC FLOW ENGINE
# =========================================================

def node(
    question_ar,
    question_en,
    options
):
    return {
        "question_ar": question_ar,
        "question_en": question_en,
        "options": options
    }


def option(
    label_ar,
    label_en,
    next_step=None,
    result=None,
    severity="normal"
):
    return {
        "label_ar": label_ar,
        "label_en": label_en,
        "next": next_step,
        "result": result,
        "severity": severity
    }


# =========================================================
# SPECIAL FLOW: P0AA6
# =========================================================

def flow_p0aa6():

    return {

        "start": node(
            "هل الكود P0AA6 موجود حالياً كـ Active / Current وليس مجرد تاريخي؟",
            "Is P0AA6 currently Active / Current rather than History / Stored?",
            [
                option(
                    "نعم، Active / Current",
                    "YES — Active / Current",
                    "hv_water",
                    severity="danger"
                ),
                option(
                    "لا، History / Stored فقط",
                    "NO — History / Stored only",
                    "hv_history"
                ),
                option(
                    "لا أعرف",
                    "I DON'T KNOW",
                    "hv_confirm"
                )
            ]
        ),

        "hv_confirm": node(
            "أعد فحص السيارة بجهاز تشخيص يدعم وحدة HV/BMS واقرأ جميع الأكواد المرتبطة، وليس P0AA6 فقط
