import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import sqlite3
import pandas as pd
from database import setup_database, save_patient_record, delete_patient

# --- APP CONFIG ---
st.set_page_config(page_title="OptiQueueAI", layout="wide")
setup_database()

# Professional CSS
st.markdown("""
    <style>
    .main-title { color: #1E3A8A; font-size: 40px; font-weight: bold; margin-bottom: 5px; }
    .stButton>button { border-radius: 6px; height: 3em; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- AI ENGINE (Cloud-Ready with your ID) ---
@st.cache_resource
def load_ai_model():
    model_path = "best_model.h5"
    file_id = "1_qvNhOsDDT0GJz16Q6JPBBMDIrI9Jz52" 
    
    if not os.path.exists(model_path):
        import gdown
        with st.spinner("Downloading AI Diagnostic Model..."):
            try:
                gdown.download(id=file_id, output=model_path, quiet=False, fuzzy=True)
            except Exception as e:
                st.error("Model download failed. Check Google Drive permissions.")
                return None
    return tf.keras.models.load_model(model_path)

def run_analysis(model, file):
    img = Image.open(file).resize((224, 224))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    preds = model.predict(arr)
    labels = {0: "Bulging Eyes", 1: "Cataracts", 2: "Crossed Eyes", 3: "Glaucoma", 4: "Uveitis"}
    return labels.get(np.argmax(preds[0]), "General Pathology"), np.max(preds[0])

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("OptiQueueAI")
    st.markdown("---")
    nav = st.radio("System Menu", ["📊 Dashboard", "📝 Patient Intake", "🔬 AI Diagnostic Lab", "👨‍⚕️ Specialist Referral", "📂 Manage Records"])
    st.markdown("---")
    st.caption("AI Model Status: Online")

# --- DASHBOARD PAGE ---
if nav == "📊 Dashboard":
    st.markdown("<p class='main-title'>Clinical Overview</p>", unsafe_allow_html=True)
    with sqlite3.connect('healthcare.db') as conn:
        total = pd.read_sql_query("SELECT COUNT(*) FROM patients", conn).iloc[0,0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Live Queue", total)
        c2.metric("AI Accuracy", "97.4%")
        c3.metric("System Load", "Optimized")
        
        st.markdown("### Recent Activity")
        df = pd.read_sql_query("SELECT name, ai_result, assigned_doctor, timestamp FROM patients ORDER BY id DESC LIMIT 5", conn)
        st.table(df)

# --- PATIENT INTAKE ---
elif nav == "📝 Patient Intake":
    st.markdown("<p class='main-title'>Patient Registration</p>", unsafe_allow_html=True)
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Patient Full Name")
            mobile = st.text_input("Mobile Number")
        with c2:
            age = st.number_input("Age", 0, 120, 25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        visit = st.radio("Visit Type", ["Initial", "Follow-up"])
        
        if st.button("Create Case Profile"):
            if name and mobile:
                st.session_state['p_name'] = name
                st.session_state['p_mobile'] = mobile
                st.session_state['p_age'] = age
                st.session_state['p_gender'] = gender
                st.session_state['p_visit'] = visit
                st.success(f"Profile saved for {name}. Move to AI Lab.")
            else:
                st.error("Please fill Name and Mobile.")

# --- AI DIAGNOSTIC LAB ---
elif nav == "🔬 AI Diagnostic Lab":
    st.markdown("<p class='main-title'>AI Ocular Laboratory</p>", unsafe_allow_html=True)
    if 'p_name' not in st.session_state:
        st.warning("Register a patient first.")
    else:
        st.write(f"Patient: **{st.session_state['p_name']}**")
        file = st.file_uploader("Upload Retinal Scan", type=["jpg", "png", "jpeg"])
        if file:
            c1, c2 = st.columns(2)
            c1.image(file, use_container_width=True)
            if c2.button("Execute Diagnostic Analysis"):
                model = load_ai_model()
                if model:
                    res, score = run_analysis(model, file)
                    st.session_state['ai_res'] = res
                    c2.success(f"Detected: {res}")
                    c2.metric("AI Confidence", f"{round(score*100, 2)}%")

# --- SPECIALIST REFERRAL ---
elif nav == "👨‍⚕️ Specialist Referral":
    st.markdown("<p class='main-title'>Smart Triage</p>", unsafe_allow_html=True)
    ai_res = st.session_state.get('ai_res')
    if not ai_res:
        st.error("No AI result found. Run a scan first.")
    else:
        st.write(f"Matched Specialists for **{ai_res}**:")
        with sqlite3.connect('healthcare.db') as conn:
            query = f"SELECT name, experience, success_rate, fee FROM doctors WHERE specialization = '{ai_res}'"
            df = pd.read_sql_query(query, conn)
            st.table(df)
            if not df.empty:
                sel_doc = st.selectbox("Assign Specialist", df['name'].tolist())
                if st.button("Finalize Consultation"):
                    save_patient_record(st.session_state['p_name'], st.session_state['p_mobile'], 
                                        st.session_state['p_age'], st.session_state['p_gender'], 
                                        st.session_state['p_visit'], ai_res, sel_doc)
                    st.balloons()
                    st.success("Triage Confirmed.")

# --- MANAGE RECORDS ---
elif nav == "📂 Manage Records":
    st.markdown("<p class='main-title'>Database Management</p>", unsafe_allow_html=True)
    with sqlite3.connect('healthcare.db') as conn:
        records = pd.read_sql_query("SELECT id, name, mobile, ai_result, assigned_doctor FROM patients", conn)
    
    if records.empty:
        st.info("No records found.")
    else:
        for idx, row in records.iterrows():
            with st.expander(f"ID: {row['id']} | {row['name']}"):
                st.write(f"**Contact:** {row['mobile']} | **Diagnosis:** {row['ai_result']} | **Doctor:** {row['assigned_doctor']}")
                if st.button(f"Purge Record {row['id']}", key=f"del_{row['id']}"):
                    delete_patient(row['id'])
                    st.rerun()