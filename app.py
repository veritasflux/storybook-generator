import streamlit as st
from story_generator import generate_story
from image_generator import generate_image

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
    image_path = generate_image(story)
    st.image(image_path, caption="Story Illustration")

