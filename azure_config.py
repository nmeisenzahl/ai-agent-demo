"""Azure OpenAI configuration for the agents."""

import dspy
from settings import APP_SETTINGS

def configure_azure_openai():
    """Configure DSPy with Azure OpenAI settings."""
    # Use the research model as the default for DSPy
    lm = dspy.LM(
        APP_SETTINGS.research_model,
        api_key=APP_SETTINGS.azure_api_key,
        api_base=APP_SETTINGS.azure_api_base,
        api_version=APP_SETTINGS.azure_api_version
    )
    dspy.configure(lm=lm)
    return lm

def get_summary_model():
    """Get a configured summary model."""
    return dspy.LM(
        APP_SETTINGS.summary_model,
        api_key=APP_SETTINGS.azure_api_key,
        api_base=APP_SETTINGS.azure_api_base,
        api_version=APP_SETTINGS.azure_api_version
    )

# Configure DSPy globally
configure_azure_openai()
