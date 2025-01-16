import re
from googletrans import Translator

# Initialize Groq client
client = Groq(api_key="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")

def generate_story(name, animal, adventure):
    """
    Generates a children's story using Groq's Llama-3.3-70b-specdec model.
    
    Args:
        name (str): The child's name.
        animal (str): The child's favorite animal.
        adventure (str): The type of adventure.

    Returns:
        str: The generated story.
    """
    # Prepare the story prompt
    system_prompt =     (    f"You are a professional sotryteller.Write a children's story (about 250 words and 4 paragraphs) about {name} who embarks on a {adventure}"
    f"with their favorite animal, a {animal}. The story must have one tricky puzzle or riddle or obstacle or adventure that will be resolved. The story should have a wise end."
    f"generate traits of the {animal} like color, size and the child, boy or a girl, hair color, cloth colors"
    f"Traits text should be positioned at the beginning of the story.Example of Expected output format for the traits "
    "Traits: The animal is a small, golden dog. The child is a boy with short black hair, wearing a blue shirt and red shorts.\n"
    f"For each paragraph, provide a title and an illustration proposal formatted as follows (Do not add special characters before Title or Content or Illustration):\n\n"
    f"Example Expected output format:"
    "Title: Setting Sail\n"
    "Content: Ahmed had always dreamed of going on a sea adventure with his favorite animal, a shark named Finley. One sunny day, he finally got his chance. Ahmed and Finley set sail on a small boat, excited to explore the open waters. The wind was in their hair, and the sun was shining bright as they sailed further and further away from the shore.\n"
     "Illustration: a {animal} sailing alongside a child who is inside a boat.\n"
     f"Second Example Expected output format:"
    "Title: The Mysterious Island\n"
    "Content: As they sailed further and further away from the shore, Ahmed and Bruce stumbled upon a mysterious island. The island was surrounded by rocky cliffs and dense jungle, and Ahmed was eager to explore it. But as they approached the shore, they realized that the only way to reach the island was by solving a tricky puzzle. A sign on the cliff read: 'What can be broken, but never held?'\n"
     "Illustration: a {animal} with a child on the shore reading a sign with multiple rows.\n"
)

    # Call Groq's chat completion
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": ""}
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collect the story output
    story = ""
    for chunk in completion:
        story += chunk.choices[0].delta.content or ""

    return story
    
def parse_story(story):
    """
    Parse the story into titled sections, excluding the Illustration proposals.
    Args:
        story (str): Raw story text with titles, content, and illustration proposals.
    Returns:
        list: A list of tuples, each containing a title and its corresponding content.
    """
    paragraphs = []
    title, content = "", ""  # Initialize title and content as empty strings

    for line in story.split("\n"):
        line = line.strip()  # Remove leading/trailing whitespace
        if line.startswith("Title:"):
            # Append the previous title-content pair if present
            if title and content:
                paragraphs.append((title, content.strip()))
            title = line[len("Title:"):].strip()  # Extract the title
            content = ""  # Reset content for the new section
        elif line.startswith("Content:"):
            # If a new content section starts
            if content:
                content += " "  # Add a space before appending new content
            content += line[len("Content:"):].strip()
        elif line.startswith("Illustration:"):
            # Skip the illustration lines
            continue
        elif title:  # Additional content lines after "Content:"
            content += " " + line.strip()

    # Append the last title-content pair
    if title and content:
        paragraphs.append((title, content.strip()))

    return paragraphs


def extract_traits(story_output):
    traits_start = story_output.find("Traits:")
    traits_end = story_output.find("Title:", traits_start)
    if traits_start != -1 and traits_end != -1:
        traits_text = story_output[traits_start + len("Traits:"):traits_end].strip()
        return traits_text
    return ""

def parse_illustration(story: str):
    """
    Parse the illustration proposals from the generated story.
    
    Args:
        story (str): The full text output of the story with titles, content, and illustration proposals.
    
    Returns:
        List[str]: A list of illustration descriptions for each paragraph.
    """
    illustration_pattern = r"Illustration:\s*(.+)"
    illustrations = re.findall(illustration_pattern, story)
    return illustrations

def translate_text(text, target_language="fr"):
    """
    Translates text to the target language.
    
    Args:
        text (str): The text to translate.
        target_language (str): The target language code (e.g., 'fr' for French).
    
    Returns:
        str: The translated text.
    """
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text
