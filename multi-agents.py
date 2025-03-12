import os
import re
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import requests
from markdownify import markdownify
from requests.exceptions import RequestException
from smolagents import (CodeAgent, DuckDuckGoSearchTool, OpenAIServerModel,
                        ToolCallingAgent, tool)


# Web browsing tool
@tool
def visit_webpage(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string.

    Args:
        url: The URL of the webpage to visit.

    Returns:
        The content of the webpage converted to Markdown, or an error message if the request fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Convert the HTML content to Markdown
        markdown_content = markdownify(response.text).strip()

        # Remove multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content

    except RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Analysis tools
@tool
def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze the sentiment of a given text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary containing sentiment score and label
    """
    # Simple rule-based sentiment analysis
    positive_words = ["growth", "increase", "profit", "success", "positive", "innovative", 
                      "improvement", "opportunity", "beneficial", "advantage"]
    negative_words = ["decline", "decrease", "loss", "failure", "negative", "downturn", 
                      "challenging", "problem", "risk", "threat"]
    
    text_lower = text.lower()
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    score = (positive_count - negative_count) / max(1, positive_count + negative_count)
    
    if score > 0.2:
        label = "positive"
    elif score < -0.2:
        label = "negative"
    else:
        label = "neutral"
    
    return {
        "score": score,
        "label": label,
        "positive_count": positive_count,
        "negative_count": negative_count
    }

@tool
def extract_key_metrics(text: str) -> Dict[str, Any]:
    """
    Extract key metrics and statistics from text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary of extracted metrics
    """
    # Extract percentages
    percentage_pattern = r'(\d+(?:\.\d+)?)%'
    percentages = re.findall(percentage_pattern, text)
    
    # Extract dollar amounts
    dollar_pattern = r'\$(\d+(?:,\d+)*(?:\.\d+)?)(?: (?:million|billion|trillion))?'
    dollar_matches = re.findall(dollar_pattern, text)
    
    # Extract dates
    date_pattern = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b'
    dates = re.findall(date_pattern, text, re.IGNORECASE)
    
    metrics = {
        "percentages": [float(p) for p in percentages] if percentages else [],
        "dollar_amounts": [m.replace(',', '') for m in dollar_matches] if dollar_matches else [],
        "dates": dates if dates else []
    }
    
    return metrics

# Initialize the OpenAI models
web_model = OpenAIServerModel(
    model_id="gpt-4o-mini-2024-07-18",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)

reasoning_model = OpenAIServerModel(
    model_id="o3-mini-2025-01-31",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)

# Create specialized agents
# 1. Web Search Agent - for retrieving market information
web_agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), visit_webpage],
    model=web_model,
    max_steps=8,
    name="web_search_agent",
    description="Searches the web for recent market data and news about specific industries.",
)

# 2. Analysis Agent - for processing information
analysis_agent = ToolCallingAgent(
    tools=[analyze_sentiment, extract_key_metrics],
    model=reasoning_model,
    max_steps=5,
    name="analysis_agent",
    description="Analyzes market data to extract sentiment and key metrics",
)

# 3. Manager Agent - orchestrates the entire process
manager_agent = CodeAgent(
    model=reasoning_model,
    tools=[],
    managed_agents=[web_agent, analysis_agent],
    additional_authorized_imports=["pandas", "matplotlib.pyplot"],
    name="market_research_manager",
    description="Manages the market research workflow and compiles the final report",
    planning_interval=2,
    max_steps=12,
    verbosity_level=2
)

# Display the agent hierarchy
def visualize_agent_system():
    manager_agent.visualize()

# Example usage function
def run_market_research(industry: str):
    """
    Generate a market research report for a specific industry.
    
    Args:
        industry: The industry to research
        
    Returns:
        A market research report with insights and analysis
    """
    prompt = f"""
    You are a market research assistant. Your task is to research recent trends in the {industry} industry
    and prepare a concise market report. Follow these steps:
    
     Compile everything into a final report with:
       - Executive summary (2-3 paragraphs)
       - Key trends (bullet points)
       - Market sentiment analysis (include both positive and negative perspectives)
       - Important statistics and metrics
       - Conclusion with outlook
    
    The report should be concise but comprehensive, focusing on actionable insights. Also include sources at the end of report from where you got the data.
    """
    
    result = manager_agent.run(prompt)
    return result

# Usage example
if __name__ == "__main__":
    # Visualize the agent system
    visualize_agent_system()
    
    # Run a market research for the renewable energy industry
    report = run_market_research("defence industry")
    print(report)
    
    # You can easily run research for other industries
    # report = run_market_research("electric vehicles")
    # report = run_market_research("artificial intelligence")