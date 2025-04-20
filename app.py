# Job Search Copilot - Full Automation Extension

import streamlit as st
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import tempfile
import os

openai_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
serpapi_key = st.text_input("🔍 Enter your SerpAPI Key", type="password")

if openai_key and serpapi_key:
    os.environ["OPENAI_API_KEY"] = openai_key
    os.environ["SERPAPI_API_KEY"] = serpapi_key
else:
    st.warning("Please enter both API keys to continue.")
    st.stop()
# Check if API keys are set

# Initialize LLM and Search Tool
llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")
search = SerpAPIWrapper()

# Tools for the Agent
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Search the internet for latest job listings."
    )
]

# Initialize Agent with error handling
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True  # retry on LLM output format errors
)

# Streamlit UI
st.title("🤖 Job Search Copilot")
st.write("Find and tailor job applications using AI")

job_title = st.text_input("Enter Job Title")
location = st.text_input("Enter Location")
skills = st.text_area("List Your Key Skills")
uploaded_resume = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])
resume_text = ""
job_results = ""

if uploaded_resume:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_resume.read())
        loader = PyPDFLoader(tmp_file.name)
        pages = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(pages)
        resume_text = " ".join([doc.page_content for doc in texts])
        st.success("📄 Resume parsed successfully!")

if st.button("Find Jobs"):
    if job_title and location:
        with st.spinner("Searching for relevant jobs..."):
            query = f"{job_title} jobs in {location}"
            job_results = agent.run(query)
            st.success("Here are some job listings:")
            st.write(job_results)
    else:
        st.warning("Please enter both job title and location.")

# Cover Letter Generator
st.markdown("---")
st.subheader("📝 AI Cover Letter Generator")

if resume_text and skills and job_title:
    cover_prompt = PromptTemplate(
        input_variables=["resume", "skills", "job"],
        template="""
        Based on the resume: {resume}, skills: {skills}, and job title: {job}, write a professional and tailored cover letter.
        Make it enthusiastic and highlight why the applicant is a good fit.
        """
    )
    cover_chain = LLMChain(llm=llm, prompt=cover_prompt)
    cover_letter = cover_chain.run(resume=resume_text[:2000], skills=skills, job=job_title)
    st.markdown("### 📄 Your Cover Letter")
    st.write(cover_letter)
else:
    st.info("Upload your resume and fill in your skills and job title to generate a cover letter.")

# Resume Updater
st.markdown("---")
st.subheader("📌 Resume Enhancer")

if resume_text and job_results:
    update_prompt = PromptTemplate(
        input_variables=["resume", "jobdesc"],
        template="""
        Here is a resume:
        {resume}

        Improve and tailor this resume based on the following job description:
        {jobdesc}

        Highlight matching skills and experience.
        Return only the updated resume text.
        """
    )
    update_chain = LLMChain(llm=llm, prompt=update_prompt)
    updated_resume = update_chain.run(resume=resume_text[:2000], jobdesc=job_results[:2000])
    st.markdown("### 🆕 Updated Resume")
    st.write(updated_resume)
    st.download_button("Download Updated Resume", updated_resume, file_name="updated_resume.txt")
else:
    st.info("Search for a job and upload your resume to enable resume enhancement.")

# Simulated Job Application
st.markdown("---")
st.subheader("🚀 Simulated Job Application")

if job_results and cover_letter and updated_resume:
    st.markdown("""
    ### ✅ Ready to Apply!
    Here’s a summary you can use to apply:
    """)
    st.write("**Job Link (search result based):**")
    st.write(job_results.split("\n")[0])
    st.markdown("---")
    st.write("**Prefilled Application Summary:**")
    st.write(f"**Cover Letter:**\n{cover_letter}")
    st.write(f"**Updated Resume:**\n{updated_resume[:1000]}...")
    st.success("Application data prepared. Copy and paste this into the job site to apply.")
else:
    st.info("Once you generate a cover letter and resume, we’ll simulate the application process.")
