from gptvision import GPTVISION
import streamlit as st
from PIL import Image
import utils
import base64
import os
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Worker Safety Recommendation Agent",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Worker Safety Recommendation Agent👷‍")
st.sidebar.markdown("## Welcome to the Worker Safety Recommendation Agent!")
st.sidebar.markdown("This advanced image analysis technology helps enhance workplace safety by identifying potential hazards and providing tailored recommendations to ensure a secure working environment.")
st.sidebar.markdown(f"""
**How to get started**
  \n-Upload an image
  \n-Generate customized safety measures for your workplace
its that easy!
""")

openai_4o_model = GPTVISION(api_key=api, parameters={})

data_directory = "data"
os.makedirs(data_directory, exist_ok=True)


def encode_image(image_path):
        with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')


def generate_response(image_url):
    encoded_image = encode_image(image_url)
    prompt = f"""
    Please analyze the uploaded image of our factory site. Identify and highlight potential safety hazards based on Industrial Safety Regulations(Occupational Safety and Health Administration (OSHA) standards) such as unguarded machinery, tripping hazards, missing safety signs, and workers not using PPE. 
    Provide a detailed report suggesting specific safety measures to mitigate each identified risk. 
    Ensure the suggestions comply with current industrial safety regulations and prioritize actions based on the severity of the hazards.

    Output Requirements:
    1/ Potential Safety Hazards
    2/ Detailed Safety Measures
    3/ Prioritization of Actions
           1/ Immediate
           2/ short-term
           3/ long-term

    IF IMAGE IS NOT RELATED TO WORKERS SAFETY OR FACTORY SITE THEN REPLY "Please upload Image related to factory site.This image does not belong to Factory site."""

    safety_measures = openai_4o_model.generate_text(prompt=prompt, image_url=encoded_image)
    return safety_measures


def main():
    page = st.sidebar.radio("Navigation", ["Default", "Custom"])

    if page == "Default":
        image_url = "demo.webp"
        st.sidebar.image(image_url)
        with st.spinner("Generating Safety Measures...."):
            res = generate_response(image_url)
            st.markdown(res)

    if page == "Custom":
        uploaded_files = st.file_uploader("Upload Factory Site Image", type=['png', 'jpg','webp'])
        if uploaded_files is not None:
            st.success(f"File uploaded: {uploaded_files.name}")
            file_path = utils.save_uploaded_file(uploaded_files)
            if file_path is not None:
                st.sidebar.image(file_path)
                if st.button("Generate"):
                    with st.spinner("Generating Safety Measures...."):
                        res = generate_response(file_path)
                        st.markdown(res)

if __name__ == "__main__":
    main()


