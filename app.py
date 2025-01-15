import streamlit as st
from story_generator import generate_story, parse_story
from image_generator import generate_image
import os
import time

headers = {"Authorization": "Bearer " os.getenv(HUGGING_API_TOKEN)"}

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
        if not story.strip():
            st.error("Failed to generate the story. Please try again.")
        else:
            # Parse the story into titled paragraphs
            paragraphs = parse_story(story)
            st.write("### Your Story")
            st.text(story)
            st.write(paragraphs) #Debug

            for title, paragraph in paragraphs:
                st.write(f"#### {title}")
                st.write(paragraph)

                # Generate an image for this paragraph
                prompt = (f"generate an illustration, in a colorful, cartoonish style with soft lighting and cheerful expressions, of a child name {child_name} and his favourite animal {favorite_animal} based on this paragrah : {title}: {paragraph}.")
                with st.spinner(f"Generating an illustration for: {title}"):
                    try:
                        time.sleep(2)
                        image_path = generate_image(prompt, headers)
                        st.image(image_path, caption=title)
                    except Exception as e:
                        st.error(f"Error generating illustration for {title}: {e}")
