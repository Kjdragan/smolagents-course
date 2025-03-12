# Part 1: Setting up Langfuse authentication
# -----------------------------------------------------------------------------
import base64
import os

# Langfuse API keys - required to authenticate with the Langfuse platform
# These keys can be obtained by signing up for Langfuse Cloud or self-hosting Langfuse
LANGFUSE_PUBLIC_KEY="pk-lf-afa0f263-634c-4e09-8b4e-4d9ad1ae69fc"
LANGFUSE_SECRET_KEY="sk-lf-18883a89-ae82-4bf6-8142-8463e2a3082a"

# Create the authentication header by encoding the API keys as base64
# This follows the HTTP Basic Authentication format expected by Langfuse
LANGFUSE_AUTH=base64.b64encode(f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()).decode()

# Configure OpenTelemetry (OTEL) environment variables to send data to Langfuse
# OTEL_EXPORTER_OTLP_ENDPOINT specifies where to send the telemetry data
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:3000/api/public/otel"  
# Uncomment the line below if your data should be stored in the US region instead
# os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://eu.cloud.langfuse.com/api/public/otel"  # US data region

# Set the authorization header for the OTEL exporter
# This ensures that your telemetry data is associated with your Langfuse account
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"


from openinference.instrumentation.smolagents import \
    SmolagentsInstrumentor  # Specific instrumentation for smolagents
from opentelemetry.exporter.otlp.proto.http.trace_exporter import \
    OTLPSpanExporter  # Exports traces via OTLP/HTTP
# Part 2: Setting up OpenTelemetry instrumentation for smolagents
# -----------------------------------------------------------------------------
from opentelemetry.sdk.trace import \
    TracerProvider  # Responsible for creating tracers
from opentelemetry.sdk.trace.export import \
    SimpleSpanProcessor  # Processes and exports spans as they end

# Agent Execution with OpenTelemetry Tracing
# -----------------------------------------

# TRACE: Complete execution of one agent invocation
# =====================================================================
#                                                                     
#  ┌───────────────────────── Root Span ─────────────────────────┐   
#  │ name: "agent.run"                                           │   
#  │ trace_id: abc123                                            │   
#  │ span_id: span1                                              │   
#  │ attributes: {agent_type: "CodeAgent", query: "How can..."}  │   
#  │                                                             │   
#  │    ┌─────────── Child Span ───────────┐                     │   
#  │    │ name: "llm.completion"           │                     │   
#  │    │ trace_id: abc123                 │     Span Context    │   
#  │    │ span_id: span2                   │    ┌───────────┐    │   
#  │    │ parent_id: span1                 │    │trace_id   │    │   
#  │    │ attributes: {model: "deepseek",  │    │span_id    │    │   
#  │    │              tokens: 450}        │    │parent_id  │    │   
#  │    │                                  │    │flags      │    │   
#  │    │ ⏱️  start_time: 12:00:00.000     │    └───────────┘    │   
#  │    │ ⏱️  end_time:   12:00:00.850     │                     │   
#  │    │                                  │                     │   
#  │    │ 📝 event: "tokens_calculated"    │                     │   
#  │    └──────────────────────────────────┘                     │   
#  │                                                             │   
#  │    ┌─────────── Child Span ───────────┐                     │   
#  │    │ name: "managed_agent.invoke"     │                     │   
#  │    │ trace_id: abc123                 │                     │   
#  │    │ span_id: span3                   │                     │   
#  │    │ parent_id: span1                 │                     │   
#  │    │ attributes: {                    │                     │   
#  │    │   agent_name: "search_agent",    │                     │   
#  │    │   agent_type: "ToolCallingAgent" │                     │   
#  │    │ }                                │                     │   
#  │    │                                  │                     │   
#  │    │    ┌── Nested Child Span ──┐     │                     │   
#  │    │    │ name: "tool.call"     │     │                     │   
#  │    │    │ trace_id: abc123      │     │                     │   
#  │    │    │ span_id: span4        │     │                     │   
#  │    │    │ parent_id: span3      │     │                     │   
#  │    │    │ attributes: {         │     │                     │   
#  │    │    │   tool: "SearchTool"  │     │                     │   
#  │    │    │ }                     │     │                     │   
#  │    │    │                       │     │                     │   
#  │    │    │ ⚠️ event: "error"     │     │                     │   
#  │    │    └───────────────────────┘     │                     │   
#  │    └──────────────────────────────────┘                     │   
#  │                                                             │   
#  │    ┌─────────── Child Span ───────────┐                     │   
#  │    │ name: "llm.completion"           │                     │   
#  │    │ trace_id: abc123                 │                     │   
#  │    │ span_id: span5                   │                     │   
#  │    │ parent_id: span1                 │                     │   
#  │    └──────────────────────────────────┘                     │   
#  │                                                             │   
#  └─────────────────────────────────────────────────────────────┘   
#                              │                                     
#                              ▼                                     
#                  ┌─────────────────────────┐                      
#                  │   Span Processor        │                      
#                  │  (SimpleSpanProcessor)  │                      
#                  └─────────────────────────┘                      
#                              │                                     
#                              ▼                                     
#                  ┌─────────────────────────┐                      
#                  │       Exporter          │                      
#                  │   (OTLPSpanExporter)    │                      
#                  └─────────────────────────┘                      
#                              │                                     
#                              ▼                                     
#                  ┌─────────────────────────┐                      
#                  │        Langfuse         │                      
#                  │  Telemetry Backend      │                      
#                  └─────────────────────────┘                      
#
# Key concepts visualized:
# -----------------------
# * TRACE - A trace represents the complete journey of a request through your system. For an agent, this is the entire execution from receiving a user's query to delivering the final response. 
# * SPAN - A span is a single unit of work within a trace.  (each nested box)
# * CONTEXT - Information that links spans together in a trace
# * ATTRIBUTES - Key-value metadata about each span
# * EVENTS - Point-in-time markers within a span
# * PROCESSOR - Handles completed spans (SimpleSpanProcessor = immediate processing)
# * EXPORTER - Sends spans to the backend (OTLPSpanExporter = using OpenTelemetry Protocol)


# Create a TracerProvider which will generate trace IDs and manage spans
trace_provider = TracerProvider()

# Add a span processor with an OTLP exporter to send trace data to Langfuse
# SimpleSpanProcessor exports spans immediately when they end (synchronously)
# This is good for debugging but in high-performance apps, BatchSpanProcessor might be better
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))

# Initialize the SmolagentsInstrumentor with our trace_provider
# This automatically wraps all relevant smolagents methods to track execution
# No additional code changes needed in our agent implementation!
SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)


# Part 3: Creating our agent system with smolagents
# -----------------------------------------------------------------------------
from smolagents import (CodeAgent, DuckDuckGoSearchTool, GradioUI, HfApiModel,
                        tool)


@tool
def get_weather_data(city: str) -> dict:
    """
    Returns sample weather data for a given city

    Args:
        city: Name of the city (new york, london or toyko)

    """
    sample_data = {
        "new york": {
            "temps": [72, 75, 65, 68, 70, 74, 73],
            "rain": [0, 0.2, 0.5, 0, 0, 0.1, 0],
            "unit": "F"
        },
        "london": {
            "temps": [15, 14, 16, 13, 15, 17, 16],
            "rain": [0.5, 0.2, 0, 0.1, 0.3, 0, 0.2],
            "unit": "C"
        },
        "tokyo": {
            "temps": [22, 24, 23, 25, 26, 25, 22],
            "rain": [0, 0, 0.3, 0.2, 0, 0, 0.1],
            "unit": "C"
        }
    }

    city_lower = city.lower()
    return sample_data.get(city_lower, {"error": f"No data for {city}"})


model = HfApiModel()


agent = CodeAgent(tools=[get_weather_data], model=model, additional_authorized_imports=['matplotlib'], verbosity_level=2)

# Run the agent with a simple task
print("Running weather analysis agent...")
response = agent.run(
    """
    Get the weather data for Tokyo and:
    1. Calculate the average temperature
    2. Count rainy days
    3. Make a simple bar chart of daily temperatures
    4. Save the chart to 'tokyo_temps.png' (don't use plt.show())
    """
)

# After this runs, you can view the complete trace in the Langfuse UI
# The trace will show:
# - All interactions between the manager and search agents
# - All LLM calls with inputs and outputs
# - All tool calls and their results
# - The complete reasoning chain and execution flow
# - Performance metrics like latency and token usage