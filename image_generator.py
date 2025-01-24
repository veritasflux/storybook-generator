import requests
from PIL import Image
import io
import time


def generate_image(prompt, headers, output_path="generated_image.png", max_retries=5):
    """
    Generates an image based on the given prompt using Hugging Face API with 429 error handling.

    Args:
        prompt (str): The description for the image.
        headers (dict): Authorization headers for the API.
        output_path (str): Path to save the generated image.
        max_retries (int): Maximum number of retries for rate-limiting errors.

    Returns:
        str: Path to the saved image or an error message if the generation fails.
    """
    # API endpoint
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"

    # Payload for the API request
    payload = {"inputs": prompt}
   
    # Retry mechanism
    retries = 0
    while retries < max_retries:
        try:
            # API request
            response = requests.post(api_url, headers=headers, json=payload)

            if response.status_code != 200:
                # Too Many Requests: wait and retry
                retry_after = int(response.headers.get("Retry-After", 5))  # Use Retry-After header if available
                print(f"Rate limit reached. Retrying in {retry_after} seconds...")
                time.sleep(retry_after)
                retries += 1
                continue

            # Raise other HTTP errors
            response.raise_for_status()

            # Read image bytes and save the image
            image_bytes = response.content
            image = Image.open(io.BytesIO(image_bytes))
            image.save(output_path)
            return output_path

        except requests.exceptions.RequestException as e:
            if retries >= max_retries - 1:
                return f"Error generating image after {max_retries} retries: {e}"
            print(f"Error occurred: {e}. Retrying in 5 seconds...")
            time.sleep(5)  # General retry delay
            retries += 1

        except Exception as e:
            return f"Unexpected error: {e}"

    return "Failed to generate image after maximum retries."
