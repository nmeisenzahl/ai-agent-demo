# AI Agent Demo

This project demonstrates AI agents using the [Flock framework](https://whiteducksoftware.github.io/flock/) with Azure OpenAI models. The demo creates a complete workflow that researches topics, generates summaries, and produces beautiful newspaper-style HTML articles. It further showcases the capabilities of using GitHub Copilot for code generation and editing.

## 🎯 Features

- **🔍 Research Agent**: Conducts comprehensive research on any topic using Azure OpenAI
- **📝 Summary Agent**: Creates compelling titles and concise summaries 
- **🎨 Image Agent**: Generates relevant images using Azure OpenAI DALL-E 3
- **🌐 HTML Agent**: Generates beautiful newspaper-style HTML articles with dynamic CSS and embedded images
- **🔄 Smart Routing**: AgentRouter automatically chains agents together based on output requirements
- **🛡️ Safety Controls**: LimitRouter prevents infinite loops with configurable iteration limits
- **✅ HTML Validation**: Optional Playwright integration via MCP (Model Context Protocol) for HTML testing and validation
- **⚙️ Configurable**: Flexible model selection and parameter tuning

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure Environment

```bash
cp .env.template .env
# Edit .env with your Azure OpenAI credentials
```

Required environment variables:

- `AZURE_OPENAI_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_BASE`: Your Azure OpenAI endpoint URL

### 3. Run Demo

```bash
uv run python main.py
```

## 📋 Example Workflow

1. **Input**: You provide a topic (e.g., "Artificial Intelligence in Healthcare")
2. **Research**: Research Agent investigates the topic and provides detailed findings
3. **Summarize**: Summary Agent creates a compelling title and concise summary
4. **Visualize**: Image Agent generates a relevant illustration using DALL-E 3
5. **Generate**: HTML Agent produces a beautiful newspaper-style article with embedded image
6. **Output**: Complete HTML file with image saved, with optional Playwright validation

## 📁 Project Structure

```bash
ai-agent-demo/
├── 📄 pyproject.toml          # Project configuration and dependencies
├── 🔧 .env.template           # Environment variables template
├── 🚀 main.py                 # Main application entry point
├── ⚙️  settings.py             # Application settings configuration
├── agents/                    # AI agents directory
│   ├── 📋 __init__.py         # Package initialization
│   ├── 🔍 research_agent.py   # Research agent (gpt-4o-mini)
│   ├── 📝 summary_agent.py    # Summary agent (gpt-4.1-mini)
│   ├── 🎨 image_agent.py      # Image generation agent (dall-e-3)
│   └── � html_agent.py       # HTML generation agent (gpt-4.1-mini)
├── routers/                   # Router components directory
│   ├── 📋 __init__.py         # Package initialization
│   └── 🛡️ limit_router.py     # LimitRouter for safety controls
├── output/                    # Generated HTML files and images
└── utils/                     # Utility functions

```

## 🤖 Agent Details

### 🔍 Research Agent

- **Model**: `azure/gpt-4o-mini`
- **Purpose**: Conducts comprehensive research on any topic
- **Input**: `topic` (string)
- **Output**: `research_content`, `key_points`
- **Temperature**: 0.7 (balanced creativity)

### 📝 Summary Agent  

- **Model**: `azure/gpt-4.1-mini`
- **Purpose**: Creates titles and summaries from research content
- **Input**: `research_content`, `key_points`
- **Output**: `title`, `short_summary`
- **Temperature**: 0.5 (focused summarization)

### 🎨 Image Agent

- **Model**: `azure/dall-e-3`
- **Purpose**: Generates relevant images from article content using DALL-E 3
- **Input**: `title`, `short_summary`
- **Output**: `image_path`, `image_prompt`, `image_metadata`
- **Temperature**: 0.8 (high creativity for visual content)
- **Features**:
  - Enhanced prompt generation for better image quality
  - Automatic image download and local storage
  - Image validation and metadata collection
  - Safe filename generation with timestamps

### 🌐 HTML Agent

- **Model**: `azure/gpt-4.1-mini`
- **Purpose**: Generates newspaper-style HTML articles with embedded CSS and images
- **Input**: `title`, `short_summary`, `research_content`, `key_points`, `image_path`, `image_metadata`
- **Output**: `html_content` (complete HTML document)
- **Temperature**: 0.3 (consistent code generation)
- **Features**:
  - Dynamic CSS generation with image styling
  - Responsive design with hover effects
  - Image captions and credits
  - Accessibility features

## 🔄 Router Architecture

### 🎯 AgentRouter

- **Purpose**: Intelligently routes between agents based on data flow
- **Configuration**: Confidence threshold (0.5), output enabled
- **Behavior**: Automatically determines which agent should run next

### 🛡️ LimitRouter

- **Purpose**: Prevents infinite execution loops
- **Configuration**: Max iterations (default: 10, configurable)
- **Behavior**: Wraps AgentRouter and safely stops after reaching limits
- **Safety**: Automatic counter reset after limit reached

## ⚙️ Configuration

### 🔧 Environment Variables

#### Required

```bash
AZURE_OPENAI_KEY=your-azure-api-key-here
AZURE_OPENAI_BASE=https://your-resource.cognitiveservices.azure.com/
```

#### Optional (with defaults)

```bash
# API Configuration
AZURE_API_VERSION=2025-01-01

# Model Selection
RESEARCH_MODEL=azure/gpt-4o-mini
SUMMARY_MODEL=azure/gpt-4.1-mini
HTML_MODEL=azure/gpt-4.1-mini
IMAGE_MODEL=azure/dall-e-3

# Model Parameters
DEFAULT_TEMPERATURE=0.7
RESEARCH_TEMPERATURE=0.7
SUMMARY_TEMPERATURE=0.5
HTML_TEMPERATURE=0.3
IMAGE_TEMPERATURE=0.8
MAX_TOKENS=4000

# Router Configuration
MAX_ITERATIONS=10

# Output Configuration
OUTPUT_DIR=output
```

## Implementation of another MCP server using GH Copilot

Use the following prompt with GitHub Copilot to implement another MCP server to further provide research capabilities via Wikipedia:

```txt
Implement the Wikipedia MCP server (https://github.com/Rudra-ravi/wikipedia-mcp) and integrate it as a tool for the research agent to enhance research capabilities with real-time Wikipedia data.
```
