# 🤖 Build AI Agents with smolagents

This repository contains the code examples and resources for the "Build AI Agents with smolagents" tutorial course. 

## 🧰 Resources

- 📝 [PDF Slides](https://jmp.sh/s/1CkBN1S815dwy5hidTUR)
- 📺 [YouTube Course](https://youtu.be/UYEBMEAxIfA)
- ☕ [Support](https://buymeacoffee.com/hayerhans)


## Resources used:
- https://huggingface.co/docs/smolagents/index
- https://huggingface.co/learn/agents-course/unit0/introduction

## 📋 Course Overview

Learn how to build powerful AI agents using the smolagents framework. This course covers both theoretical concepts and practical implementation, including:

- Understanding AI agents, components, and architecture
- Exploring workflow types and multi-agent collaboration patterns
- Building agents with custom tools and UI
- Creating multi-agent systems
- Implementing monitoring with OpenTelemetry and LangFuse
- Sharing your agents on Hugging Face Spaces

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A Hugging Face API token

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/XamHans/smolagents-course.git
cd smolagents-course
```

2. **Install uv**

We'll use `uv`, a fast Python package installer and resolver, for setting up the environment.

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows using PowerShell
irm -Uri https://astral.sh/uv/install.ps1 | iex

# Alternatively, install via pipx
pipx install uv
```

3. **Set up your environment with uv**

```bash
# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate

# Sync dependencies from the lockfile
uv sync
```

The project uses a lockfile (`uv.lock`) and project configuration (`pyproject.toml`), so `uv sync` will install the exact versions of dependencies specified in these files.


3. **Configure your environment variables**

```bash
# Copy the example .env file
cp .env.example .env

# Edit the .env file with your Hugging Face API token
# Get your token from: https://huggingface.co/settings/tokens
```

## 📁 Repository Structure

- `main.py` - Basic agent example to get started
- `agent-with-ui.py` - Example of an agent with user interface
- `agent-with-monitor.py` - Implementation with monitoring capabilities
- `multi-agents.py` - Multi-agent system example
- `share-agents.py` - Code to share your agents on Hugging Face Spaces

## 🔍 Usage Examples

### Running a simple agent

```bash
uv run main.py
```

### Running an agent with UI

```bash
uv run agent-with-ui.py
```

### Working with multiple agents

```bash
uv run multi-agents.py
```

## 🔐 Hugging Face Token

This course uses Hugging Face models, which require an API token for access. To obtain your token:

1. Create an account at [Hugging Face](https://huggingface.co/)
2. Go to Settings > [Access Tokens](https://huggingface.co/settings/tokens)
3. Create a new token with read permission
4. Add this token to your `.env` file

## 📚 Further Learning

The video course provides detailed explanations for all code examples in this repository. The course walks through each implementation step-by-step, covering both theory and practice.

## 🤝 Contributing

Feel free to submit issues or pull requests if you find any problems or have suggestions for improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.