import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import urllib.request
from src.rag import search_guides, ensure_index
from src.ai_assistant import client, MODEL

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

def run_agent(user_question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a travel planning agent. Use the available tools to help "
                "users plan trips. Always use a tool if it can answer the question "
                "more accurately — especially for real-time data or guide content."
            )
        },
        {"role": "user", "content": user_question}
    ]

    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
            max_tokens=1024,
            timeout=30,
        )
        
        msg = response.choices[0].message
        if not msg.tool_calls:
            return msg.content

        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)
            print(f"[Tool call] {name}({args})")
            
            if name == "budget_breakdown":
                result = budget_breakdown(**args)
            elif name == "get_weather":
                result = get_weather(**args)
            elif name == "search_guides_tool":
                result = search_guides_tool(**args)
            else:
                result = f"Unknown tool: {name}"
            
            print(f"[Tool result] {result[:120]}...")
            
            messages.append({"role": "assistant", "content": None, "tool_calls": [tc]})
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result
            })
            
    return "Agent reached maximum iterations."

if __name__ == "__main__":
    print("Testing budget_breakdown:")
    print(budget_breakdown("Tokyo", 7, 1400))
    print("\nTesting get_weather:")
    print(get_weather("Tokyo"))
    print("\nTesting search_guides_tool:")
    print(search_guides_tool("things to do in Tokyo"))
