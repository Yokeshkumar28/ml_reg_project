import streamlit as st
import pandas as pd
import requests
from prediction_helper import predict
from streamlit_lottie import st_lottie

# ---------- Page Setup ----------
st.set_page_config(page_title="Health Insurance Premium Predictor", layout="wide")

# ---------- Load Lottie Animation ----------
@st.cache_data
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie = load_lottie_url("https://lottie.host/48ab53a8-84e1-4cfd-a958-d99299de36f2/0fEOHkVInI.json")
if lottie:
    st_lottie(lottie, height=180, key="insurance")

# ---------- Custom Styles ----------
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

# ---------- App Title ----------
st.title("🧪 Health Insurance Premium Predictor")
st.markdown("Estimate your premium based on personal, medical, and employment details.")
st.markdown("---")

# ---------- Input Form ----------
with st.form("prediction_form"):

    def section(title):
        st.markdown(f"""
        <div style="background-color:#111111; padding: 20px; border-radius: 15px; margin-top: 10px;">
        <h4>{title}</h4>
        """, unsafe_allow_html=True)

    # Personal
    section("👤 Personal Details")
    col1, col2, col3 = st.columns(3)
    age = col1.number_input('Age', min_value=18, max_value=100, step=1)
    dependents = col2.number_input("Number of Dependents", min_value=0, max_value=5, step=1)
    income = col3.number_input("Income in Lakhs", min_value=0.0, max_value=100.0, step=0.1)
    st.markdown("</div>", unsafe_allow_html=True)

    # Medical
    section("🧬 Medical Details")
    col4, col5, col6 = st.columns(3)
    genetical_risk = col4.number_input('Genetical Risk (0-5)', min_value=0, max_value=5, step=1)
    bmi = col5.selectbox("🢍 BMI Category", ['Overweight', 'Underweight', 'Normal', 'Obesity'])
    smoking = col6.selectbox("🚬 Smoking Status", ['Regular', 'No Smoking', 'Occasional'])

    col7, col8, col9 = st.columns(3)
    gender = col7.selectbox("🛫 Gender", ['Male', 'Female'])
    marital = col8.selectbox("💍 Marital Status", ['Unmarried', 'Married'])
    history = col9.selectbox("🏥 Medical History", [
        'High blood pressure', 'No Disease', 'Diabetes & High blood pressure',
        'Diabetes & Heart disease', 'Diabetes', 'Diabetes & Thyroid',
        'Heart disease', 'Thyroid', 'High blood pressure & Heart disease'
    ])
    st.markdown("</div>", unsafe_allow_html=True)

    # Employment
    section("💼 Employment & Insurance")
    col10, col11, col12 = st.columns(3)
    plan = col10.selectbox("📄 Insurance Plan", ['Silver', 'Bronze', 'Gold'])
    status = col11.selectbox("💼 Employment Status", ['Self-Employed', 'Freelancer', 'Salaried'])
    region = col12.selectbox("🌍 Region", ['Northeast', 'Northwest', 'Southeast', 'Southwest'])
    st.markdown("</div>", unsafe_allow_html=True)

    submit = st.form_submit_button("🔮 Predict Premium")

# ---------- On Submit ----------
if submit:
    input_data = {
        'Age': age,
        'Number of Dependents': dependents,
        'Income in Lakhs': income,
        'Genetical Risk': genetical_risk,
        'Insurance Plan': plan,
        'Employment Status': status,
        'Gender': gender,
        'Maritial Status': marital,
        'BMI Category': bmi,
        'Smoking status': smoking,
        'Region': region,
        'Medical History': history
    }

    with st.spinner("Predicting your premium..."):
        try:
            prediction = predict(input_data)

            st.markdown("---")
            st.success("✅ Prediction Complete")
            st.metric(label="💰 Predicted Premium (in ₹)", value=f"{prediction:,.0f}")

            # Health Score Logic
            st.markdown("### 🧠 Health Feedback")

            score = 10
            if smoking == 'Regular': score -= 4
            elif smoking == 'Occasional': score -= 2
            if bmi == 'Obesity': score -= 3
            elif bmi == 'Overweight': score -= 2
            elif bmi == 'Underweight': score -= 1
            if history != 'No Disease': score -= 3
            if genetical_risk >= 3: score -= 2

            if score >= 8:
                st.success("🟢 Your health is **Good**.")
            elif score >= 5:
                st.warning("🟡 Your health is **Moderate**.")
            else:
                st.error("🔴 Your health is **At Risk**.")

            st.markdown("#### 💡 Health Tips")
            tips = []
            if smoking != 'No Smoking':
                tips.append("🚭 Reduce or quit smoking.")
            if bmi in ['Obesity', 'Overweight']:
                tips.append("🏃‍♀️ Adopt a healthy diet and exercise.")
            if history != 'No Disease':
                tips.append("🩺 Monitor your health and consult a doctor.")
            if genetical_risk >= 3:
                tips.append("🧬 Consider genetic counseling or preventive screening.")

            if not tips:
                tips.append("🎉 You're doing great! Keep up your healthy lifestyle.")

            for tip in tips:
                st.markdown(f"- {tip}")

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
