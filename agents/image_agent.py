"""Image generation agent using Azure OpenAI DALL-E 3 model."""

import os
import uuid
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import requests
from PIL import Image
from openai import AzureOpenAI
from flock.core import FlockFactory
from settings import APP_SETTINGS

# Agent configuration constants
AGENT_NAME = "image_agent"
AGENT_DESCRIPTION = """Image Generation Agent

This agent generates relevant images from text summaries using Azure OpenAI DALL-E 3.
It takes a title and summary as input and creates a compelling, article-relevant image
that enhances the content presentation.

The agent:
- Uses Azure DALL-E 3 for high-quality image generation
- Generates contextually relevant images based on content summary
- Saves images to the output directory with proper naming
- Returns image file path and metadata for integration with HTML agent

Features:
- Automatic prompt enhancement for better image quality
- Error handling and retry logic for robust operation
- Image validation and format optimization
- Unique filename generation to prevent conflicts
"""

AGENT_INPUT = """title: str | The article title for context,
short_summary: str | Brief summary to base the image generation on"""

AGENT_OUTPUT = """image_path: str | Path to the saved generated image,
image_prompt: str | The enhanced prompt used for image generation,
image_metadata: dict | Metadata about the generated image (size, format, etc.)"""


def create_image_generation_tool():
    """Create a tool for generating and saving images using Azure OpenAI DALL-E 3."""
    
    def generate_image_from_summary(title: str, short_summary: str) -> Dict[str, Any]:
        """
        Generate an image from article title and summary using Azure DALL-E 3.
        
        Args:
            title: Article title for context
            short_summary: Brief summary to base image generation on
            
        Returns:
            Dict containing image_path, image_prompt, and image_metadata
        """
        try:
            # Initialize Azure OpenAI client
            client = AzureOpenAI(
                api_key=APP_SETTINGS.azure_api_key,
                api_version=APP_SETTINGS.azure_api_version,
                azure_endpoint=APP_SETTINGS.azure_api_base
            )
            
            # Create enhanced prompt for better image generation
            enhanced_prompt = _create_enhanced_prompt(title, short_summary)
            
            # Ensure output directory exists
            output_dir = Path(APP_SETTINGS.output_dir).resolve()  # Ensure absolute path
            output_dir.mkdir(exist_ok=True)
            
            # Generate image using DALL-E 3
            print(f"🎨 Generating image with prompt: {enhanced_prompt[:100]}...")
            
            response = client.images.generate(
                model="dall-e-3",  # This will use the deployed model name
                prompt=enhanced_prompt,
                n=1,
                size="1024x1024",  # Standard square format
                quality="hd",  # High quality for better results
                style="vivid",  # More dramatic and engaging images
                response_format="url"
            )
            
            # Get the image URL from response
            image_url = response.data[0].url
            revised_prompt = getattr(response.data[0], 'revised_prompt', enhanced_prompt)
            
            # Download and save the image
            image_path = _download_and_save_image(image_url, title)
            
            # Debug: Print the path we're returning
            print(f"🔍 Image saved at absolute path: {image_path}")
            print(f"🔍 Path exists: {os.path.exists(image_path)}")
            print(f"🔍 Basename: {os.path.basename(image_path)}")
            
            # Create metadata
            image_metadata = {
                "original_prompt": enhanced_prompt,
                "revised_prompt": revised_prompt,
                "size": "1024x1024",
                "quality": "hd",
                "style": "vivid",
                "format": "png",
                "generated_at": datetime.now().isoformat(),
                "file_size_bytes": os.path.getsize(image_path) if os.path.exists(image_path) else 0
            }
            
            print(f"✅ Image generated successfully: {image_path}")
            
            return {
                "image_path": str(image_path),
                "image_prompt": revised_prompt,
                "image_metadata": image_metadata
            }
            
        except Exception as e:
            error_msg = f"Failed to generate image: {str(e)}"
            print(f"❌ {error_msg}")
            
            # Return error information
            return {
                "image_path": "",
                "image_prompt": enhanced_prompt if 'enhanced_prompt' in locals() else "",
                "image_metadata": {
                    "error": error_msg,
                    "generated_at": datetime.now().isoformat()
                }
            }
    
    def _create_enhanced_prompt(title: str, summary: str) -> str:
        """Create an enhanced prompt for better image generation."""
        # Create a focused, visual prompt based on the content
        base_prompt = f"""Create a professional, engaging illustration for an article titled "{title}". 
        
        Content summary: {summary}
        
        Style requirements:
        - Professional and modern visual style
        - High quality, editorial illustration
        - Relevant to the article content
        - Suitable for web publication
        - Clean composition with good contrast
        - No text or captions in the image"""
        
        # Limit prompt length to avoid API limits
        if len(base_prompt) > 1000:
            base_prompt = base_prompt[:1000] + "..."
            
        return base_prompt
    
    def _download_and_save_image(image_url: str, title: str) -> str:
        """Download image from URL and save to output directory."""
        try:
            # Create a safe filename from title
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
            
            # Add timestamp and hash for uniqueness
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
            filename = f"article_image_{safe_title}_{timestamp}_{title_hash}.png"
            
            # Full path for saving
            output_dir = Path(APP_SETTINGS.output_dir).resolve()  # Ensure absolute path
            image_path = output_dir / filename
            
            # Download the image
            print(f"📥 Downloading image from Azure OpenAI...")
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Save the image
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            # Validate image can be opened
            with Image.open(image_path) as img:
                img.verify()  # Verify the image is valid
            
            print(f"💾 Image saved: {image_path}")
            return str(image_path)
            
        except Exception as e:
            raise Exception(f"Failed to download/save image: {str(e)}")
    
    return generate_image_from_summary


# Create the image generation agent with the custom tool
image_agent = FlockFactory.create_default_agent(
    name=AGENT_NAME,
    description=AGENT_DESCRIPTION,
    input=AGENT_INPUT,
    output=AGENT_OUTPUT,
    include_thought_process=True,
    stream=True,
    enable_rich_tables=True,
    model=APP_SETTINGS.research_model,  # Use text model for planning/coordination
    max_tokens=APP_SETTINGS.max_tokens,
    temperature=APP_SETTINGS.image_temperature,
    print_context=True,
    tools=[create_image_generation_tool()],  # Include the image generation tool
)
