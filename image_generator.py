import replicate
import os
os.environ["REPLICATE_API_TOKEN"] = "r8_QDjRm5zsFSCDvP2WKzlbVCNjPiZ0zUW1TjjZM"
api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])


def generate_image(prompt, output_path="generated_image.png"):
    """
    Generates an image based on the given prompt.

    Args:
        prompt (str): The description for the image.
        pipeline (StableDiffusionPipeline): The Stable Diffusion XL pipeline.
        output_path (str): Path to save the generated image.

    Returns:
        str: Path to the saved image.
    
    image = pipeline(prompt, height=512, width=512).images[0]
    image.save(output_path)
    return output_path
    """
    output = api.run(
      "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
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
