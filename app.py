import streamlit as st
import joblib
import pandas as pd

# Load model
model = joblib.load("Depression_predictor.pkl")

# App design
st.set_page_config(page_title="Student Depression Risk", page_icon="🧠", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .main { background-color: #F5FFFA; }
        h1 { color: #00796B; text-align: center; }
        .stButton>button {
            background-color: #00BFA6;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px 24px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🧠 Depression Risk Predictor for Students</h1>", unsafe_allow_html=True)
st.write("Mental health matters. This tool helps raise awareness about potential depression risks among students. 💚")

# Sidebar inputs
st.sidebar.header("📌 Input Student Details")
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
age = st.sidebar.slider("Age", 15, 40, 20)
academic_pressure = st.sidebar.slider("Academic Pressure (1-5)", 1, 5, 3)
cgpa = st.sidebar.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1)
study_satisfaction = st.sidebar.slider("Study Satisfaction (1-5)", 1, 5, 3)
sleep_duration = st.sidebar.selectbox("Sleep Duration", 
                                      ['5-6 hours', 'Less than 5 hours', 
                                       '7-8 hours', 'More than 8 hours', 'Others'])
diet = st.sidebar.selectbox("Dietary Habits", ['Healthy', 'Moderate', 'Unhealthy', 'Others'])
degree = st.sidebar.selectbox("Degree", 
                              ['B.Pharm','BSc','BA','BCA','M.Tech','PhD','Class 12','B.Ed','LLB',
                               'BE','M.Ed','MSc','BHM','M.Pharm','MCA','MA','B.Com','MD','MBA',
                               'MBBS','M.Com','B.Arch','LLM','B.Tech','BBA','ME','MHM','Others'])
financial_stress = st.sidebar.slider("Financial Stress (1-5)", 1, 5, 3)
suicidal = st.sidebar.selectbox("Suicidal Thoughts", ["No", "Yes"])
fam_hist = st.sidebar.selectbox("Family History of Mental Illness", ["No", "Yes"])

# Convert categorical to numeric (dummy encoding placeholder)
input_data = pd.DataFrame({
    'Gender': [gender],
    'Age': [age],
    'Academic Pressure': [academic_pressure],
    'CGPA': [cgpa],
    'Study Satisfaction': [study_satisfaction],
    'Sleep Duration': [sleep_duration],
    'Dietary Habits': [diet],
    'Degree': [degree],
    'Financial Stress': [financial_stress],
    'Suicidal thoughts': [1 if "Yes" in suicidal else 0],
    'Fam_hist_ml': [1 if "Yes" in fam_hist else 0]
})

# Prediction button
if st.sidebar.button("🔎 Predict"):
    # Encoding must match training
    try:
        prediction = model.predict(input_data)[0]
        if prediction == 1:
            st.error("⚠️ High Risk: The student may be experiencing depression.")
            st.markdown("**💡 Suggestion:** Consider seeking counseling support, stress management, and community help.")
        else:
            st.success("✅ Low Risk: The student is unlikely to be experiencing depression.")
            st.markdown("**💚 Keep it up:** Maintain balance with sleep, studies, and healthy habits.")
    except Exception as e:
        st.warning("⚠️ Something went wrong. Ensure model encoding matches inputs.")
        st.text(str(e))

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("🔒 **Disclaimer:** This tool is not a medical diagnosis. It is for awareness and educational purposes only.")

