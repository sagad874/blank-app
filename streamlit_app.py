import streamlit as st

# إعدادات الصفحة مع فرض اتجاه النص العربي (RTL)
st.set_page_config(page_title="BYD Iraq Team - الورشة الذكية", page_icon="🚗", layout="centered")

st.markdown("""
<style>
    body, .stApp {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚗 الورشة الذكية لفريق BYD العراق")
st.write("النسخة الميدانية التفاعلية المتقدمة | التشخيص التفرعي الذكي خطوة بخطوة")

st.markdown("---")

# --- 1. خريطة ورشة العمل الميدانية للمبتدئين ---
with st.expander("🛠️ دليل العدة المطلوبة وأماكن القطع الأساسية في سيارات BYD"):
    st.markdown("""
    قبل أن تبدأ بأي عطل، تأكد من توفر هذه العدة البسيطة بجانبك في الكراج:
    - **مفكات براغي (سحب وعادي)** ومفتاح ربط (تثبيت) قياس 10 ملم.
    - **جهاز متعدد القياس (Multimeter)** لفحص الفولتية بدقة.
    - **بخاخ تنظيف إلكترونيات (Contact Cleaner)** لتنظيف الفيش من الرطوبة والكلس.
    - **جهاز فحص OBD2 بلوتوث** لمسح الأخطاء بعد التصليح.
    """)

st.markdown("---")

# --- 2. حاسبة التوفير ---
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

# --- 3. الدليل الميداني التفاعلي المتفرع ---
st.header("🔧 التشخيص التفاعلي الذكي (الفحص المتفرع)")

def build_interactive_guide(code, title_desc):
    category = code[0]
    type_explanations = {
        "P": "منظومة الحركة، المحرك، البنزين، أو البطارية والإنفرتر.",
        "U": "شبكة الاتصالات الرقمية (CAN-Bus).",
        "C": "أنظمة الثبات، الفرامل (ABS)، وتوجيه المقود.",
        "B": "المقصورة الداخلية، الوسائد الهوائية، والتكييف."
    }
    general_desc = type_explanations.get(category, "الحساسات الإلكترونية المسؤولة عن أداء السيارة.")

    return {
        "title": f"{code} - {title_desc}",
        "danger": f"ℹ️ طبيعة النظام: {general_desc} اتبع خطوات الفحص أدناه:",
        "step1": "الفحص الميداني الظاهري: ارفع الغطاء أو افحص تحت السيارة. هل لاحظت أي سلك مجروح، فيشة مهتزة، أو فيوز تالف؟",
        "step2": "فحص فولتية البطارية (12V) بجهاز القياس وهي مطفأة. هل القراءة أقل من 12.2 فولت (مثل 11V)؟",
        "step3": "تنظيف فيشة الحساس المتضرر: هل ما زال الكود ظاهراً بعد تنظيف الفيشة وإزالة الأتربة والرطوبة منها؟",
        "step4": "المسح التجريبي: اربط جهاز الفحص (OBD2) ومسح الرمز، ثم قد السيارة لمسافة قصيرة. هل عاد الكود للظهور مجدداً؟"
    }

# عينة موسعة من الأكواد
raw_codes_list = [
    ("TPMS", "تنبيه ضغط الهواء في الإطارات"),
    ("P0100", "حساس تدفق الهواء الرئيسي MAF Sensor"),
    ("P0115", "حساس حرارة مياه التبريد للمحرك ECT"),
    ("P0300", "تفتفة عشوائية في أسطوانات المحرك"),
    ("U0100", "انقطاع الاتصال مع عقل المحرك الرئيسي ECM"),
    ("C1241", "جهد التغذية الكهربائية لوحدة الـ ABS منخفض جداً")
]

for i in range(1, 20):
    extra_code = f"P0{200+i:03d}"
    raw_codes_list.append((extra_code, f"Diagnostic Code {extra_code} System Circuit Performance"))

workshop_db = {"اختر كود من القائمة...": None}
for code_key, name_key in raw_codes_list:
    workshop_db[f"{code_key} - {name_key}"] = build_interactive_guide(code_key, name_key)

selected_code = st.selectbox("📌 اختر كود العطل من القائمة:", list(workshop_db.keys()))

if selected_code and selected_code != "اختر كود من القائمة...":
    data = workshop_db[selected_code]
    
    st.subheader(data["title"])
    st.error(data["danger"])
    st.markdown("---")
    
    # --- الخطوة 1 ---
    st.markdown(f"""
    <div style="background-color: #0e2a1b; border-right: 5px solid #28a745; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #ffffff;">
        <strong>الخطوة 1:</strong><br>{data['step1']}
    </div>
    """, unsafe_allow_html=True)
    
    ans1 = st.radio("هل وجدت تلفاً ظاهرياً أو فيوزاً محترقاً في الخطوة 1؟", ["لا، كل شيء سليم", "نعم، وجدْتُ تلفاً/فيوزاً تالفاً"], key="ans1")
    
    if ans1 == "نعم، وجدْتُ تلفاً/فيوزاً تالفاً":
        st.warning("🛑 **النتيجة والتصليح الجذري:** استبدل الفيوز التالف أو أصلح السلك المجروح فوراً، ثم امسح الكود بجهاز الفحص. لا داعي لإكمال باقي الخطوات!")
    else:
        st.success("✅ ممتاز، التوصيلات سليمة. ننتقل للخطوة التالية...")
        st.markdown("---")
        
        # --- الخطوة 2 ---
        st.markdown(f"""
        <div style="background-color: #0e2a1b; border-right: 5px solid #28a745; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #ffffff;">
            <strong>الخطوة 2:</strong><br>{data['step2']}
        </div>
        """, unsafe_allow_html=True)
        
        ans2 = st.radio("ما هي قراءة الفولتية للبطارية؟", ["طبيعية (12.6 فولت أو أكثر)", "ضعيفة (11 فولت أو أقل / تحتاج شحن أو تبديل)"], key="ans2")
        
        if ans2 == "ضعيفة (11 فولت أو أقل / تحتاج شحن أو تبديل)":
            st.error("🚨 **التشخيص النهائي والحل:** قراءة ال11 فولت هي **السبب الجذري للمشكلة!** ضعف البطارية يولد أكواد وهمية كثيرة. قم بشحن البطارية أو استبدالها بأخرى جديدة فوراً، وسيختفي العطل نهائياً بدون إكمال الخطوات.")
        else:
            st.success("✅ الفولتية سليمة ومستقرة. ننتقل للخطوة التالية...")
            st.markdown("---")
            
            # --- الخطوة 3 ---
            st.markdown(f"""
            <div style="background-color: #0e2a1b; border-right: 5px solid #28a745; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #ffffff;">
                <strong>الخطوة 3:</strong><br>{data['step3']}
            </div>
            """, unsafe_allow_html=True)
            
            ans3 = st.radio("هل اختفى العطل أو تغير بعد تنظيف الفيشة؟", ["نعم، اختفى المشكلة", "لا، ما زال الكود ظاهراً"], key="ans3")
            
            if ans3 == "نعم، اختفى المشكلة":
                st.success("🎉 **تم الإصلاح بنجاح!** المشكلة كانت مجرد رطوبة أو كلس داخل الفيشة وتمت معالجتها.")
            else:
                st.markdown("---")
                # --- الخطوة 4 ---
                st.markdown(f"""
                <div style="background-color: #0e2a1b; border-right: 5px solid #28a745; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #ffffff;">
                    <strong>الخطوة 4:</strong><br>{data['step4']}
                </div>
                """, unsafe_allow_html=True)
                
                ans4 = st.radio("هل عاد الكود للظهور بعد المسح والقيادة القصيرة؟", ["لا، لم يعد (انتهت المشكلة)", "نعم، عاد للظهور (الحساس نفسه تالف)"], key="ans4")
                
                if ans4 == "نعم، عاد للظهور (الحساس نفسه تالف)":
                    st.error("🛠️ **التشخيص النهائي:** طالما أن التوصيلات سليمة والبطارية قوية ورغم ذلك عاد الكود، فهذا يثبت أن **الحساس تالف ميكانيكياً/إلكترونياً** ويجب استبداله بقطعة أصلية جديدة.")
                else:
                    st.success("🎉 مبروك! تم التخلص من العطل نهائياً.")

st.markdown("---")
st.caption("إهداء خاص إلى قائد وأعضاء فريق BYD العراق ❤️ - صُمم ليكون دليلك التفاعلي الذكي في الكراج")
