import streamlit as st
from story_generator import generate_story, parse_story, extract_traits, parse_illustration, translate_text
from image_generator import generate_image
import os
import time
import asyncio


# Headers for the API authorization
headers = {"Authorization": "Bearer " + os.getenv("HUGGING_API_TOKEN")}

# Title
st.title("Personalized Storybook Generator")

# Input Form
with st.form("storybook_form"):
    child_name = st.text_input("Child's Name")
    favorite_animal = st.text_input("Favorite Animal")
    adventure_type = st.text_input("Choose Adventure")
    target_language = st.selectbox("Translate Story To", ["None", "French", "Spanish", "Arabic"])
    submit_button = st.form_submit_button("Generate Story")

# Function to handle the translation
async def translate_paragraphs(paragraphs, lang_code):
    translated_paragraphs = []
    for title, paragraph in paragraphs:
        translated_title = await translate_text(title, lang_code)
        st.write(translated_title)
        translated_paragraph = await translate_text(paragraph, lang_code)
        translated_paragraphs.append((translated_title, translated_paragraph))
    return translated_paragraphs

# Generate and Display Story with Images
if submit_button:
    with st.spinner("Generating your story..."):
        story = generate_story(child_name, favorite_animal, adventure_type)
        if not story.strip():
            st.error("Failed to generate the story. Please try again.")
        else:
            # Parse the story into titled paragraphs
            paragraphs = parse_story(story)  # Titles and content (without illustrations)
            traits = extract_traits(story)
            illustrations = parse_illustration(story)
            
            st.write("### Your Story")
            
            if len(illustrations) != len(paragraphs):
                st.error("Mismatch between story paragraphs and illustrations.")
            else:
                # Handle translation if needed
                if target_language != "None":
                    lang_code = {"French": "fr", "Spanish": "es", "Arabic": "ar"}[target_language]
                    translated_paragraphs = asyncio.run(translate_paragraphs(paragraphs, lang_code))
                    st.write(lang_code)
                else:
                    translated_paragraphs = paragraphs

                for i, (title, paragraph) in enumerate(translated_paragraphs):
                    # Display title and content
                    st.write(f"#### {title}")
                    st.write(paragraph)

                    # Generate and display an image
                    illustration_description = illustrations[i]
                    prompt = (
                        f"{animal} and child {name} are the main characters, {traits}. {illustration_description}. "
                        f"Depict this in a colorful and vibrant children's storybook style."
                    )

                    with st.spinner(f"Generating an illustration for: {title}"):

                        try:
                            time.sleep(4)  # Adjust delay as needed
                            image_path = generate_image(prompt, headers)
                            st.image(image_path, caption=title)
                        except Exception as e:
                            st.error(f"Error generating illustration for {title}: {e}")
