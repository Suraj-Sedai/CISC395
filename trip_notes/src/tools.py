import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import urllib.request
from src.rag import search_guides, ensure_index

def budget_breakdown(destination: str, days: int, budget_usd: float) -> str:
    """
    Calculates a daily budget breakdown:
    - accommodation: 40% of daily budget
    - food: 30% of daily budget
    - transport: 15% of daily budget
    - activities: 15% of daily budget
    """
    daily_total = budget_usd / days
    
    accommodation = daily_total * 0.40
    food = daily_total * 0.30
    transport = daily_total * 0.15
    activities = daily_total * 0.15
    
    report = [
        f"{days}-day {destination} budget (${budget_usd:.2f} total)",
        f"Daily: ${daily_total:.2f}",
        f"  Accommodation : ${accommodation:.2f}",
        f"  Food          : ${food:.2f}",
        f"  Transport     : ${transport:.2f}",
        f"  Activities    : ${activities:.2f}"
    ]
    return "\n".join(report)

def get_weather(city: str) -> str:
    """
    Fetches current weather from https://wttr.in/{city}?format=j1 using urllib.request.
    """
    url_city = city.replace(" ", "+")
    url = f"https://wttr.in/{url_city}?format=j1"
    
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            
            condition = data["current_condition"][0]
            temp_c = condition["temp_C"]
            temp_f = condition["temp_F"]
            description = condition["weatherDesc"][0]["value"]
            
            return f"{city}: {description}, {temp_c}°C / {temp_f}°F"
    except Exception as e:
        return f"Could not fetch weather for {city}: {e}"

def search_guides_tool(query: str) -> str:
    """
    Search the local travel guides for tips, recommendations, or information about a destination.
    """
    ensure_index()
    chunks = search_guides(query, n_results=2)
    
    if not chunks:
        return "No relevant information found in guides."
    
    return "\n\n---\n\n".join(chunks)

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "budget_breakdown",
            "description": "Calculate a daily budget breakdown for a trip given destination, number of days, and total budget in USD",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string",
                        "description": "The name of the destination"
                    },
                    "days": {
                        "type": "integer",
                        "description": "The number of days for the trip"
                    },
                    "budget_usd": {
                        "type": "number",
                        "description": "The total budget in USD"
                    }
                },
                "required": ["destination", "days", "budget_usd"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current real-time weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get weather for"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_guides_tool",
            "description": "Search the local travel guides for tips, recommendations, or information about a destination",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for the travel guides"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

if __name__ == "__main__":
    print("Testing budget_breakdown:")
    print(budget_breakdown("Tokyo", 7, 1400))
    print("\nTesting get_weather:")
    print(get_weather("Tokyo"))
    print("\nTesting search_guides_tool:")
    print(search_guides_tool("things to do in Tokyo"))
