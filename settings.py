"""Application Settings."""

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AppSettings(BaseSettings):
    """Settings for the application"""
    
    azure_api_key: str = Field(
        validation_alias="AZURE_OPENAI_KEY",
        description="API-Key for the azure models."
    )
    
    azure_api_version: str = Field(
        default="2025-01-01",
        validation_alias="AZURE_API_VERSION",
        description="API-Version of AzureOpenAI to use."
    )
    
    azure_api_base: str = Field(
        validation_alias="AZURE_OPENAI_BASE",
        description="BASE_URL for azure deployments."
    )
    
    research_model: str = Field(
        default="azure/gpt-4o-mini",
        validation_alias="RESEARCH_MODEL",
        description="Model for research agent."
    )
    
    summary_model: str = Field(
        default="azure/gpt-4o-mini",
        validation_alias="SUMMARY_MODEL", 
        description="Model for summary agent."
    )
    
    html_model: str = Field(
        default="azure/gpt-4o-mini",
        validation_alias="HTML_MODEL",
        description="Model for HTML generation agent."
    )
    
    image_model: str = Field(
        default="azure/dall-e-3",
        validation_alias="IMAGE_MODEL",
        description="Model for image generation agent."
    )
    
    default_temperature: float = Field(
        default=0.7,
        validation_alias="DEFAULT_TEMPERATURE",
        description="Temperature setting for models."
    )
    
    research_temperature: float = Field(
        default=0.7,
        validation_alias="RESEARCH_TEMPERATURE",
        description="Temperature setting for research agent (higher for creativity)."
    )
    
    summary_temperature: float = Field(
        default=0.5,
        validation_alias="SUMMARY_TEMPERATURE",
        description="Temperature setting for summary agent (medium for balanced creativity)."
    )
    
    html_temperature: float = Field(
        default=0.3,
        validation_alias="HTML_TEMPERATURE",
        description="Temperature setting for HTML generation (lower for consistency)."
    )
    
    image_temperature: float = Field(
        default=0.8,
        validation_alias="IMAGE_TEMPERATURE",
        description="Temperature setting for image generation (higher for creativity)."
    )
    
    max_tokens: int = Field(
        default=4000,
        validation_alias="MAX_TOKENS",
        description="Max output tokens"
    )
    
    max_iterations: int = Field(
        default=10,
        validation_alias="MAX_ITERATIONS",
        description="Max iterations for LimitRouter"
    )
    
    output_dir: str = Field(
        default="output",
        validation_alias="OUTPUT_DIR",
        description="Directory for saving generated files (HTML, reports)"
    )
    
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=str(Path(__file__).parent / ".env"),
        env_file_encoding="utf-8",
    )


APP_SETTINGS = AppSettings()
