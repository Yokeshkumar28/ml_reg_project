import streamlit as st
import pandas as pd
import requests
from prediction_helper import predict

# ---------- Page Setup ----------
st.set_page_config(page_title="Health Insurance Premium Predictor", layout="wide")

# ---------- Custom Styles & Fonts ----------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
    background-color: #000000;
    color: white;
}
h1, h2, h3, h4, h5, h6, label, .stMarkdown {
    color: #ffffff !important;
}
.stButton>button {
    background-color: #00C853;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}
.stNumberInput input, .stSelectbox div, .stTextInput input {
    background-color: #222 !important;
    color: white !important;
    border-radius: 10px;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- Optional Lottie Animation ----------
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

from streamlit_lottie import st_lottie
lottie = load_lottie_url("https://lottie.host/48ab53a8-84e1-4cfd-a958-d99299de36f2/0fEOHkVInI.json")
if lottie:
    st_lottie(lottie, height=180, key="insurance")

# ---------- App Title ----------
st.title("🧪 Health Insurance Premium Predictor")
st.markdown("Estimate your premium based on personal, medical, and employment details.")
st.markdown("---")

# ---------- Form ----------
with st.form("prediction_form"):
    def section(title):
        st.markdown(f"""
        <div style="background-color:#111111; padding: 20px; border-radius: 15px; margin-top: 10px; box-shadow: 0 0 5px rgba(255,255,255,0.05);">
        <h4>{title}</h4>
        """, unsafe_allow_html=True)

    section("👤 Personal Details")
    r1 = st.columns(3)
    with r1[0]:
        age = st.number_input('Age', min_value=18, max_value=100, step=1)
    with r1[1]:
        dependents = st.number_input("Number of Dependents", min_value=0, max_value=5, step=1)
    with r1[2]:
        income_lakhs = st.number_input("Income in Lakhs", min_value=0, max_value=100, step=1)
    st.markdown("</div>", unsafe_allow_html=True)

    section("🧬 Medical Details")
    r2 = st.columns(3)
    with r2[0]:
        genetical_risk = st.number_input('Genetical Risk (0-5)', min_value=0, max_value=5, step=1)
    with r2[1]:
        bmi_category = st.selectbox("🢍 BMI Category", ['Overweight', 'Underweight', 'Normal', 'Obesity'])
    with r2[2]:
        smoking_status = st.selectbox("🚬 Smoking Status", ['Regular', 'No Smoking', 'Occasional'])

    r3 = st.columns(3)
    with r3[0]:
        gender = st.selectbox("🛫 Gender", ['Male', 'Female'])
    with r3[1]:
        marital_status = st.selectbox("💍 Marital Status", ['Unmarried', 'Married'])
    with r3[2]:
        medical_history = st.selectbox("🏥 Medical History", [
            'High blood pressure', 'No Disease', 'Diabetes & High blood pressure',
            'Diabetes & Heart disease', 'Diabetes', 'Diabetes & Thyroid',
            'Heart disease', 'Thyroid', 'High blood pressure & Heart disease'
        ])
    st.markdown("</div>", unsafe_allow_html=True)

    section("💼 Employment & Insurance")
    r4 = st.columns(3)
    with r4[0]:
        insurance_plan = st.selectbox("📄 Insurance Plan", ['Silver', 'Bronze', 'Gold'])
    with r4[1]:
        employment_status = st.selectbox("💼 Employment Status", ['Self-Employed', 'Freelancer', 'Salaried'])
    with r4[2]:
        region = st.selectbox("🌍 Region", ['Northeast', 'Northwest', 'Southeast', 'Southwest'])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    submit = st.form_submit_button("🔮 Predict Premium")

# ---------- Prediction & Result ----------
if submit:
    input_dict = {
        'Age': age,
        'Number of Dependents': dependents,
        'Income in Lakhs': income_lakhs,
        'Genetical Risk': genetical_risk,
        'Insurance Plan': insurance_plan,
        'Employment Status': employment_status,
        'Gender': gender,
        'Maritial Status': marital_status,
        'BMI Category': bmi_category,
        'Smoking status': smoking_status,
        'Region': region,
        'Medical History': medical_history
    }

    try:
        prediction = predict(input_dict)

        st.markdown("---")
        st.success("✅ Prediction Complete")
        st.metric(label="💰 Predicted Premium (in ₹)", value=f"{prediction:,.0f}")

        # ---------- Personalized Health Advice ----------
        st.markdown("### 🧠 Health Feedback")

        health_score = 10
        if smoking_status == 'Regular':
            health_score -= 4
        elif smoking_status == 'Occasional':
            health_score -= 2

        if bmi_category == 'Obesity':
            health_score -= 3
        elif bmi_category == 'Overweight':
            health_score -= 2
        elif bmi_category == 'Underweight':
            health_score -= 1

        if medical_history != 'No Disease':
            health_score -= 3

        if genetical_risk >= 3:
            health_score -= 2

        if health_score >= 8:
            st.success("🟢 Your health is **Good**. Keep up the healthy habits!")
        elif 5 <= health_score < 8:
            st.warning("🟡 Your health is **Moderate**. You may want to take some precautions.")
        else:
            st.error("🔴 Your health is **At Risk**. Consider making lifestyle changes and consulting a doctor.")

        st.markdown("#### 💡 Health Tips for You")
        tips = []

        if smoking_status != 'No Smoking':
            tips.append("🚭 Consider quitting or reducing smoking to lower your risk of chronic illness.")

        if bmi_category in ['Obesity', 'Overweight']:
            tips.append("🏃 Regular exercise and a balanced diet can help you manage your weight.")

        if medical_history != 'No Disease':
            tips.append("🦠 Monitor your existing condition and follow up with your healthcare provider regularly.")

        if genetical_risk >= 3:
            tips.append("🧬 Since you have a higher genetic risk, early screening and preventive care are important.")

        if not tips:
            tips.append("🎉 You're doing great! Continue maintaining a healthy lifestyle.")

        for tip in tips:
            st.markdown(f"- {tip}")

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
