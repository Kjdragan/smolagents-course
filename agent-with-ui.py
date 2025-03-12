import base64
import os

from openinference.instrumentation.smolagents import \
    SmolagentsInstrumentor  # Specific instrumentation for smolagents
from opentelemetry.exporter.otlp.proto.http.trace_exporter import \
    OTLPSpanExporter  # Exports traces via OTLP/HTTP
from opentelemetry.sdk.trace import \
    TracerProvider  # Responsible for creating tracers
from opentelemetry.sdk.trace.export import \
    SimpleSpanProcessor  # Processes and exports spans as they end
from smolagents import (CodeAgent, DuckDuckGoSearchTool, GradioUI, HfApiModel,
                        tool)

# Langfuse API keys - required to authenticate with the Langfuse platform
# These keys can be obtained by signing up for Langfuse Cloud or self-hosting Langfuse
LANGFUSE_PUBLIC_KEY="pk-lf-738fdbd9-8c66-4af0-b742-2915a121cc87"
LANGFUSE_SECRET_KEY="sk-lf-86e4c30e-bf00-4d87-a87e-198eb6f8fa22"

# Create the authentication header by encoding the API keys as base64
# This follows the HTTP Basic Authentication format expected by Langfuse
LANGFUSE_AUTH=base64.b64encode(f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()).decode()

# Configure OpenTelemetry (OTEL) environment variables to send data to Langfuse
# OTEL_EXPORTER_OTLP_ENDPOINT specifies where to send the telemetry data
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:3000/api/public/otel"  
# Uncomment the line below if your data should be stored in the US region instead
# os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://us.cloud.langfuse.com/api/public/otel"  # US data region

# Set the authorization header for the OTEL exporter
# This ensures that your telemetry data is associated with your Langfuse account
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"



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

