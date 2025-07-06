"""Research agent that conducts research on provided topics."""

from flock.core import FlockFactory
from settings import APP_SETTINGS
# Import to ensure Azure OpenAI is configured
import azure_config

AGENT_NAME = "research_agent"
AGENT_DESCRIPTION = """Research Agent

This agent conducts comprehensive research on any given topic.
It takes a topic as input and provides detailed research content
including key points, findings, and relevant information about the subject.

The agent uses Azure OpenAI gpt-4o-mini model for efficient research generation.
"""

AGENT_INPUT = """topic: str | The topic to research and analyze"""

AGENT_OUTPUT = """research_content: str | Detailed research findings and analysis on the topic,
key_points: list[str] | Main points and findings from the research"""

research_agent = FlockFactory.create_default_agent(
    name=AGENT_NAME,
    description=AGENT_DESCRIPTION,
    input=AGENT_INPUT,
    output=AGENT_OUTPUT,
    include_thought_process=True,
    stream=True,
    enable_rich_tables=True,
    model=APP_SETTINGS.research_model,  # Use string model name
    max_tokens=APP_SETTINGS.max_tokens,
    temperature=APP_SETTINGS.default_temperature,
    print_context=True,
    tools=[],  # No tools needed for basic research
)
