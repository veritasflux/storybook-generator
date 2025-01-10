from diffusers import DiffusionPipeline

access_token = "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"

# Load the FLUX model
def initialize_image_generator():
    """
    Initializes the FLUX.1-dev image generation pipeline.
    
    Returns:
        DiffusionPipeline: The initialized pipeline.
    """
    pipeline = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-dev",token=access_token)
    pipeline.to("cuda")  # Use GPU for faster generation
    return pipeline

def generate_image(prompt, pipeline, output_path="generated_image.png"):
    """
    Generates an image based on the given prompt.

    Args:
        prompt (str): The description for the image.
        pipeline (DiffusionPipeline): The FLUX image generation pipeline.
        output_path (str): Path to save the generated image.

    Returns:
        str: Path to the saved image.
    """
    image = pipeline(prompt).images[0]
    image.save(output_path)
    return output_path
