from diffusers import StableDiffusionPipeline


# Initialize the Stable Diffusion pipeline
def initialize_image_generator():
    """
    Initializes the Stable Diffusion XL pipeline.
    
    Returns:
        StableDiffusionPipeline: The initialized pipeline.
    """
    pipeline = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",safety_checker=StableDiffusionPipeline.default_safety_checker)
    pipeline.to("cpu")  # Use CPU
    return pipeline

def generate_image(prompt, pipeline, output_path="generated_image.png"):
    """
    Generates an image based on the given prompt.

    Args:
        prompt (str): The description for the image.
        pipeline (StableDiffusionPipeline): The Stable Diffusion XL pipeline.
        output_path (str): Path to save the generated image.

    Returns:
        str: Path to the saved image.
    """
    image = pipeline(prompt).images[0]
    image.save(output_path)
    return output_path
