import streamlit as st
from story_generator import generate_story
from image_generator import generate_image
import torch
import replicate
import os

api = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

# Title
st.title("Personalized Storybook Generator")

# Input Form
with st.form("storybook_form"):
    child_name = st.text_input("Child's Name")
    favorite_animal = st.text_input("Favorite Animal")
    adventure_type = st.selectbox(
        "Choose an Adventure", 
        ["Space Journey", "Forest Quest", "Pirate Adventure"]
    )
    submit_button = st.form_submit_button("Generate Story")

# Generate and Display Story
if submit_button:
    with st.spinner("Generating your story..."):
        story = generate_story(child_name, favorite_animal, adventure_type)
    st.write("### Your Story")
    st.write(story)

    # Generate Illustration
    prompt = f"{adventure_type} with a {favorite_animal} for a children's story"
    with st.spinner("Generating an illustration..."):
        try:
            image_path = generate_image(prompt, api)
            st.image(image_path, caption="Generated Illustration")
        except Exception as e:
            st.error(f"Error generating illustration: {e}")

