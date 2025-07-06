# AI Agent Demo

This project demonstrates AI agents using the Flock framework with Azure OpenAI models.

## Quick Setup

1. **Install dependencies:**

   ```bash
   uv sync
   ```

2. **Set up environment:**

   ```bash
   cp .env.template .env
   # Edit .env with your Azure OpenAI credentials
   ```

3. **Run demo:**

   ```bash
   uv run python main.py
   ```

## Features

- **Research Agent**: Uses azure/gpt-4o-mini to research any topic
- **Summary Agent**: Uses azure/gpt-4.1-mini to create titles and summaries
- **Smart Routing**: AgentRouter automatically chains agents together
- **Safety**: LimitRouter prevents infinite loops

## Example Workflow

1. You provide a topic (e.g., "Artificial Intelligence in Healthcare")
2. Research Agent researches the topic and provides detailed findings
3. Summary Agent creates a title and summary from the research
4. You get comprehensive results with both detailed research and concise summaries

## Project Structure

```bash
ai-agent-demo/
├── pyproject.toml          # Project configuration and dependencies
├── .python-version         # Python version (3.11)
├── .env.template          # Environment variables template
├── .env                   # Environment variables (ignored by git)
├── main.py                # Main application entry point
├── demo.py                # Demo/example scripts
├── settings.py            # Application settings configuration
├── agents/                # AI agents directory
│   ├── __init__.py        # Package initialization
│   ├── research_agent.py  # Research agent (azure/gpt-4o-mini)
│   └── summary_agent.py   # Summary agent (azure/gpt-4.1-mini)
└── routers/               # Router components directory
    ├── __init__.py        # Package initialization
    └── limit_router.py    # LimitRouter to prevent infinite loops
```

## Agent Details

### 📊 Research Agent

- **Model**: azure/gpt-4o-mini
- **Purpose**: Conducts comprehensive research on topics
- **Input**: topic (string)
- **Output**: research_content, key_points, sources_mentioned
- **Features**: Thought process, streaming, rich tables

### 📝 Summary Agent

- **Model**: azure/gpt-4.1-mini
- **Purpose**: Creates titles and summaries from research
- **Input**: research_content, key_points, sources_mentioned
- **Output**: title, short_summary, detailed_summary, recommendation
- **Features**: Thought process, streaming, rich tables

## Router Details

### 🎯 AgentRouter

- **Purpose**: Intelligently routes between agents
- **Features**: Confidence threshold (0.75), output enabled
- **Behavior**: Decides which agent should run next

### 🛡️ LimitRouter

- **Purpose**: Prevents infinite execution loops
- **Configuration**: Max iterations (configurable, default 10)
- **Behavior**: Wraps AgentRouter and stops after max iterations
- **Safety**: Resets counter after reaching limit

## Environment Setup

### Required Environment Variables

- `AZURE_API_KEY`: Your Azure OpenAI API key
- `AZURE_API_BASE`: Your Azure OpenAI endpoint URL
- `AZURE_API_VERSION`: API version (default: 2025-01-01)

### Optional Configuration

- `RESEARCH_MODEL`: Model for research agent (default: azure/gpt-4o-mini)
- `SUMMARY_MODEL`: Model for summary agent (default: azure/gpt-4.1-mini)
- `DEFAULT_TEMPERATURE`: Model temperature (default: 0.7)
- `MAX_TOKENS`: Max output tokens (default: 4000)
- `MAX_ITERATIONS`: Router iteration limit (default: 10)

### Setup Steps

1. Copy `.env.template` to `.env`
2. Fill in your Azure OpenAI credentials
3. Run: `uv run python main.py`

## Usage Examples

```bash
# Run the main demo
uv run python main.py

# Run example scenarios
uv run python demo.py
```
