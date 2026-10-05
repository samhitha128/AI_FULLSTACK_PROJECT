from diffusers import StableDiffusionPipeline
import torch
pipe=StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe=pipe.to("cpu")
print("Success")