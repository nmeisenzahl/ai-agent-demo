"""Demo script showing how to use the AI agents."""

import asyncio
import os
from agents.research_agent import research_agent
from agents.summary_agent import summary_agent
from routers.limit_router import LimitRouter, LimitRouterConfig
from settings import APP_SETTINGS
from flock.core import Flock
from flock.routers.agent.agent_router import AgentRouter, AgentRouterConfig


async def demo_simple_usage():
    """Demonstrate simple usage of individual agents."""
    print("🔬 Demo: Simple Agent Usage")
    print("-" * 40)
    
    # Demo research agent
    print("1. Testing Research Agent:")
    research_result = await research_agent.run_async({
        "topic": "Weather in Germany the last 10 years"
    })
    print(f"Research completed: {bool(research_result)}")
    
    # Demo summary agent using research results
    if research_result and 'research_content' in research_result:
        print("\n2. Testing Summary Agent:")
        summary_result = await summary_agent.run_async({
            "research_content": research_result.get('research_content', ''),
            "key_points": research_result.get('key_points', []),
            "sources_mentioned": research_result.get('sources_mentioned', [])
        })
        print(f"Summary completed: {bool(summary_result)}")


async def demo_with_routers():
    """Demonstrate usage with AgentRouter and LimitRouter."""
    print("\n🤖 Demo: Agents with Routers")
    print("-" * 40)
    
    # Create routers
    agent_router = AgentRouter(
        name="demo_agent_router",
        config=AgentRouterConfig(
            enabled=True,
            with_output=True,
            confidence_threshold=0.75,
        )
    )
    
    limit_router = LimitRouter(
        name="demo_limit_router",
        config=LimitRouterConfig(
            enabled=True,
            max_iterations=3,  # Lower for demo
            orchestrator=agent_router,
        )
    )

    # Set up agents with routers
    research_agent.handoff_router = limit_router
    summary_agent.handoff_router = limit_router

    # Create and run flock
    flock = Flock(
        name="demo_flock",
        model=APP_SETTINGS.research_model,
        agents=[research_agent, summary_agent],
    )

    result = await flock.run_async(
        start_agent=research_agent,
        input={"topic": "Weather in Germany the last 10 years"}
    )
    
    print(f"Flock execution completed: {bool(result)}")


async def main():
    """Run all demos."""
    print("🚀 AI Agent Demo Suite")
    print("=" * 50)
    
    # Set up environment
    os.environ["AZURE_API_KEY"] = APP_SETTINGS.azure_api_key
    os.environ["AZURE_API_BASE"] = APP_SETTINGS.azure_api_base
    os.environ["AZURE_API_VERSION"] = APP_SETTINGS.azure_api_version
    
    try:
        # Run demos
        await demo_simple_usage()
        await demo_with_routers()
        
        print("\n✅ All demos completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure your environment variables are set correctly.")


if __name__ == "__main__":
    asyncio.run(main())
