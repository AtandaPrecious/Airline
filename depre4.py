# -*- coding: utf-8 -*-
"""
Student Mental Wellness App – Gentle, Supportive, and Clear UI
(uses existing trained model: Depression_predictor.pkl)
"""

import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Load Model (kept exactly as is)
# -----------------------------
model = joblib.load("Depression_predictor.pkl")

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Student Mental Wellness Sanctuary",
    page_icon="🌿",
    layout="wide"
)

# -----------------------------
# Custom CSS – Vibrant background with white text
# -----------------------------
st.markdown(
    """
<style>
:root {
  --bg: #00C4B4;        /* vibrant teal background to pop */
  --panel: #E6FFFA;     /* light mint for card contrast */
  --ink: #FFFFFF;       /* pure white for bright, readable text */
  --muted: #80E7D8;     /* soft cyan for helper text */
  --accent: #FF6F61;    /* vibrant coral for accents */
  --accent-dark: #E55A4F; /* darker coral for gradients */
  --success: #27AE60;   /* vivid green for positive feedback */
  --risk: #C0392B;     /* bright red for alerts */
}

/* page background and base text */
body {
  background: var(--bg);
  color: var(--ink);
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* card style */
.card {
  background: var(--panel);
  padding: 26px;
  border-radius: 18px;
  box-shadow: 0 8px 24px rgba(0, 196, 180, 0.15);
  margin-bottom: 22px;
  transition: transform .18s ease, box-shadow .18s ease;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 14px 36px rgba(0, 196, 180, 0.2); }

/* Buttons */
.stButton>button {
  background: linear-gradient(90deg, var(--accent), var(--accent-dark));
  color: #FFFFFF; /* bright white for button text */
  font-size: 16px;
  border-radius: 12px;
  padding: 10px 22px;
  border: none;
  box-shadow: 0 8px 20px rgba(255, 111, 97, 0.25);
  transition: transform .12s ease, box-shadow .12s ease;
}
.stButton>button:hover { transform: translateY(-3px); box-shadow: 0 14px 32px rgba(229, 90, 79, 0.3); }

/* Headings readability */
h1, h2, h3, h4, h5, h6 {
  color: var(--ink) !important;
  font-weight: 800;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3); /* stronger shadow for visibility */
}

/* helper & small note */
.helper { color: var(--muted); font-size: 13px; margin-top:6px; display:block; }
.small-note { color: var(--muted); font-size:13px; }

/* keep default nav hidden (Streamlit) */
#MainMenu, header, footer {visibility: hidden;}

/* moving footer */
.moving-footer {
  position: fixed; left: 0; right: 0; bottom: 0; z-index: 999;
  background: rgba(255, 111, 97, 0.15); /* coral-based footer background */
  padding: 10px 0; text-align: center;
  font-weight: 700; color: #FFFFFF; font-size: 15px; /* white footer text */
  backdrop-filter: blur(4px);
}
.moving-footer span { display:inline-block; white-space:nowrap; animation: moveText 18s linear infinite; }
@keyframes moveText { 0% {transform: translateX(100%);} 100% {transform: translateX(-100%);} }

/* ensure caption / small text contrast */
.stCaption, .stMarkdown p, .stText, .stWrite { color: var(--muted) !important; }

/* improve contrast inside card paragraphs */
.card p, .card div { color: var(--ink) !important; }

/* Health status indicators */
.health-green { color: var(--success); font-weight: 700; font-size: 18px; }
.health-red { color: var(--risk); font-weight: 700; font-size: 18px; }
</style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Session State
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "city" not in st.session_state:
    st.session_state.city = ""
if "name" not in st.session_state:
    st.session_state.name = ""
if "predicted" not in st.session_state:
    st.session_state.predicted = False
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

SAFE_NOTE = "Your information is safe and not recorded. This is a gentle guide — not a diagnosis."

# -----------------------------
# OPENING PAGE
# -----------------------------
if st.session_state.page == "welcome":
    st.markdown("<h1 style='text-align:center; color:#FFFFFF;'>🌿 Welcome to your mental wellness sanctuary.</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; font-size:18px; max-width:820px; margin: 8px auto; color:#FFFFFF;'>Let's begin your journey towards understanding and nurturing your mental health.</p>",
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0; color:#FFFFFF;'>Please enter your name and city below</h4>", unsafe_allow_html=True)
        name = st.text_input("Your name", "")
        city = st.text_input("Your city", "")
        st.caption("We use this to personalize your experience. " + SAFE_NOTE)
        
        c1, c2, c3 = st.columns([1,1,1])
        with c2:
            if st.button("Continue 🌱"):
                if name.strip() and city.strip():
                    st.session_state.name = name.strip()
                    st.session_state.city = city.strip()
                    st.session_state.page = "welcome_message"
                else:
                    st.warning("Please enter both your name and city to proceed.")
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# WELCOME MESSAGE PAGE
# -----------------------------
elif st.session_state.page == "welcome_message":
    n = st.session_state.name
    c = st.session_state.city
    st.markdown(f"<h2 style='text-align:center; color:#FFFFFF;'>Hi {n} from {c} 🌿</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='max-width:900px; margin:18px auto 0 auto; color:#FFFFFF; font-size:18px; text-align:center;'>
        <p>Welcome to a space of care and clarity. This is a gentle place created for students like you — a quiet moment to pause, reflect, and explore your mental well-being with compassion.</p>
        <p>Life as a student can be overwhelming, and sometimes the weight we carry isn’t easy to name. This tool is here to help you notice, understand, and gently assess whether certain patterns in your lifestyle may be placing you at risk of depression. <strong>It’s not a diagnosis — it’s a guide.</strong> A soft nudge toward awareness, support, and healing.</p>
        <p>Whatever the result, know this: <strong>You are not alone. You are not broken. You are deeply valued.</strong> Let this be a step toward kindness — the kind you offer yourself.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='text-align:center; margin-top:28px;'>", unsafe_allow_html=True)
    back, go = st.columns([1,1])
    with back:
        if st.button("⬅️ Back"):
            st.session_state.page = "welcome"
    with go:
        if st.button("Click here to go ahead with analysis ✨"):
            st.session_state.page = "details"
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# DETAILS PAGE (sliders fixed with guidance BEFORE input)
# -----------------------------
elif st.session_state.page == "details":
    n = st.session_state.name
    st.markdown("<h1 style='text-align:center; color:#FFFFFF;'>🌿 Your Details</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:16px; color:#80E7D8;'>Hi {n}, I’m glad you decided to do this. Please fill in correct information below. <br><em>{SAFE_NOTE}</em></p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.slider("Age", 15, 40, 20)

        st.subheader("Academic Pressure")
        st.markdown("<span class='helper'>On a scale of 1–5: 1 = low workload, 5 = very high workload/expectations.</span>", unsafe_allow_html=True)
        academic_pressure = st.slider("", 1, 5, 3, key="ap")

        cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1)

        st.subheader("Study Satisfaction")
        st.markdown("<span class='helper'>On a scale of 1–5: 1 = not satisfied with study time, 5 = very satisfied with study time.</span>", unsafe_allow_html=True)
        study_satisfaction = st.slider("", 1, 5, 3, key="ss")

    with col2:
        sleep_duration = st.selectbox("Sleep Duration", ["5-6 hours", "<5 hours", "7-8 hours", ">8 hours", "Others"])
        diet = st.selectbox("Dietary Habits", ["Healthy", "Moderate", "Unhealthy", "Others"])
        degree = st.selectbox("Degree", ["B.Sc", "BA", "BCA", "B.Tech", "M.Sc", "PhD", "Others"])

        st.subheader("Financial Stress")
        st.markdown("<span class='helper'>On a scale of 1–5: 1 = low/no financial strain, 5 = severe financial pressure.</span>", unsafe_allow_html=True)
        financial_stress = st.slider("", 1, 5, 3, key="fs")

        suicidal = st.radio("Have you ever had suicidal thoughts?", ["No", "Yes"], horizontal=True)
        fam_hist = st.radio("Is anyone in your family currently facing a mental health issue?", ["No", "Yes"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Prediction ---
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#FFFFFF;'>🔎 Gentle Check-In</h3>", unsafe_allow_html=True)
    st.caption(SAFE_NOTE)

    if st.button("See My Reflections"):
        input_data = pd.DataFrame({
            "Gender": [gender],
            "Age": [age],
            "Academic Pressure": [academic_pressure],
            "CGPA": [cgpa],
            "Study Satisfaction": [study_satisfaction],
            "Sleep Duration": [sleep_duration],
            "Dietary Habits": [diet],
            "Degree": [degree],
            "Financial Stress": [financial_stress],
            "Suicidal Thoughts": [1 if suicidal == "Yes" else 0],
            "Fam_hist_ml": [1 if fam_hist == "Yes" else 0],
        })
        try:
            prediction = model.predict(input_data)[0]
            st.session_state.predicted = True
            st.session_state.prediction_result = prediction

            n = st.session_state.name
            if prediction == 1:
                st.markdown("<p class='health-red'>⚠️ You may be at risk of depression.</p>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div style='font-size:16px; line-height:1.7; color:#FFFFFF;'>
                    {n}, I see you. I hear you. The weight you carry is real, and your feelings make sense. You do not have to hold it alone. 
                    Consider talking with a trusted friend or family member, and if you can, reach out to a counselor or support line. 
                    Try saying to yourself: <em>“This weight will not end me, I will emerge victorious.”</em> 
                    Small steps are enough. You matter here. 🌿
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("<p class='health-green'>✅ You are not at risk of depression.</p>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div style='font-size:16px; line-height:1.7; color:#FFFFFF;'>
                    {n}, you’re doing a wonderful job balancing life and academics. Keep choosing rest, connection, and routines that nourish you. 
                    If you ever feel yourself slowing down, pause, breathe, and choose you. Your well-being is worth protecting. 🌱
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        except Exception as e:
            st.warning("We couldn’t complete the check-in. Please review your inputs and try again.")
            st.text(str(e))

    c_prev, c_next = st.columns(2)
    with c_prev:
        if st.button("⬅️ Back"):
            st.session_state.page = "welcome_message"
    with c_next:
        if st.session_state.predicted and st.button("Learn More About Depression →"):
            st.session_state.page = "knowledge"

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# KNOWLEDGE PAGE
# -----------------------------
elif st.session_state.page == "knowledge":
    st.markdown("<h1 style='text-align:center; color:#FFFFFF;'>📘 Understanding & Overcoming Depression (for Students)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#80E7D8;'>Gentle guidance you can return to anytime. Save or share with a friend who may need it.</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    with st.expander("What is depression? (simple)", expanded=True):
        st.write(
            """
            Depression is a common mental health condition that can affect how you feel, think, and function day-to-day. 
            It is more than sadness — it can feel like heaviness, numbness, or a loss of energy and interest. 
            Depression is treatable, and many students recover with support, care, and time.
            """
        )

    with st.expander("Signs & symptoms (emotional, physical, behavioral)"):
        st.write(
            """
            **Emotional**: persistent sadness, irritability, emptiness, guilt, hopelessness.
            
            **Physical**: sleep changes (too little/too much), appetite changes, fatigue, headaches.
            
            **Behavioral**: loss of interest in activities, withdrawal from friends, difficulty focusing, academic decline.
            """
        )

    with st.expander("Why it matters (student life)"):
        st.write(
            """
            Depression can make studying, attending classes, or keeping up with responsibilities feel overwhelming. 
            It can affect relationships, motivation, and self-esteem. 
            Identifying it early helps you get the right support so you can heal and continue growing.
            """
        )

    with st.expander("Coping & self-care you can start today"):
        st.write(
            """
            - **Gentle routines**: aim for 7–8 hours of sleep, regular meals, light movement or short walks.
            - **Mind-body care**: deep breathing, journaling, stretching, prayer/meditation.
            - **Connection**: talk with a friend, mentor, or join a support group; you are not a burden.
            - **Study with kindness**: break tasks into tiny steps (10–20 minutes), use timers, and celebrate small wins.
            - **Limit overwhelm**: reduce late-night scrolling, set restful boundaries, say no when you need to.
            - **Crisis planning**: if thoughts of self-harm appear, seek immediate support (hotline, counselor, or trusted adult).
            """
        )

    with st.expander("When to seek professional support"):
        st.write(
            """
            - Symptoms last **two weeks or more** and affect daily life.
            - You struggle to study, attend classes, or get out of bed.
            - You have thoughts of self-harm or feel unsafe — please reach out immediately.
            - You want guidance from a counselor, therapist, or doctor to feel better sooner.
            """
        )

    with st.expander("Resources & hotlines (start here)"):
        st.write(
            """
            - **Campus counseling**: your school may offer free or subsidized counseling.
            - **Local mental health services**: search for community clinics or NGOs near you.
            - **International resources**: WHO mental health resources, local/national helplines.
            - **Online therapy**: platforms like BetterHelp/Talkspace (availability varies by country).
            
            *If you feel at immediate risk, contact local emergency services or a crisis line in your country.*
            """
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⬅️ Back to Details"):
        st.session_state.page = "details"
# -----------------------------
# Moving Footer
# -----------------------------
st.markdown(
    """
    <style>
    .moving-footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f0f4f8;
        color: #333;
        text-align: center;
        padding: 10px;
        font-size: 16px;
        font-weight: 500;
        overflow: hidden;
        white-space: nowrap;
    }

    .moving-footer span {
        display: inline-block;
        padding-left: 100%;
        animation: scroll-left 20s linear infinite;
    }

    @keyframes scroll-left {
        0% {
            transform: translateX(100%);
        }
        100% {
            transform: translateX(-100%);
        }
    }
    </style>

    <div class="moving-footer">
      <span>🌱 You are not alone • You are strong • You are loved • You are enough • Keep going • One gentle step at a time 🌸</span>
    </div>
    """,
    unsafe_allow_html=True
)
