from diffusers import DiffusionPipeline


def generate_image(prompt, api, output_path="generated_image.png"):
    """
    Generates an image based on the given prompt.

    Args:
        prompt (str): The description for the image.
        pipeline (StableDiffusionPipeline): The Stable Diffusion XL pipeline.
        output_path (str): Path to save the generated image.

    Returns:
        str: Path to the saved image.
    """
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0")
    image = pipe(prompt).images[0]
    image = pipeline(prompt, height=512, width=512).images[0]
    image.save(output_path)
    return output_path
    """
    output = api.run(
      "black-forest-labs/flux-1.1-pro-ultra",
      input={
        "width": 1024,
        "height": 1024,
        "prompt": prompt,
        "refine": "expert_ensemble_refiner",
        "num_outputs": 1,
        "apply_watermark": False,
        "negative_prompt": "low quality, worst quality",
        "num_inference_steps": 25
       }
     )
    output.save(output_path)
    return output_path
"""
