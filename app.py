from gptvision import GPTVISION
import streamlit as st
from PIL import Image
import utils
import base64
import os

st.set_page_config(
    page_title="Worker Safety Monitering",
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
st.title("Worker Safety Monitering👷‍")
st.sidebar.markdown("## Welcome to the Worker Safety Monitering!")
st.sidebar.markdown("In this App you need to Upload Your Factory Site image and It can Analyze Your Image and Generate Safety Measures for Your Workers.")

api = st.sidebar.text_input("Enter Your OPENAI API KEY HERE",type="password")

if api:
        openai_4o_model = GPTVISION(api_key=api,parameters={})
else:
        st.sidebar.error("Please Enter Your OPENAI API KEY")

data_directory = "data"
os.makedirs(data_directory, exist_ok=True)


def encode_image(image_path):
        with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')


uploaded_files = st.file_uploader("Upload Your Construction Map", type=['png', 'jpg'])
prompt = f"""
Please analyze the uploaded image of our factory site. Identify and highlight potential safety hazards such as unguarded machinery, tripping hazards, missing safety signs, and workers not using PPE. 
Provide a detailed report suggesting specific safety measures to mitigate each identified risk. 
Ensure the suggestions comply with current industrial safety regulations and prioritize actions based on the severity of the hazards.

IF IMAGE IS NOT RELATED TO WORKERS SAFETY OR FACTORY SITE THEN REPLY "Please upload Image related to factory site.This image does not belong to Factory site."""
if uploaded_files is not None:
        st.success(f"File uploaded: {uploaded_files.name}")
        file_path = utils.save_uploaded_file(uploaded_files)
        if file_path is not None:
            st.sidebar.image(file_path)
            if st.button("Generate"):
                encoded_image = encode_image(file_path)
                planning = openai_4o_model.generate_text(prompt=prompt, image_url=encoded_image)
                st.markdown(planning)



