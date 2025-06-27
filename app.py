import streamlit as st
import fitz
from transformers import pipeline

summarizer = pipeline(
    "summarization", 
    model="facebook/bart-large-cnn", 
    device=-1
)


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
