import os
import re
import time
from google import genai
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.config import config
from app.agents.state import VoiceAgentState
from app.tools.ops import get_system_metrics, check_ticket_status

client = genai.Client(api_key=config.GOOGLE_API_KEY)

SYSTEM_PROMPT = """You are Nexus, an autonomous enterprise voice operations assistant.
You maintain conversation context and execute real-time operations.

Backend actions:
1. If the user asks about system health, CPU, RAM, disk, or latency: include [ACTION:METRICS]
2. If asking about a ticket or incident: include [ACTION:TICKET:ID]

Rules:
- Speak in 1 to 2 clear, natural sentences.
- Never use markdown, bullet points, asterisks, or lists.
- Keep tone professional and operational."""

def call_gemini_with_retry(conversation_text: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=config.LLM_MODEL,
                contents=conversation_text,
                config={
                    "system_instruction": SYSTEM_PROMPT,
                    "temperature": 0.2
                }
            )
            return response.text or ""
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(0.5)
                continue
            return "Connection dropped momentarily. Systems are standing by."

def fast_voice_node(state: VoiceAgentState) -> dict:
    # Build context from previous conversation messages
    history = []
    for msg in state["messages"][-4:]:  # Keep last 4 turns for low latency & context
        role = "User" if msg.type == "human" else "Nexus"
        history.append(f"{role}: {msg.content}")
        
    full_context = "\n".join(history)
    text = call_gemini_with_retry(full_context)

    # Inline tool execution
    if "[ACTION:METRICS]" in text or any(k in full_context.lower() for k in ["cpu", "ram", "memory", "hardware"]):
        telemetry = get_system_metrics()
        text = f"Hardware diagnostics complete. {telemetry}"
    elif "[ACTION:TICKET" in text:
        match = re.search(r"\[ACTION:TICKET:(.*?)\]", text)
        ticket_id = match.group(1) if match else "409"
        status_info = check_ticket_status(ticket_id)
        text = f"Status confirmed. {status_info}"

    clean_speech = re.sub(r"\[ACTION:.*?\]", "", text).strip()

    from langchain_core.messages import AIMessage
    return {
        "messages": [AIMessage(content=clean_speech)],
        "voice_output": clean_speech
    }

# LangGraph with Checkpointer (Memory)
workflow = StateGraph(VoiceAgentState)
workflow.add_node("fast_agent", fast_voice_node)
workflow.set_entry_point("fast_agent")
workflow.add_edge("fast_agent", END)

memory_saver = MemorySaver()
voice_graph = workflow.compile(checkpointer=memory_saver)