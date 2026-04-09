from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    car_context: Dict[str, Any]
    diagnostic_info: Dict[str, Any]
    loop_count: int
    is_emergency: bool
    error_results: List[Any]
    selected_garage: Dict[str, Any]
    next_node: str
