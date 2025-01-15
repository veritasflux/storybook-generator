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
    system_prompt =     (    f"Write a children's story (about 250 words) about {name} who embarks on a {adventure} "
    f"with their favorite animal, a {animal}. For each paragraph, provide a title formatted as follows:\n\n"
    "Title: Title of the Paragraph\n"
    "Content: Paragraph text goes here.\n")

    # Call Groq's chat completion
    completion = client.chat.completions.create(
        model="gemma2-9b-it",
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
    """Parse the story into titled sections."""
    paragraphs = []
    title = None

    for line in story.split("\n"):
        if line.startswith("Title:"):
            # Save any incomplete content before moving to the next title
            if title and content:
                paragraphs.append((title, content))
            title = line.replace("Title:", "").strip()
            content = ""  # Reset content for the new title
        elif line.startswith("Content:"):
            content = line.replace("Content:", "").strip()
        elif title:  # Handle lines that belong to content
            content += " " + line.strip()

    # Add the last parsed paragraph
    if title and content:
        paragraphs.append((title, content))

    return paragraphs
