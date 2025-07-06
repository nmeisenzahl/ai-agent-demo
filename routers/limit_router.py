"""Limiting Router to prevent infinite iterations."""

from flock.core.flock_router import FlockRouter, FlockRouterConfig, HandOffRequest
from flock.routers.agent.agent_router import AgentRouter
from pydantic import ConfigDict, Field


class LimitRouterConfig(FlockRouterConfig):
    """Configuration for LimitRouter."""
    
    max_iterations: int = Field(
        default=10,
        description="Maximum number of iterations before stopping."
    )
    
    orchestrator: AgentRouter = Field(
        ...,
        description="The underlying AgentRouter to orchestrate."
    )
    
    model_config: ConfigDict = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
    )


class LimitRouter(FlockRouter):
    """
    Limiting Router that prevents infinite loops.
    
    This router wraps an AgentRouter and stops execution 
    after a maximum number of iterations.
    """
    
    config: LimitRouterConfig = Field(
        ...,
        description="Router configuration"
    )
    
    current_iteration: int = Field(
        default=0,
        description="Current iteration counter."
    )
    
    async def route(self, current_agent, result, context) -> HandOffRequest:
        """Route to the next agent with iteration limit."""
        self.current_iteration += 1
        
        if self.current_iteration > self.config.max_iterations:
            print(f"Maximum iterations ({self.config.max_iterations}) reached. Stopping execution.")
            self.current_iteration = 0
            return HandOffRequest(
                next_agent=""  # Empty string stops execution
            )
        else:
            return await self.config.orchestrator.route(
                current_agent=current_agent,
                result=result,
                context=context
            )
