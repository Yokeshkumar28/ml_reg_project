# Frontend using streamlit

import streamlit as st
from prediction_helper import predict

st.markdown("### Health insurance Premium prediction")

categorical_options = {
    'Gender' : ['Male','Female'],
    'region' : ['Northeast', 'Northwest', 'Southeast', 'Southwest'],
    'Marital_Status' : ['Unmarried', 'Married'],
    'BMI_category' : ['Overweight' ,'Underweight' ,'Normal' ,'Obesity'],
    'Smoking_Status' : ['Regular', 'No Smoking', 'Occasional'],
    'employment_status' : ['Self-Employed', 'Freelancer', 'Salaried'],
     'medical_history' : ['High blood pressure', 'No Disease', 'Diabetes & High blood pressure',
 'Diabetes & Heart disease' ,'Diabetes' ,'Diabetes & Thyroid',
 'Heart disease' ,'Thyroid' ,'High blood pressure & Heart disease'],
    'insurance_plan' : ['Silver' ,'Bronze' ,'Gold']
}

row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

with row1[0]:
    age = st.number_input('Age', min_value = 18, step = 1, max_value = 100)
with row1[1]:
    number_of_dependents = st.number_input("Number of Dependents",min_value = 0, step = 1, max_value = 5 )
with row1[2]:
    income_lakhs = st.number_input("Income in Lakhs",min_value = 0, step = 1, max_value = 100 )

with row2[0]:
    genetical_risk =  st.number_input('Genetical Risk', min_value = 0, step = 1, max_value = 5)
with row2[1]:
    insurance_plan = st.selectbox("Insurance plan", categorical_options['insurance_plan'])
with row2[2]:
    employment_status = st.selectbox("Employment Status", categorical_options['employment_status'])

with row3[0]:
    gender =  st.selectbox("Gender", categorical_options['Gender'])
with row3[1]:
    marital_status = st.selectbox(" marital_status", categorical_options['Marital_Status'])
with row3[2]:
    bmi_category = st.selectbox("BMI category", categorical_options['BMI_category'])

with row4[0]:
    smoking_status     =  st.selectbox("Smoking Status", categorical_options['Smoking_Status'])
with row4[1]:
    region = st.selectbox("Region", categorical_options['region'])
with row4[2]:
    medical_history = st.selectbox("Medical History", categorical_options['medical_history'])

# Create a dictionary for input values
input_dict = {
    'Age' : age,
    'Number of Dependents' : number_of_dependents,
    'Income in Lakhs' : income_lakhs,
    'Genetical Risk' : genetical_risk,
    'Insurance Plan' : insurance_plan,
    'Employment Status' : employment_status,
    'Gender' : gender,
    'Maritial Status' : marital_status,
    'BMI Category': bmi_category,
    'Smoking status' : smoking_status,
    'Region' : region,
    'Medical History' : medical_history
}

if st.button("Predict Premium"):
    prediction = predict(input_dict)
    st.success(f"Predicted Health insurance Premium: {prediction}")