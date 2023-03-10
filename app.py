import os
import torch
import base64
from io import BytesIO
from transformers import pipeline
from diffusers import StableDiffusionPipeline


# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"
def init():
    global model

    model_name = os.getenv("MODEL_NAME")
    model = StableDiffusionPipeline.from_pretrained(
        model_name, safety_checker=None).to("cuda")


# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs: dict) -> dict:
    global model

    # Parse out your arguments
    prompt = model_inputs.pop('prompt', None)
    if prompt is None:
        return {'message': "No prompt provided"}

    # Run the model
    result = model(prompt, **model_inputs)

    # Check if result is an image or text
    image = result.images[0]
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Return the results as a dictionary
    return {'image_base64': image_base64}
