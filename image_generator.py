import requests
from PIL import Image
import io


def generate_image(prompt, headers, output_path="generated_image.png"):
    """
    Generates an image based on the given prompt using Hugging Face API.

    Args:
        prompt (str): The description for the image.
        api_url (str): The API endpoint for the Stable Diffusion model.
        headers (dict): Authorization headers for the API.
        output_path (str): Path to save the generated image.

    Returns:
        str: Path to the saved image or an error message if the generation fails.
    """
    # Payload for the API request
    payload = {"inputs": prompt}

    try:
        # API request
        response = requests.post("https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev", headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Read image bytes and save the image
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        image.save(output_path)
        return output_path

    except requests.exceptions.RequestException as e:
        return f"Error generating image: {e}"

    except Exception as e:
        return f"Unexpected error: {e}"
