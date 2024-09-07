import google.generativeai as genai
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

def set_model():
    """Configure the Generative AI model using the Gemini API."""
    genai.configure(api_key='AIzaSyDIRz_Nrocg0F-QVVIfJOI-qrJlcU7iQq8')

    generation_config = {
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
    }

    safety_settings = [
        {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    return model

def read_image_data(file_path):
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Could not find image: {image_path}")
    return {"mime_type": "image/jpeg", "data": image_path.read_bytes()}

def generate_gemini_response(prompt, image_path, sensor_data=None):
    """Generate a response from the Gemini API based on the prompt and image."""
    model = set_model()
    image_data = read_image_data(image_path)
    if sensor_data is not None:
        prompt += f"\nSensor Data: {sensor_data}"
    response = model.generate_content([prompt, image_data])
    return response.text

def build_prompt():
    """Build the prompt for the generative AI model."""
    return """
You are a highly skilled plant pathologist specializing in the diagnosis and treatment of plant diseases. Your task is to analyze the provided data, which includes an image of a plant and sensor readings, to identify any diseases, infestations, or other issues. Structure your response as follows:

1. **Disease Identification**: Analyze the provided image and sensor data to detect any diseases, pests, or deficiencies.
2. **Detailed Findings**: Provide in-depth findings on the identified issues, including possible causes and severity.
3. **Recommended Actions**: Suggest effective treatment options, preventive measures, and further actions.
4. **Preventive Measures**: Offer recommendations to prevent recurrence.
5. **Expert Recommendations**: Provide long-term health and disease management strategies.

If the condition is unrecognizable, say "I don't know". If the image is not plant-related, respond with "Please upload a valid plant image."
"""

def generate_crop_recommendation(prompt):
    model = set_model()
    response = model.generate_content(prompt)
    return response.text


