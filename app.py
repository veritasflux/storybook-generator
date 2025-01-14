import streamlit as st
from story_generator import generate_story
from image_generator import generate_image
import os

headers = {"Authorization": "Bearer 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"}

# Title
st.title("Personalized Storybook Generator")

# Input Form
with st.form("storybook_form"):
    child_name = st.text_input("Child's Name")
    favorite_animal = st.text_input("Favorite Animal")
    adventure_type = st.text_input("Choose Adventure")
    submit_button = st.form_submit_button("Generate Story")

# Generate and Display Story with Images
if submit_button:
    with st.spinner("Generating your story..."):
        story = generate_story(child_name, favorite_animal, adventure_type)
    st.write("### Your Story")

    # Split the story into paragraphs
    paragraphs = story.split("\n\n")  # Assuming paragraphs are separated by double newlines

    # Generate images for each paragraph
    for idx, paragraph in enumerate(paragraphs):
        if paragraph.strip():  # Ensure the paragraph is not empty
            st.write(paragraph)

            prompt = f"An illustration for: {paragraph}"
            with st.spinner(f"Generating illustration for paragraph {idx + 1}..."):
                try:
                    image_path = generate_image(prompt, headers, output_path=f"generated_image_{idx + 1}.png")
                    st.image(image_path, caption=f"Illustration for paragraph {idx + 1}")
                except Exception as e:
                    st.error(f"Error generating illustration for paragraph {idx + 1}: {e}")
