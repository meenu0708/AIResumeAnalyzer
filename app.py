import streamlit as st
from openai import OpenAI
import os
import PyPDF2

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


st.title("AI Resume Analyzer")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job = st.text_area("Paste job description")


def read_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text

if st.button("Analyze"):
    if uploaded_file is None or job == "":
        st.warning("Please fill both fields")
    else:
        with st.spinner("Analyzing..."):
            resume= read_pdf(uploaded_file)
            prompt = f"""
                       You are an expert HR assistant.

                        Analyze the resume against the job description.

                        Return output in this format:

                        Match Score: (in percentage)

                        Give an expert opinion whether I can apply for this job: Yes, you can proceed with this job or No, this don't match you.

                        Skills which match with the job description ?

                        Skills to be removed from the resume which is irrelevant to this job description ?

                        Skills to be added to this resume to match the job description ?

                        Is there any headings or portions to be removed from the resume irrelevant to the job ?

                       Resume:
                       {resume}

                       Job:
                       {job}
                       """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

        st.subheader("Result")
        st.write(result)