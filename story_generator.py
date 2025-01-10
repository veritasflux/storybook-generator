from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.environ.get("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"),)

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
    system_prompt = f"Write a children's story about {name} who embarks on a {adventure} with their favorite animal, a {animal}."

    # Call Groq's chat completion
    completion = client.chat.completions.create(
        model="llama-3.3-70b-specdec",
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
