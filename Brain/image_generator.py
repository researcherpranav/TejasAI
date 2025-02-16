import requests
from diffusers import StableDiffusionPipeline
import torch

class ImageGenerator:
    def __init__(self, use_api=False, api_key=None):
        """
        Initialize the image generator.
        :param use_api: If True, use DeepAI API instead of local model
        :param api_key: Required for DeepAI API
        """
        self.use_api = use_api
        self.api_key = api_key

        if not use_api:
            print("🔄 Loading Stable Diffusion model...")
            self.pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to("cuda" if torch.cuda.is_available() else "cpu")
            print("✅ Model loaded successfully!")

    def generate_image(self, command):
        """
        Extracts the prompt from the command and generates an image.
        :param command: Full user command (e.g., "Generate an image of a sunset")
        :return: Image object (PIL format) or Image URL (if using API)
        """
        # Extract prompt (remove "generate an image of" or "generate an image")
        prompt = command.replace("generate an image of", "").replace("generate an image", "").strip()

        if not prompt:
            return "❌ Please provide an image description."

        if self.use_api:
            if not self.api_key:
                raise ValueError("🔴 API Key is required for DeepAI API.")
            
            print(f"🖼️ Generating image via DeepAI API: {prompt}")
            response = requests.post(
                "https://api.deepai.org/api/text2img",
                data={"text": prompt},
                headers={"api-key": self.api_key},
            )
            return response.json().get("output_url", "🔴 Failed to generate image.")

        else:
            print(f"🖌️ Generating image using Stable Diffusion for prompt: {prompt}")
            image = self.pipe(prompt).images[0]
            return image
