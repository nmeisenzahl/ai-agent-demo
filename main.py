"""Main application for AI Agent Demo using Flock framework."""

import asyncio
import os
from agents.research_agent import research_agent
from agents.summary_agent import summary_agent
from agents.html_agent import html_agent, save_html_article
from routers.limit_router import LimitRouter, LimitRouterConfig
from settings import APP_SETTINGS
from flock.core import Flock
from flock.routers.agent.agent_router import AgentRouter, AgentRouterConfig
from flock.core.logging.logging import configure_logging


async def run_full_workflow(topic: str) -> dict:
    """
    Run the complete workflow: research, summary, and HTML generation.
    
    Args:
        topic: The topic to research and create an HTML article for
        
    Returns:
        dict: The final result containing research, summary, and HTML output
    """
    try:
        # Create the AgentRouter with optimal configuration
        agent_router = AgentRouter(
            name="agent_router",
            config=AgentRouterConfig(
                enabled=True,
                with_output=True,
                confidence_threshold=0.5,  # Balanced threshold for reliable routing
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

        # Set up handoff routers for all agents
        research_agent.handoff_router = limit_router
        summary_agent.handoff_router = limit_router
        html_agent.handoff_router = limit_router

        # Create the Flock with all three agents
        flock = Flock(
            name="full_workflow_flock",
            description="A flock for researching topics, creating summaries, and generating HTML articles",
            model=APP_SETTINGS.research_model,  # Default model
            show_flock_banner=True,
            agents=[
                research_agent,
                summary_agent,
                html_agent,
            ],
            # Re-enabled MCP servers after TaskGroup error was resolved
            servers=[
                {
                    "name": "playwright",
                    "command": "npx",
                    "args": ["-y", "@executeautomation/playwright-mcp-server"],
                    "description": "Playwright browser automation for HTML validation"
                }
            ],
        )

        # Configure logging to reduce noise
        configure_logging(flock_level="INFO", external_level="WARNING")

        print(f"🔍 Starting full workflow for topic: {topic}")
        print("=" * 60)

        print("🔧 Setting up agents and routers...")
        # Set up handoff routers for all agents
        research_agent.handoff_router = limit_router
        summary_agent.handoff_router = limit_router
        html_agent.handoff_router = limit_router
        print("✅ Agent routers configured")

        print("🔧 Creating Flock...")
        # Run the flock starting with the research agent
        result = await flock.run_async(
            start_agent=research_agent,
            input={
                "topic": topic,
            },
        )
        print("✅ Flock execution completed")

        # If we got HTML content, save it to a file with validation
        if result and isinstance(result, dict) and 'html_content' in result:
            try:
                html_content = result['html_content']
                # Generate filename from the topic
                filename = f"{topic.replace(' ', '_').lower()}_article.html"
                
                # Save with Playwright validation enabled
                saved_path = save_html_article(html_content, filename, validate=True)
                result['saved_html_path'] = saved_path
                
                print(f"\n📄 HTML article saved to: {saved_path}")
                print(f"🔍 Playwright validation: ✅ Enabled")
                
            except Exception as e:
                print(f"⚠️  Warning: Could not save HTML file: {e}")

        return result
        
    except Exception as e:
        print(f"❌ Error in run_full_workflow: {e}")
        import traceback
        traceback.print_exc()
        raise


async def main():
    """Main function to run the AI agent demo."""
    print("🤖 AI Agent Demo using Flock Framework")
    print("=" * 60)
    print("This demo uses three agents:")
    print("1. Research Agent (azure/gpt-4o-mini) - Conducts research")
    print("2. Summary Agent (azure/gpt-4.1-mini) - Creates titles and summaries")
    print("3. HTML Agent (azure/gpt-4o-mini) - Generates newspaper-style HTML articles")
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
        # Run the complete workflow
        result = await run_full_workflow(topic.strip())
        
        print("\n" + "=" * 60)
        print("🎉 Full Workflow Complete!")
        print("=" * 60)
        
        if result:
            print("✅ Final result received")
            if 'saved_html_path' in result:
                print(f"📄 HTML article created: {result['saved_html_path']}")
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
