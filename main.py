import os
import datetime
import time
import threading
from typing import Annotated, Literal, TypedDict
from dotenv import load_dotenv

# LangChain & LangGraph imports
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Load API Keys
load_dotenv()

# --- STEP 1: SIMULATE THE DATABASE ---
# Calendar for passive events (Meetings, Parties)
calendar_db = []
# Reminders for active notifications (Wake up, Drink water)
reminders_db = []

# --- STEP 2: DEFINE TOOLS (FUNCTIONS) ---

@tool
def add_calendar_event(event_name: str, time: str, description: str = ""):
    """
    Use this tool to schedule passive EVENTS (Meetings, Trips).
    Input required: event_name, time (Format: 'YYYY-MM-DD HH:MM'), description.
    """
    try:
        event = {
            "id": len(calendar_db) + 1,
            "name": event_name,
            "time": time,
            "description": description,
            "type": "event",
            "created_at": str(datetime.datetime.now())
        }
        calendar_db.append(event)
        return f"Success: Scheduled event '{event_name}' at {time}."
    except Exception as e:
        return f"Error adding event: {str(e)}"

@tool
def set_reminder(task_name: str, time: str):
    """
    Use this tool to set an ACTIVE REMINDER/ALARM.
    Use when user says: 'Remind me', 'Wake me up', 'Alert me'.
    Input required: task_name, time (Format: 'YYYY-MM-DD HH:MM').
    """
    try:
        reminder = {
            "id": len(reminders_db) + 1,
            "task": task_name,
            "time": time,
            "status": "pending"  # Status: pending -> done
        }
        reminders_db.append(reminder)
        return f"Success: I will remind you to '{task_name}' at {time}."
    except Exception as e:
        return f"Error setting reminder: {str(e)}"

@tool
def list_all_activities():
    """
    Use this tool to list ALL Calendar Events and Active Reminders.
    """
    result = "--- YOUR PLAN ---\n"
    
    # List Events
    if calendar_db:
        result += "[EVENTS]\n"
        for event in calendar_db:
            result += f"- {event['time']}: {event['name']} ({event['description']})\n"
    else:
        result += "[EVENTS] Empty.\n"

    # List Reminders
    if reminders_db:
        result += "[REMINDERS]\n"
        for r in reminders_db:
            status_icon = "⏳" if r['status'] == 'pending' else "✅"
            result += f"- {r['time']}: {r['task']} {status_icon}\n"
    else:
        result += "[REMINDERS] Empty.\n"
        
    return result

tools = [add_calendar_event, set_reminder, list_all_activities]

# --- STEP 3: BUILD THE LANGGRAPH AGENT ---

# Define the state of the Graph (State)
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize LLM
# USING GPT-4o for best logic handling
llm = ChatOpenAI(
    model="gpt-4o",   
    temperature=0,
    max_tokens=150
)
llm_with_tools = llm.bind_tools(tools)

# Node 1: Agent (The decision-making brain)
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # --- Date & Time Calculation Logic ---
    now = datetime.datetime.now()
    days_map = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_str = days_map[now.weekday()]
    date_str = now.strftime("%Y-%m-%d") # Format YYYY-MM-DD for consistency
    time_str = now.strftime("%H:%M")
    
    # Detailed System Prompt to avoid Date Hallucinations (e.g., Year 2025 error)
    prompt_text = (
        f"You are a smart Personal Assistant.\n"
        f"Current Context: Today is {weekday_str}, Date: {date_str}, Time: {time_str}.\n"
        f"INSTRUCTIONS:\n"
        f"1. If user says 'Next Sunday' or 'This Friday', calculate the specific date based on Today.\n"
        f"2. Use 'add_calendar_event' for meetings/events.\n"
        f"3. Use 'set_reminder' ONLY when user explicitly asks to be reminded or alerted.\n"
        f"4. Always ensure time format is 'YYYY-MM-DD HH:MM'."
    )
    
    system_prompt = SystemMessage(content=prompt_text)
    
    # Ensure SystemPrompt is always at the beginning/updated
    if not isinstance(messages[0], SystemMessage):
         messages = [system_prompt] + messages
    else:
        messages[0] = system_prompt
         
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Node 2: Tools Execution
tool_node = ToolNode(tools)

# Conditional Edge
def should_continue(state: AgentState) -> Literal["tools", END]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")
app = workflow.compile()

# --- BACKGROUND THREAD FOR REMINDERS ---
def background_reminder_checker():
    """
    Runs in background to check if any reminder matches current time.
    """
    print("   [System] Background reminder service started...")
    while True:
        # Get current time (Strip seconds for comparison)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        for reminder in reminders_db:
            if reminder['status'] == 'pending':
                # Compare string times (e.g. "2024-05-21 14:00")
                if reminder['time'] <= current_time:
                    print(f"\n\n🔔 🔔 🔔 REMINDER ALERT: {reminder['task']} at {reminder['time']} 🔔 🔔 🔔\nYou: ", end="")
                    reminder['status'] = 'done' # Mark as done so it doesn't ring again
        
        time.sleep(5) # Check every 5 seconds

# --- STEP 4: RUN DEMO ---
if __name__ == "__main__":
    
    # 1. Start Background Thread for Reminders
    reminder_thread = threading.Thread(target=background_reminder_checker, daemon=True)
    reminder_thread.start()

    print(f"--- PERSONAL ASSISTANT (GPT-4o + Real-time Reminders) ---")
    print("Type 'quit' to exit.")
    
    # 2. Draw Graph Structure
    print("Generating Graph structure...")
    try:
        png_data = app.get_graph().draw_mermaid_png()
        with open("graph_structure.png", "wb") as f:
            f.write(png_data)
        print("--> SUCCESS: Saved to 'graph_structure.png'")
    except Exception as e:
        print(f"--> WARNING: Could not draw graph. Error: {e}")
        # print(app.get_graph().draw_mermaid()) # Optional: Print code if drawing fails

    # 3. Chat Loop
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                break
            
            inputs = {"messages": [HumanMessage(content=user_input)]}
            
            for event in app.stream(inputs, stream_mode="values"):
                message = event["messages"][-1]
                
                if isinstance(message, AIMessage):
                    if not message.tool_calls and message.content:
                        print(f"Assistant: {message.content}")

        except Exception as e:
            print(f"System Error: {e}")