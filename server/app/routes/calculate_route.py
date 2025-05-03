from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models import ChatOllama
from langchain_core.chat_history import InMemoryChatMessageHistory
import requests

router = APIRouter()

# Load local LLM
llm = ChatOllama(base_url="http://host.docker.internal:11434", model="llama2")

# In-memory chat history per session
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Wrap the model with message history support
conversation = RunnableWithMessageHistory(
    llm,
    get_session_history=get_session_history,
)

# Reverse geocode utility
def reverse_geocode(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    headers = {"User-Agent": "RoutePlannerAgent"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("display_name", f"{lat},{lon}")
    return f"{lat},{lon}"

# Create a summarized route string
def build_route_summary(coordinates):
    summary = []
    for i, (lon, lat) in enumerate(coordinates):
        place = reverse_geocode(lat, lon)
        summary.append(f"Stop {i+1}: {place}")
    return "\n".join(summary)


# Define the request model
class RouteRequest(BaseModel):
    user_intent: str
    email: str    


@router.post('/calculate_route')
def calculate_route(data: RouteRequest):
    print("IM HERE **********************************")
    print("DATA@@@@@@@@@@@@@@@@@@@@@@@@@", data)
    coordinates = [
        [2.3522, 48.8566],   # Paris
        [2.7280, 47.7544],   # midpoint
        [4.8357, 45.7640],   # Lyon
    ]
    route_summary = build_route_summary(coordinates)

    # Format user input for the conversation
    full_input = f"""
    User Intent: {data.user_intent}

    Route:
    {route_summary}

    If relevant, update the itinerary accordingly.
    """

    # Process the input and get the response
    response = conversation.invoke(
        full_input,
        config={"configurable": {"session_id": data.email}}  # Use email as session ID for uniqueness
    )

    return {
        "route_summary": route_summary,
        "agent_response": str(response)  # Return the agent's response
    }
