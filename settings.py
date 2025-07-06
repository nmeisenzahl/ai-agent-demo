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
        default="azure/gpt-4.1-mini",
        validation_alias="SUMMARY_MODEL", 
        description="Model for summary agent."
    )
    
    default_temperature: float = Field(
        default=0.7,
        validation_alias="DEFAULT_TEMPERATURE",
        description="Temperature setting for models."
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
    
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=str(Path(__file__).parent / ".env"),
        env_file_encoding="utf-8",
    )


APP_SETTINGS = AppSettings()
