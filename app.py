import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="MOSFET Virtual Lab", layout="wide")

# ------------------ CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #00d4ff;
}
.stButton>button {
    background-color: #00d4ff;
    color: black;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("🔬 MOSFET Lab")
page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Aim & Theory", "Experiment", "Quiz", "Feedback"]
)

# ------------------ DASHBOARD ------------------
if page == "Dashboard":
    st.title("🔬 MOSFET Virtual Laboratory")

    st.markdown("""
    Welcome to the **Interactive MOSFET Simulation Lab** 🎯  

    ### ✨ Features:
    ✔ Interactive MOSFET Output Characteristics  
    ✔ Real-time Graph Visualization  
    ✔ Quiz to test understanding  
    ✔ Feedback system  
    ✔ Downloadable Experiment Report  

    👉 Use the sidebar to explore!
    """)

# ------------------ AIM & THEORY ------------------
elif page == "Aim & Theory":
    st.title("📘 Aim & Theory")

    st.header("🎯 Aim")
    st.write("""
    To study the characteristics of an N-channel MOSFET and analyze the relationship 
    between Drain Current (Id), Gate Voltage (Vgs), and Drain Voltage (Vds).
    """)

    st.header("📖 Theory")
    st.markdown("""
    ### 🔹 What is MOSFET?
    A MOSFET is a voltage-controlled semiconductor device.

    ### 🔹 Regions of Operation:
    1. Cutoff Region  
    2. Triode Region  
    3. Saturation Region  

    ### 🔹 Equation:
    Id = k (Vgs - Vt)^2

    ### 🔹 Applications:
    - Amplifiers  
    - Switching circuits  
    - Power electronics  
    """)

# ------------------ PDF FUNCTION ------------------
def generate_pdf(Vgs, Vt, k):
    file_name = "mosfet_report.pdf"
    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("MOSFET Experiment Report", styles['Title']))
    content.append(Paragraph(f"Gate Voltage (Vgs): {Vgs}", styles['Normal']))
    content.append(Paragraph(f"Threshold Voltage (Vt): {Vt}", styles['Normal']))
    content.append(Paragraph(f"Constant (k): {k}", styles['Normal']))

    doc.build(content)
    return file_name

# ------------------ EXPERIMENT ------------------
elif page == "Experiment":
    st.title("🧪 MOSFET Experiment")

    st.sidebar.header("⚙ Input Parameters")

    Vgs = st.sidebar.slider("Gate Voltage (Vgs)", 0.0, 5.0, 2.5)
    Vt = st.sidebar.slider("Threshold Voltage (Vt)", 0.5, 2.0, 1.0)
    k = st.sidebar.slider("Constant (k)", 0.1, 2.0, 1.0)

    Vds = np.linspace(0, 5, 100)

    Id = []
    for v in Vds:
        if Vgs <= Vt:
            Id.append(0)
        elif v < (Vgs - Vt):
            Id.append(k * ((Vgs - Vt) * v - (v**2) / 2))
        else:
            Id.append(k * (Vgs - Vt) ** 2)

    Id = np.array(Id)

    st.subheader("📊 Output Characteristics")

    fig, ax = plt.subplots()
    ax.plot(Vds, Id)
    ax.set_xlabel("Vds")
    ax.set_ylabel("Id")
    ax.set_title("MOSFET Output Characteristics")

    st.pyplot(fig)

    st.subheader("📌 Results")
    st.write(f"Vgs = {Vgs}, Vt = {Vt}, k = {k}")

    if st.button("📄 Generate Report"):
        pdf_file = generate_pdf(Vgs, Vt, k)

        with open(pdf_file, "rb") as f:
            st.download_button(
                label="⬇ Download PDF",
                data=f,
                file_name="mosfet_report.pdf"
            )

# ------------------ QUIZ ------------------
elif page == "Quiz":
    st.title("🧠 MOSFET Quiz")

    questions = [
        {"q": "MOSFET is a ___ controlled device?", "opt": ["Current", "Voltage", "Power", "Resistance"], "ans": "Voltage"},
        {"q": "MOSFET stands for?", "opt": ["Metal Oxide Semiconductor Field Effect Transistor", "Micro System"], "ans": "Metal Oxide Semiconductor Field Effect Transistor"},
        {"q": "Which terminal controls current?", "opt": ["Gate", "Drain", "Source"], "ans": "Gate"},
        {"q": "Cutoff region current?", "opt": ["Zero", "High"], "ans": "Zero"},
        {"q": "Vt means?", "opt": ["Threshold voltage", "Test voltage"], "ans": "Threshold voltage"},
        {"q": "MOSFET used as switch?", "opt": ["Yes", "No"], "ans": "Yes"},
        {"q": "Drain current symbol?", "opt": ["Id", "Ig"], "ans": "Id"},
        {"q": "MOSFET type?", "opt": ["N-channel", "P-channel", "Both"], "ans": "Both"},
        {"q": "Device control type?", "opt": ["Voltage", "Current"], "ans": "Voltage"},
        {"q": "Region for amplification?", "opt": ["Saturation", "Cutoff"], "ans": "Saturation"}
    ]

    score = 0

    for i, q in enumerate(questions):
        st.subheader(f"Q{i+1}: {q['q']}")
        ans = st.radio("Select answer", q["opt"], key=i)
        if ans == q["ans"]:
            score += 1

    if st.button("Submit Quiz"):
        st.success(f"Your Score: {score}/10")

# ------------------ FEEDBACK ------------------
elif page == "Feedback":
    st.title("💬 Feedback")

    q1 = st.slider("How was the UI?", 1, 5)
    q2 = st.slider("Concept clarity?", 1, 5)
    q3 = st.slider("Simulation usefulness?", 1, 5)
    q4 = st.slider("Ease of use?", 1, 5)
    q5 = st.slider("Overall rating?", 1, 5)

    if st.button("Submit Feedback"):
        st.success("✅ Thank you for your feedback!")
