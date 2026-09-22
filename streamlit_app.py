import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="BYD Iraq Team - الورشة الذكية",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 الورشة الذكية لفريق BYD العراق")
st.caption("النسخة الميدانية التفاعلية المخصصة لكل عطل")

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

# --- 3. قاعدة بيانات الأشجار التشخيصية المخصصة كلياً لكل كود ---

def get_code_diagnostic_tree(code_key):
    """
    تسترجع هذه الدالة شجرة القرارات الخاصة بكل كود بدقة بدلاً من استخدام دالة عامة مكررة.
    """
    trees = {
        "P0AA6": {
            "title": "P0AA6 - تسريب فولتية عالية في الهيكل",
            "danger": "🚨 تحذير أمان: هذا العطل يتعلق بتسرب كهرباء الضغط العالي. لا تلمس الأسلاك البرتقالية بدون عزل!",
            "steps": {
                "start": {
                    "q": "الخطوة 1: قم بفصل مقبس الأمان البرتقالي خلف صندوق الأمتعة وانتظر 5 دقائق. هل تم فصل التيار؟",
                    "options": {
                        "نعم، تم الفصل والتفريغ": "step_2",
                        "لا، يوجد مشكلة في المقبس": "err_plug"
                    }
                },
                "step_2": {
                    "q": "الخطوة 2: افحص فيش الكمبريسور والكيبلات البرتقالية تحت السيارة بمصباح. ماذا وجدت؟",
                    "options": {
                        "توجد رطوبة أو ماء داخل الفيشة": "fix_wet",
                        "يوجد جرح/احتكاك بالسلك مع الشاصي": "fix_wire",
                        "الكيبلات جافة وسليمة تماماً": "step_3"
                    }
                },
                "step_3": {
                    "q": "الخطوة 3: قس مقاومة العزل للمكونات بالملتيميتر. ما هي القراءة؟",
                    "options": {
                        "المقاومة سليمة وطبيعية": "fix_clear",
                        "المقاومة منخفضة (تسريب داخلي)": "fix_internal"
                    }
                }
            },
            "outcomes": {
                "err_plug": "⚠️ تأكد من سحب عتلة الأمان للأمام أولاً ثم رفع الذراع للأعلى لتفادي كسر القفل.",
                "fix_wet": "🛠️ الحل: نظف الفيشة بماء مقطر ثم جففها تماماً ببخاخ تنظيف الإلكترونيات.",
                "fix_wire": "🛠️ الحل: اعزل الجزء المجروح بشريط عازل حراري مخصص للضغط العالي.",
                "fix_internal": "🚨 العطل داخلي في الإنفرتر أو بطارية الضغط العالي نفسها، يتطلب فحص الخلايا.",
                "fix_clear": "✅ تم التأكد من سلامة العزل! قم بإعادة المقبس ومسح الكود باستخدام جهاز OBD2."
            },
            "video": "https://www.youtube.com/watch?v=0h94Lh1a6_s"
        },
        
        "P0100": {
            "title": "P0100 - حساس تدفق الهواء الرئيسي MAF",
            "danger": "ℹ️ هذا العطل يتسبب في خنقة المحرك، زيادة استهلاك البنزين، أو ضعف التسارع.",
            "steps": {
                "start": {
                    "q": "الخطوة 1: افحص الفيشة الموصلة بحساس تدفق الهواء على مجرى الفلتر. ما هي حالتها؟",
                    "options": {
                        "توجد أتربة كثيفة أو الفيشة مرخية": "fix_clean_plug",
                        "توجد أسلاك مقطوعة ظاهرياً": "fix_harness",
                        "الفيشة نظيفة ومربوطة بإحكام": "step_2"
                    }
                },
                "step_2": {
                    "q": "الخطوة 2: افحص سلك وشبكة الحساس الداخلية بعد فكه. ماذا تلاحظ؟",
                    "options": {
                        "يوجد غبار أو زيوت متراكمة على السلك الداخلي": "fix_maf_clean",
                        "السلك الداخلي متقطع أو تالف": "fix_replace_maf"
                    }
                }
            },
            "outcomes": {
                "fix_clean_plug": "🛠️ الحل: رش بخاخ تنظيف الإلكترونيات داخل الفيشة وأعد تثبيتها جيداً.",
                "fix_harness": "🛠️ الحل: أصلح السلك المقطوع واعزله بشريط عازل لمنع التماس.",
                "fix_maf_clean": "🛠️ الحل: استخدم بخاخ تنظيف حساس الهواء المخصص (MAF Cleaner) ولا تلمس السلك بيدك.",
                "fix_replace_maf": "⚠️ الحساس تالف داخلياً ويحتاج إلى استبدال بقطعة جديدة أصلية."
            },
            "video": "https://www.youtube.com/results?search_query=BYD+P0100+MAF+Sensor"
        },

        "P0301": {
            "title": "P0301 - تفتفة واضحة في السلندر رقم 1",
            "danger": "⚠️ هذا العطل يسبب اهتزازاً واضحاً في المحرك وتأخيراً عند الدوس على البنزين.",
            "steps": {
                "start": {
                    "q": "الخطوة 1: قم ببدل كويل السلندر 1 مع كويل السلندر 2 وافحص بـ OBD2. هل انتقلت التفتفة للسلندر 2؟",
                    "options": {
                        "نعم، انتقل العطل إلى السلندر 2": "fix_coil",
                        "لا، بقيت التفتفة في السلندر 1": "step_2"
                    }
                },
                "step_2": {
                    "q": "الخطوة 2: افتح بلك (شمعة احتراق) السلندر 1 وافحصه. ما هي حالته؟",
                    "options": {
                        "البلك متآكل أو عليه آثار زيت وقاطر": "fix_spark",
                        "البلك بحالة ممتازة": "fix_injector"
                    }
                }
            },
            "outcomes": {
                "fix_coil": "🛠️ الحل: الكويل الخاص بالسلندر 1 تالف ويجب استبداله بكويل جديد.",
                "fix_spark": "🛠️ الحل: استبدل طقم البلكات (شمعات الاحتراق) بقطعة مطابقة.",
                "fix_injector": "⚠️ افحص نوزل (بخاخ) البنزين الخاص بالسلندر 1 أو افحص ضغط السلندر في الورشة."
            },
            "video": "https://www.youtube.com/results?search_query=BYD+P0301+misfire"
        },

        "C1241": {
            "title": "C1241 - جهد التغذية الكهربائية لوحدة ABS منخفض",
            "danger": "⚠️ هذا العطل يسبب توقف نظام منع انغلاق الفرامل وثبات السيارة.",
            "steps": {
                "start": {
                    "q": "الخطوة 1: قس الفولتية الواصلة لأصابع بطارية 12V والسيارة مطفأة. كم القراءة؟",
                    "options": {
                        "أقل من 11.8 فولت": "fix_battery",
                        "أعلى من 12.2 فولت": "step_2"
                    }
                },
                "step_2": {
                    "q": "الخطوة 2: افحص فيوز الـ ABS الرئيسي في علبة الفيوزات المجاورة للمحرك. ما هي حالته؟",
                    "options": {
                        "الفيوز محترق أو به كلس": "fix_abs_fuse",
                        "الفيوز سليم تماماً": "fix_abs_harness"
                    }
                }
            },
            "outcomes": {
                "fix_battery": "🛠️ الحل: شحن بطارية الـ 12V الصغيرة أو استبدالها إذا كانت لا تحتفظ بالشحن.",
                "fix_abs_fuse": "🛠️ الحل: استبدل فيوز الـ ABS بنفس القيمة المحددة (غالباً 30A أو 40A).",
                "fix_abs_harness": "🛠️ الحل: افصل الفيشة الرئيسية لكمبيوتر الـ ABS ونظف أسنانها بخاخ إلكترونيات ثم أعد مسح الكود."
            },
            "video": "https://www.youtube.com/results?search_query=BYD+C1241+ABS"
        },

        "U0100": {
            "title": "U0100 - انقطاع الاتصال مع عقل المحرك الرئيسي ECM",
            "danger": "⚠️ عطل في شبكة الاتصال يمنع تشغيل المحرك أو استجابة دواسة البنزين.",
            "steps": {
                "start": {
                    "q": "الخطوة 1: افحص فيشة عقل المحرك الرئيسي (ECM). هل هي مكبوسة بإحكام ومقفولة؟",
                    "options": {
                        "الفيشة مرخية أو بها رطوبة": "fix_ecm_plug",
                        "الفيشة مثبتة ومقفولة تماماً": "step_2"
                    }
                },
                "step_2": {
                    "q": "الخطوة 2: افحص الفيوز الرئيسي للـ ECM وخط التغذية (Main Relay). ماذا تلاحظ؟",
                    "options": {
                        "الفيوز أو المرحل (الكتوت) تالف": "fix_relay",
                        "جميع الفيوزات والمرحلات سليمة": "fix_can_bus"
                    }
                }
            },
            "outcomes": {
                "fix_ecm_plug": "🛠️ الحل: نظف فيشة العقل ببخاخ إلكترونيات واكبس قفل الفيشة بإحكام.",
                "fix_relay": "🛠️ الحل: استبدل المرحل الرئيسي (Main Relay) أو الفيوز التالف بآخر جديد.",
                "fix_can_bus": "⚠️ يوجد انقطاع في أسلاك شبكة الـ CAN-Bus الموصلة بين العقول، افحص المقاومة (يجب أن تكون 60 أوم)."
            },
            "video": "https://www.youtube.com/results?search_query=BYD+U0100+ECM+Communication"
        }
    }
    
    # في حال اختيار كود آخر غير المعرفة أعلاه، تظهر شجرة قياسية عامة للحساسات بدون استخدام البطارية كمرجع أساسي
    default_tree = {
        "title": f"{code_key} - دليل فحص وتشخيص العطل الميداني",
        "danger": "ℹ️ اتبع الخطوات الميدانية المحددة لهذا الحساس لمعرفة السبب مباشرة.",
        "steps": {
            "start": {
                "q": f"الخطوة 1: افحص الفيشة الخاصة بـ ({code_key}). ماذا تلاحظ؟",
                "options": {
                    "توجد أتربة، كلس، أو الفيشة غير مثبتة": "fix_def_plug",
                    "الفيشة نظيفة ومربوطة بشكل ممتاز": "step_2"
                }
            },
            "step_2": {
                "q": "الخطوة 2: افحص التغذية الكهربائية وسلك التأريض (الأرضي) للقطعة. ما هي النتيجة؟",
                "options": {
                    "لا تصل كهرباء للقطعة (0 فولت)": "fix_def_fuse",
                    "التغذية الكهربائية واصلة بشكل سليم": "fix_def_sensor"
                }
            }
        },
        "outcomes": {
            "fix_def_plug": "🛠️ الحل: رش بخاخ تنظيف الإلكترونيات داخل الفيشة وأعد تركيبها بإحكام.",
            "fix_def_fuse": "🛠️ الحل: تتبع علبة الفيوزات المخصصة لهذه الدائرة واستبدل الفيوز التالف.",
            "fix_def_sensor": "⚠️ التغذية والأسلاك سليمة، العطل في الحساس/القطعة نفسها وتحتاج استبدال ثم مسح الكود."
        },
        "video": f"https://www.youtube.com/results?search_query=BYD+{code_key}+repair"
    }
    
    return trees.get(code_key, default_tree)

# --- 4. قوائم البحث واختيار الكود ---

st.header("🔧 الموسوعة الميدانية التشخيصية للأعطال")

available_codes = ["P0AA6", "P0100", "P0301", "C1241", "U0100", "TPMS", "P0101", "P0120", "P0420", "C1300", "B1000"]

selected_code = st.selectbox("📌 اختر الكود المراد تشخيصه ميدانياً:", ["اختر كود من القائمة..."] + available_codes)

# --- 5. تشغيل الشجرة التفاعلية بدون تداخل ---

if selected_code != "اختر كود من القائمة...":
    code_data = get_code_diagnostic_tree(selected_code)
    
    st.markdown("---")
    st.subheader(code_data["title"])
    st.error(code_data["danger"])
    
    st.markdown("### 🛠️ شجرة التشخيص الميدانية:")

    # تهيئة مفتاح الحالة لضمان التغيير عند اختيار كود جديد
    if "tree_node" not in st.session_state or st.session_state.get("active_code_key") != selected_code:
        st.session_state.tree_node = "start"
        st.session_state.active_code_key = selected_code

    current_node = st.session_state.tree_node

    # إذا كنا داخل مرحلة من مراحل الأسئلة
    if current_node in code_data["steps"]:
        node_info = code_data["steps"][current_node]
        
        st.info(f"**{node_info['q']}**")
        
        user_choice = st.radio("اختر القراءة أو نتيجة الفحص الميداني:", list(node_info["options"].keys()))
        
        if st.button("تأكيد النتيجة والانتقال للخطوة التالية 🔗"):
            st.session_state.tree_node = node_info["options"][user_choice]
            st.rerun()

    # إذا وصلنا للنتيجة والحل (Outcome)
    elif current_node in code_data["outcomes"]:
        outcome_text = code_data["outcomes"][current_node]
        
        if "✅" in outcome_text:
            st.success(outcome_text)
            st.balloons()
        elif "🛠️" in outcome_text:
            st.warning(outcome_text)
        else:
            st.error(outcome_text)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 إعادة تشخيص هذا الكود من البداية"):
            st.session_state.tree_node = "start"
            st.rerun()

    # عرض الفيديو التوضيحي
    if code_data.get("video"):
        st.markdown("---")
        st.write("🎥 **فيديو توضيحي تفصيلي للمساعدة:**")
        st.markdown(f"[▶️ اضغط هنا لمشاهدة فيديو الصيانة الخاص بـ {selected_code} على يوتيوب]({code_data['video']})")

st.markdown("---")
st.caption("إهداء خاص إلى قائد وأعضاء فريق BYD العراق ❤️ - صُمم ليكون دليلك الميداني الأول")
