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
    st.write("### Raw Story Output")
    st.code(story)  # Display raw output for debugging
    # Split the story into sections
    sections = story.split("---")
    for i in range(0, len(sections) - 1, 2):  # Titles and paragraphs alternate
        title = sections[i].strip().replace("###", "").strip()
        paragraph = sections[i + 1].strip()

        if title and paragraph:
            st.write(f"#### {title}")
            st.write(paragraph)

            # Generate illustration for the paragraph
            prompt = f"An illustration for: {paragraph}"
            with st.spinner(f"Generating illustration for '{title}'..."):
                try:
                    image_path = generate_image(prompt, headers, output_path=f"generated_image_{i // 2 + 1}.png")
                    st.image(image_path, caption=f"Illustration for '{title}'")
                except Exception as e:
                    st.error(f"Error generating illustration for '{title}': {e}")
