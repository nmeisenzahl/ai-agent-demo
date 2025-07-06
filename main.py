"""Main application for AI Agent Demo using Flock framework."""

import asyncio
import os
from agents.research_agent import research_agent
from agents.summary_agent import summary_agent
from routers.limit_router import LimitRouter, LimitRouterConfig
from settings import APP_SETTINGS
from flock.core import Flock
from flock.routers.agent.agent_router import AgentRouter, AgentRouterConfig
from flock.core.logging.logging import configure_logging


async def run_research_and_summary(topic: str) -> dict:
    """
    Run the research and summary workflow.
    
    Args:
        topic: The topic to research and summarize
        
    Returns:
        dict: The final result containing research and summary
    """
    # Create the AgentRouter
    agent_router = AgentRouter(
        name="agent_router",
        config=AgentRouterConfig(
            enabled=True,
            with_output=True,
            confidence_threshold=0.75,
        )
    )
    
    # Create the LimitRouter to wrap the AgentRouter
    limit_router = LimitRouter(
        name="limit_router",
        config=LimitRouterConfig(
            enabled=True,
            max_iterations=APP_SETTINGS.max_iterations,
            orchestrator=agent_router,
        )
    )

    # Set up handoff routers for agents
    research_agent.handoff_router = limit_router
    summary_agent.handoff_router = limit_router

    # Create the Flock
    flock = Flock(
        name="research_summary_flock",
        description="A flock for researching topics and creating summaries",
        model=APP_SETTINGS.research_model,  # Default model
        show_flock_banner=True,
        agents=[
            research_agent,
            summary_agent,
        ],
        servers=[],  # No MCP servers for this demo
    )

    # Configure logging to reduce noise
    configure_logging(flock_level="INFO", external_level="WARNING")

    print(f"🔍 Starting research on topic: {topic}")
    print("=" * 60)

    # Run the flock starting with the research agent
    result = await flock.run_async(
        start_agent=research_agent,
        input={
            "topic": topic,
        },
    )

    return result


async def main():
    """Main function to run the AI agent demo."""
    print("🤖 AI Agent Demo using Flock Framework")
    print("=" * 60)
    print("This demo uses two agents:")
    print("1. Research Agent (azure/gpt-4o-mini) - Conducts research")
    print("2. Summary Agent (azure/gpt-4.1-mini) - Creates titles and summaries")
    print("=" * 60)
    
    # Check if environment variables are set
    try:
        APP_SETTINGS.azure_api_key
        APP_SETTINGS.azure_api_base
    except Exception as e:
        print("❌ Error: Missing required environment variables.")
        print("Please set AZURE_API_KEY and AZURE_API_BASE")
        print(f"Error details: {e}")
        return

    # Get topic from user
    topic = input("\n📝 Please enter a topic to research: ")
    
    if not topic.strip():
        print("❌ Error: Topic cannot be empty")
        return

    try:
        # Run the research and summary workflow
        result = await run_research_and_summary(topic.strip())
        
        print("\n" + "=" * 60)
        print("🎉 Research and Summary Complete!")
        print("=" * 60)
        
        if result:
            print("✅ Final result received")
            # The agents will have printed their outputs during execution
        else:
            print("❌ No result received - check the execution logs above")
            
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        print("Please check your environment variables and try again.")


if __name__ == "__main__":
    # Set up Azure OpenAI environment for litellm
    if hasattr(APP_SETTINGS, 'azure_api_key'):
        os.environ["AZURE_API_KEY"] = APP_SETTINGS.azure_api_key
    if hasattr(APP_SETTINGS, 'azure_api_base'):
        os.environ["AZURE_API_BASE"] = APP_SETTINGS.azure_api_base
    if hasattr(APP_SETTINGS, 'azure_api_version'):
        os.environ["AZURE_API_VERSION"] = APP_SETTINGS.azure_api_version
    
    asyncio.run(main())
