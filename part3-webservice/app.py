import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage
import os
import re
import io

st.set_page_config(page_title="TOPSIS Calculator", layout="centered")

st.markdown("""
<style>
body {background-color:#0e1117;}
.block-container {
    max-width:420px;
    background:#1c1f26;
    padding:30px;
    border-radius:10px;
    box-shadow:0 0 15px rgba(0,0,0,0.6);
    color:white;
}
div.stButton > button {
    background-color:orange;
    color:black;
    font-weight:bold;
    width:100%;
}
</style>
""", unsafe_allow_html=True)

st.title("TOPSIS Calculator")

uploaded_file = st.file_uploader("File Name", type=["csv","xlsx"])
weights_input = st.text_input("Weights", placeholder="1,1,1,1")
impacts_input = st.text_input("Impacts", placeholder="+,+,+,+")
email_input = st.text_input("Email Id", placeholder="example@gmail.com")

# ---------- EMAIL VALIDATION ----------
def valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

# ---------- TOPSIS FUNCTION ----------
def run_topsis(df, weights, impacts):

    if weights.strip() == "" or impacts.strip() == "":
        return None

    try:
        weights = [float(w.strip()) for w in weights.split(',')]
    except:
        return None

    impacts = [i.strip() for i in impacts.split(',')]

    if any(i not in ['+','-'] for i in impacts):
        return None

    data = df.iloc[:,1:].astype(float).values

    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        return None

    norm = data / np.sqrt((data**2).sum(axis=0))
    weighted = norm * weights

    best, worst = [], []
    for i in range(len(impacts)):
        if impacts[i] == '+':
            best.append(weighted[:,i].max())
            worst.append(weighted[:,i].min())
        else:
            best.append(weighted[:,i].min())
            worst.append(weighted[:,i].max())

    best, worst = np.array(best), np.array(worst)

    d_best = np.sqrt(((weighted-best)**2).sum(axis=1))
    d_worst = np.sqrt(((weighted-worst)**2).sum(axis=1))

    score = d_worst/(d_best+d_worst)
    rank = score.argsort()[::-1] + 1

    df['Topsis Score'] = score
    df['Rank'] = rank
    return df

# ---------- EMAIL FUNCTION ----------
def send_email(receiver, file_bytes):
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

    msg = EmailMessage()
    msg['Subject'] = 'TOPSIS Result'
    msg['From'] = EMAIL_USER
    msg['To'] = receiver
    msg.set_content("Attached is your TOPSIS result file.")

    msg.add_attachment(
        file_bytes,
        maintype='application',
        subtype='octet-stream',
        filename='topsis_result.csv'
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

# ---------- SUBMIT ----------
if st.button("Submit"):
    if not uploaded_file:
        st.error("Upload file first.")
    elif not valid_email(email_input):
        st.error("Invalid email format.")
    else:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        result_df = run_topsis(df, weights_input, impacts_input)

        if result_df is None:
            st.error("Invalid weights or impacts.")
        else:
            buffer = io.StringIO()
            result_df.to_csv(buffer, index=False)
            send_email(email_input, buffer.getvalue().encode())
            st.success("Result sent to your email!")