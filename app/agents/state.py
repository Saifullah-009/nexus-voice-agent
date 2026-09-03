from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class VoiceAgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    voice_output: str