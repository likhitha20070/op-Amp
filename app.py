import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ------------------ PDF FUNCTION ------------------
def generate_pdf(name, reg, dept, obs_data):
    file_name = "experiment_report.pdf"
    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("OP-AMP VIRTUAL LAB REPORT", styles['Title']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Name: {name}", styles['Normal']))
    content.append(Paragraph(f"Reg No: {reg}", styles['Normal']))
    content.append(Paragraph(f"Department: {dept}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Observation Data:", styles['Heading2']))
    for row in obs_data:
        content.append(Paragraph(str(row), styles['Normal']))

    content.append(Spacer(1, 10))
    content.append(Paragraph("Result:", styles['Heading2']))
    content.append(Paragraph("Experiment performed successfully and output verified.", styles['Normal']))

    doc.build(content)
    return file_name

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Op-Amp Virtual Lab", layout="wide")

# ------------------ SIDEBAR ------------------
st.sidebar.title("🔬 Virtual Lab Navigation")
page = st.sidebar.radio("Go to", [
    "Aim & Theory",
    "Apparatus Required",
    "Experiment",
    "Quiz",
    "Feedback"
])

# ------------------ PAGE 1 ------------------
if page == "Aim & Theory":
    st.title("🔬 OP-AMP VIRTUAL LAB")

    st.header("🎯 Aim")
    st.write("""
    To study the working and characteristics of Operational Amplifier circuits 
    such as Inverting Amplifier, Non-Inverting Amplifier, and Comparator.
    """)

    st.header("📖 Theory")
    st.write("""
    An Operational Amplifier (Op-Amp) is a high-gain differential amplifier widely used in analog electronics.

    It amplifies the difference between two input voltages and produces an output voltage.

    ### Key Features:
    - High input impedance  
    - Low output impedance  
    - High gain  

    ### Types of Configurations:

    🔹 Inverting Amplifier:
    Output is inverted and gain is given by:
    Gain = -Rf / Rin

    🔹 Non-Inverting Amplifier:
    Output is in phase with input:
    Gain = 1 + (Rf / Rin)

    🔹 Comparator:
    Compares input voltage with reference voltage and gives digital output.

    ### Applications:
    - Signal amplification  
    - Filtering  
    - Oscillators  
    - Voltage comparison  
    """)

# ------------------ PAGE 2 ------------------
elif page == "Apparatus Required":
    st.title("🧰 Apparatus Required")

    st.write("""
    - Operational Amplifier IC (741)  
    - Resistors  
    - Breadboard  
    - Power Supply  
    - Function Generator  
    - CRO (Oscilloscope)  
    - Connecting Wires  
    """)

# ------------------ PAGE 3 ------------------
elif page == "Experiment":
    st.title("🧪 Experiment")

    # Student details
    st.subheader("👨‍🎓 Student Details")
    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Name")
    with col2:
        reg = st.text_input("Register Number")
    with col3:
        dept = st.text_input("Department")

    st.subheader("📋 Observation Table")

    rows = 5
    obs_data = []

    for i in range(rows):
        col1, col2 = st.columns(2)
        with col1:
            vin = st.number_input(f"Vin (Row {i+1})", key=f"vin{i}")
        with col2:
            vout = st.number_input(f"Vout (Row {i+1})", key=f"vout{i}")

        obs_data.append((vin, vout))

    # Run experiment
    if st.button("▶ Run Experiment"):
        st.success("✅ Experiment has been run successfully!")

        # Graph
        vin_vals = [x[0] for x in obs_data]
        vout_vals = [x[1] for x in obs_data]

        fig, ax = plt.subplots()
        ax.plot(vin_vals, vout_vals, marker='o')
        ax.set_xlabel("Input Voltage (Vin)")
        ax.set_ylabel("Output Voltage (Vout)")
        ax.set_title("Input vs Output Graph")

        st.pyplot(fig)

        st.subheader("📌 Result")
        st.write("The Op-Amp characteristics are verified successfully.")

        # PDF download
        pdf = generate_pdf(name, reg, dept, obs_data)

        with open(pdf, "rb") as f:
            st.download_button("⬇ Download Full Report", f, file_name="report.pdf")

# ------------------ PAGE 4 ------------------
elif page == "Quiz":
    st.title("🧠 Quiz")

    questions = [
        {"q": "Op-Amp gain is?", "opt": ["High", "Low"], "ans": "High"},
        {"q": "Inverting gain formula?", "opt": ["-Rf/Rin", "Rf/Rin"], "ans": "-Rf/Rin"},
        {"q": "Non-inverting gain?", "opt": ["1+Rf/Rin", "Rf/Rin"], "ans": "1+Rf/Rin"},
        {"q": "Comparator output?", "opt": ["Digital", "Analog"], "ans": "Digital"},
        {"q": "Op-Amp input type?", "opt": ["Differential", "Single"], "ans": "Differential"},
        {"q": "IC used?", "opt": ["741", "555"], "ans": "741"},
        {"q": "Feedback used?", "opt": ["Yes", "No"], "ans": "Yes"},
        {"q": "Output saturation?", "opt": ["Yes", "No"], "ans": "Yes"},
        {"q": "Used for?", "opt": ["Amplifier", "Motor"], "ans": "Amplifier"},
        {"q": "Gain type?", "opt": ["Voltage", "Current"], "ans": "Voltage"}
    ]

    score = 0

    for i, q in enumerate(questions):
        ans = st.radio(q["q"], q["opt"], key=i)
        if ans == q["ans"]:
            score += 1

    if st.button("Submit Quiz"):
        st.success(f"Your Score: {score}/10")

# ------------------ PAGE 5 ------------------
elif page == "Feedback":
    st.title("💬 Feedback Form")

    q1 = st.text_input("1. How was the virtual lab experience?")
    q2 = st.text_input("2. Was the theory clear?")
    q3 = st.text_input("3. How was the experiment interface?")
    q4 = st.text_input("4. Suggestions for improvement?")
    q5 = st.text_input("5. Overall feedback")

    if st.button("Submit Feedback"):
        st.success("✅ Thank you for your feedback!")
