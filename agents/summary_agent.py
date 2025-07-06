"""Summary agent that creates titles and summaries from research content."""

from flock.core import FlockFactory
from settings import APP_SETTINGS

# Agent configuration constants
AGENT_NAME = "summary_agent"
AGENT_DESCRIPTION = """Summary Agent

This agent creates concise titles and summaries from research content.
It takes detailed research content and key points as input and produces
a compelling title and a short, digestible summary.

The agent uses Azure OpenAI gpt-4o-mini model for high-quality summarization.
"""

AGENT_INPUT = """research_content: str | The detailed research content to summarize,
key_points: list[str] | Main points from the research"""

AGENT_OUTPUT = """title: str | A compelling and descriptive title for the research,
short_summary: str | A concise summary of the main findings (2-3 sentences)"""

# Create the summary agent
summary_agent = FlockFactory.create_default_agent(
    name=AGENT_NAME,
    description=AGENT_DESCRIPTION,
    input=AGENT_INPUT,
    output=AGENT_OUTPUT,
    include_thought_process=True,
    stream=True,
    enable_rich_tables=True,
    model=APP_SETTINGS.summary_model,
    max_tokens=APP_SETTINGS.max_tokens,
    temperature=APP_SETTINGS.summary_temperature,
    print_context=True,
    tools=[],  # No tools needed for summarization
)
