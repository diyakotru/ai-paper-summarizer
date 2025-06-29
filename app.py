import streamlit as st
import fitz
from transformers import pipeline

import base64

summarizer = pipeline(
    "summarization", 
    model="facebook/bart-large-cnn", 
    device=-1
)

def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("marketing.jpg")

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Smart Summarizer", layout="wide", initial_sidebar_state="collapsed")

# ----------------- CUSTOM CSS -----------------
st.markdown("""
    <style>
        [data-testid="stHeader"] {
        height: 0px !important;
        padding: 0px !important;
        background-color: transparent !important;
        box-shadow: none !important;
        } 
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container { padding-top: 0 !important; margin-top: 0 !important; }
        .main, .block-container {
            padding: 0;
            margin: 0;
        }
        body {
            background-color: black;
            color: white;
        }

        .navbar {
            background-color: black;
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: 'Segoe UI', sans-serif;
        }
        .navbar .logo {
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
        }
        .navbar .start-btn {
            background-color: white;
            padding: 8px 18px;
            border-radius: 8px;
            color: black;
            font-weight: bold;
        }
            .navbar .start-btn:hover {
            background-color: #bebebe;
            cursor: pointer;
            }

        .hero {
            background-color: black;
            padding: 100px 40px;
            text-align: center;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .hero h5{
            color:#a3a3a3;}
        .hero h1 {
            white-space: nowrap; 
            font-size: 3em; 
            text-align: center; 
            color: white;
            margin-bottom: 10px;
            padding:0 20px;
        }
        .features {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 40px;
            font-size: 16px;
        }
        .feature-box {
            background-color: white;
            color: black;
            padding: 10px ;
            font-size: 1em;
            font-weight: 600;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .gradient-body {
            width: 100%;
            padding: 40px 0;
            background-image: linear-gradient(to bottom, #15523e, #000000);
            color: white;
            text-align: center;

        }
        section[data-testid="stFileUploader"] {
            background-color: #1f2937;
            padding: 20px;
            border-radius: 12px;
        }
        section[data-testid="stFileUploader"] * {
            color: white;
        }
        
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
<body>
 <div class="navbar">
    <div class="logo">
        <img src="data:image/png;base64,{logo_base64}" style="height: 30px; vertical-align: middle; margin-right: 10px;">
        <span style="font-size: 24px; font-weight: bold; color: white; vertical-align: middle;">smartify</span>
    </div>
    <div class="start-btn">Get Started</div>
 </div>
<div class="hero">
    <h1>Summarize, analyze and organize your research</h1>
            <h5>With Smartify you can easily summarize any research paper in seconds.</h5>
    <div class="features">
        <div class="feature-box"><b> Summarize anything</b></div>
        <div class="feature-box"><b> Understand complex research</b></div>
        <div class="feature-box"><b> Organize your knowledge </b></div>
    </div>
</div>

</body>
""", unsafe_allow_html=True)

st.markdown("""<div class="gradient-body">
               <h2 style="color: white; font-size: 2em; margin-bottom: 20px;">Upload Your PDF File Below</h2>
            """, unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("", type=["pdf"])

# Close gradient div
st.markdown('</div>', unsafe_allow_html=True)


st.title("AI Research Paper Summarizer")

uploaded_file = st.file_uploader("Upload a PDF research paper", type="pdf")

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    
    # Read the PDF with PyMuPDF
    pdf_reader = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    text = ""
    for page in pdf_reader:
        text += page.get_text()
    
    if text:
        st.subheader("Extracted Text")
        st.write(text)

        if st.button("Summarize Locally"):
            with st.spinner("Summarizing... please wait."):
                chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
                summaries = []
                for chunk in chunks:
                    summary_result = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
                    summaries.append(summary_result[0]['summary_text'])
                final_summary = "\n\n".join(summaries)

                st.subheader("Summary")
                st.write(final_summary)
    else:
        st.error("No text found in PDF!")
