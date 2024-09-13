import streamlit as st
import numpy as np
from utils import *
import tempfile
import os
import cv2

def sidebar_navigation():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Leaf Disease Analyzer", "Crop Recommender"])
    return page

def leaf_disease_analyzer():

    format_project()
    intro()
    uploaded_file = st.file_uploader("📤 Upload a leaf image (JPEG/PNG)...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.subheader("📊 Visual and Analytical Report")
        col1, col2 = st.columns([1, 1])

        button = st.button("🔍 Analyze Leaf")

        with col1:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            display_uploaded_image(uploaded_file)

        if button:
            with col2:
                with st.spinner("Analyzing image..."):
                    model_path = "models/model.pt"
                    annotated_image = inference(model_path, tmp_file_path)
                    annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                    st.image(annotated_image_rgb, caption="Inference Output with Bounding Boxes", use_column_width=True)

            with st.spinner("Generating detailed analysis..."):
                prompt = build_prompt()
                response = generate_gemini_response(prompt, tmp_file_path)
                with st.expander("📋 **Click here to see the Detailed Analysis Report**", expanded=True):
                    st.markdown(response)

        os.unlink(tmp_file_path)
    else:
        st.info("Upload an image to start the analysis.")

    st.markdown("""
        ---
        **Disclaimer:** The information provided is based on expert plant pathology analysis. 
        Please consult with agricultural experts before implementing any treatments or strategies.
    """)

def crop_recommender():

    st.title("🌱 CROP RECOMMENDATION")
    st.write("Input your sensor data to find the optimal crops for your conditions.")

    season = st.text_input("Enter the Season", placeholder="e.g., 'summer'")

    input_method = st.radio("Choose input method:", ("Manual Input", "Array/List Input"))

    if input_method == "Manual Input":
        nitrogen = st.number_input("Nitrogen", min_value=0, max_value=100, value=50)
        phosphorus = st.number_input("Phosphorus", min_value=0, max_value=100, value=50)
        potassium = st.number_input("Potassium", min_value=0, max_value=100, value=50)
        temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0)
        soil_fertility = st.selectbox("Soil Fertility", ["Low", "Medium", "High"], index=1)
        moisture = st.number_input("Moisture (%)", min_value=0.0, max_value=100.0, value=60.0)

        sensor_data = [nitrogen, phosphorus, potassium, temperature, soil_fertility, moisture]
    else:
        sensor_input = st.text_input("Enter sensor data as a comma-separated list or numpy array (nitrogen, phosphorus, potassium, temperature, soil_fertility, moisture):")
        try:
            sensor_data = eval(sensor_input)
            if isinstance(sensor_data, (list, np.ndarray)) and len(sensor_data) == 6:
                st.success("Sensor data successfully parsed!")
            else:
                st.error("Invalid input. Please provide 6 values in the correct order.")
                return
        except:
            st.error("Invalid input. Please check your format and try again.")
            return

    if st.button("🌾 Find Optimal Crops"):
        with st.spinner("Finding the best crops for your conditions..."):
            formatted_data = format_sensor_data(sensor_data)
            prompt = f"""
            You are an agricultural expert in India. Based on the following detailed soil and environmental sensor data, recommend crops that are most suitable for cultivation in this region. 
            {formatted_data}
            The season is {season} in India.
            Consider the specific growing conditions in India, and provide a list of crops that will produce high yields with minimal maintenance during the current season. Be certain and specific in your recommendations based on the sensor data provided, and ensure that the crops suggested are well-suited for Indian agriculture.
            Your response should not be ambiguous. Do not say things like 'I am not sure' or 'I cannot be certain'. Instead, provide clear, confident recommendations for the best crops to grow in these conditions.
            """
            response = generate_crop_recommendation(prompt)
            st.success("Optimal crops found!")
            st.markdown(response)


def main():
    format_project()
    page = sidebar_navigation()

    if page == "Leaf Disease Analyzer":
        leaf_disease_analyzer()
    elif page == "Crop Recommender":
        crop_recommender()
    
    outro()

if __name__ == '__main__':
    main()
