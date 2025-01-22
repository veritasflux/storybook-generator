import re
from googletrans import Translator
from groq import Groq

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
    system_prompt =      (
    f"You are a professional storyteller. Write a charming and imaginative story (600 words and 4 paragraphs) for children aged 5-10. The main character is a child named {name} who embarks on a {adventure} with their favorite animal, a {animal}. "
    f"1 - Begin with a magical or whimsical setting that sparks wonder (e.g., an enchanted forest, a colorful meadow, or a bustling seaside town). Use sensory details (sights, sounds, smells) to create vivid imagery. "
    f"2 - Adventure and Twist: Introduce a surprising twist or challenge that {name} and the {animal} must face together, such as solving a tricky riddle, navigating a mysterious maze, or helping someone in need. Include facts about the setting or abilities of {animal} to educate while entertaining . Add gentle suspense to keep readers captivated.  "
    f"3 - Dialogue and Emotional Depth: Incorporate playful or emotional dialogue between {name} and the {animal} to highlight their bond and personalities. Show how the characters use teamwork, kindness, or bravery to overcome the challenge. "
    f"4 - Resolution and Positive Theme: Resolve the twist with clever teamwork or kindness, and conclude with a heartwarming, inspiring ending that emphasizes values like friendship, courage, or helping others. Reflect briefly on what {name} and the {animal} learned from their adventure. "
    f"Generate traits of the {animal} like color, size, and the child (boy or girl, hair color, and clothing colors). Include the traits text at the beginning of the story. Example format: "
    "Traits: The animal is a small, golden dog. The child is a boy with short black hair, wearing a blue shirt and red shorts.\n"
    f"For each paragraph, provide a title and an illustration proposal formatted as follows (Do not add special characters before Title, Content, or Illustration).\n\n"
    f"For the illustration, do not mention any style of image, just keywords of the characters (boy or a girl, clothes, smiling, surprised, crying ...) and then describe the environment. Do not include many characters "
    f"Example Expected output format:"
    "Title: Setting Sail\n"
    "Content: Ahmed had always dreamed of going on a sea adventure with his favorite animal, a shark named Finley. One sunny day, he finally got his chance. Ahmed and Finley set sail on a small boat, excited to explore the open waters. The wind was in their hair, and the sun was shining bright as they sailed further and further away from the shore.\n"
    "Illustration: boy smiling with short black hair, wearing a bright yellow shirt, blue shorts and white shoes. Turquoise Raptor sitting on a boat. Calm sea, beautiful sunny sky, fluffy white clouds. Island in the background, towers rising out of the sea.\n"
    f"Second Example Expected output format:"
    "Title: The Mysterious Island\n"
    "Content: As they sailed further and further away from the shore, Ahmed and Bruce stumbled upon a mysterious island. The island was surrounded by rocky cliffs and dense jungle, and Ahmed was eager to explore it. But as they approached the shore, they realized that the only way to reach the island was by solving a tricky puzzle. A sign on the cliff read: 'What can be broken, but never held?'\n"
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

async def translate_text(text, lang_code):
    """
    Translates the given text into the specified language.
    
    Args:
        text (str): The text to translate.
        lang_code (str): The language code to translate the text into.
    
    Returns:
        str: The translated text.
    """
    async with Translator() as translator:
        translated = await translator.translate(text, dest=lang_code)
        return translated.text
