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
    layout="wide",  # or "wide"
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

openai_4o_model = GPTVISION(api_key=api, parameters={})

data_directory = "data"
os.makedirs(data_directory, exist_ok=True)


def encode_image(image_path):
        with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')


def generate_response(image_url):
    encoded_image = encode_image(image_url)
    prompt1 = f"""
    Analyze the images to identify potential hazards.
    Tag and label the identified hazards within the images for easy reference.
    Based on the identified hazards, recommend appropriate PPE for workers, such as helmets, gloves, safety goggles, and protective clothing.
    Create checklists to ensure all recommended safety Equipments are wore by workers.If any of the mentioned equipments are not wore by worker then mention Only those equipments and their safety measures.
    IF IMAGE IS NOT RELATED TO WORKERS SAFETY OR FACTORY SITE THEN REPLY "Please upload Image related to factory site.This image does not belong to Factory site.
    
    Output Requirements:
        **Analysis:**
            give analysis of image
        **Identified Hazards:**
            give identified hazards
        **Checklist for Safety Equipments:**
            equipment1:❌
            equipment2:✅
        **Recommended Safety Equipments:**
            equipment1: SAFETY measure for equipment1
        **Prioritization of Actions:**
              **\n1 Immediate**
           **\n2 short-term**
           **\n3 long-term**
     """

    safety_measures = openai_4o_model.generate_text(prompt=prompt1, image_url=encoded_image)
    return safety_measures


def main():
    page = st.sidebar.radio("Navigation", ["Home","Factory site 1", "Factory site 2", "Custom"])

    if page == "Home":
        st.markdown("## Welcome to the Worker Safety Recommendation Agent!")
        st.markdown(
            "This advanced image analysis technology helps enhance workplace safety by identifying potential hazards and providing tailored recommendations to ensure a secure working environment.")
        st.markdown(f"""
        **How to get started**
          \n-Upload an image
          \n-Generate customized safety measures for your workplace
        its that easy!
        """)
        st.markdown(f"""
        ****How it works:****
        \n**1. Image Analysis:** Load and examine the image to understand the context.
        \n**2. Identifying Hazards:** Identify and tag potential hazards in the image.Label each identified hazard clearly for reference.
        \n**3. Checklist Creation:** Create a checklist to ensure all recommended safety equipment is worn by workers.If any recommended equipment is missing in the image, list only those items along with their safety measures.
        \n**4. Prioritizing Actions:** Prioritize actions based on the severity and urgency of addressing the hazards.
        """)

    elif page == "Factory site 1":
        image_url = "image1.jpg"
        st.sidebar.image(image_url)
        with st.spinner("Generating Safety Measures...."):
            res = generate_response(image_url)
            st.markdown(res)

    elif page == "Factory site 2":
        image_url = "image2.webp"
        st.sidebar.image(image_url)
        with st.spinner("Generating Safety Measures...."):
            res = generate_response(image_url)
            st.markdown(res)

    elif page == "Custom":
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


