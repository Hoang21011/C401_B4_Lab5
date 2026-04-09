import os
import json
from typing import Annotated, Sequence, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, BaseMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Import tools
from tools.diagnose import VINFAST_TOOLS
from tools.search_garages import search_garages
from tools.search_mechanic import search_mechanic
from tools.maintain_schedule import maintain_schedule

class AgentState(TypedDict):
    """Trạng thái của agent, lưu trữ lịch sử hội thoại."""
    messages: Annotated[Sequence[BaseMessage], add_messages]

def get_agent():
    # Setup LLM based on environment variables
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("DEFAULT_MODEL", "gemini-2.5-flash"),
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.2  # Low temperature for more deterministic, professional responses
    )

    # Read system prompt
    prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # Combine all tools
    all_tools = []
    all_tools.extend(VINFAST_TOOLS)
    all_tools.append(search_garages)
    all_tools.append(search_mechanic)
    all_tools.append(maintain_schedule)

    tool_map = {tool.name: tool for tool in all_tools}
    llm_with_tools = llm.bind_tools(all_tools)

    def call_model(state: AgentState):
        """Node gọi LLM để sinh câu trả lời hoặc quyết định gọi tool."""
        messages = state["messages"]
        # Đảm bảo inject system prompt ở đầu (tạo list mới mẻ để an toàn)
        sys_msg = SystemMessage(content=system_prompt)
        
        # Nếu message đầu tiên không phải system thì nhét vào, nếu phải thì thay thế hoàn toàn
        # Langchain google genai requires system messages to be at the very front
        clean_msgs = [m for m in messages if not isinstance(m, SystemMessage)]
        
        response = llm_with_tools.invoke([sys_msg] + clean_msgs)
        return {"messages": [response]}

    def execute_tools(state: AgentState):
        """Node thực thi các tools nếu LLM quyết định gọi."""
        messages = state["messages"]
        last_message = messages[-1]
        
        tool_messages = []
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            tool = tool_map.get(tool_name)
            if not tool:
                result_str = f"Error: Tool '{tool_name}' not found."
            else:
                try:
                    # Invoke tool and defensively serialize output
                    # Đề phòng trường hợp tool trả về Dictionaries hoặc List gây lỗi ToolMessage
                    raw_result = tool.invoke(tool_args)
                    
                    if isinstance(raw_result, (dict, list)):
                        result_str = json.dumps(raw_result, ensure_ascii=False, indent=2)
                    else:
                        result_str = str(raw_result)
                except Exception as e:
                    result_str = f"Lỗi khi thực thi tool '{tool_name}': {str(e)}"
            
            tool_messages.append(
                ToolMessage(
                    content=result_str,
                    tool_call_id=tool_call["id"],
                    name=tool_name
                )
            )
            
        return {"messages": tool_messages}

    def should_continue(state: AgentState):
        """Hàm điều hướng condition: Có tool call thì rẽ vào tools node, nếu không thì kết thúc."""
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return END

    # Thiết lập StateGraph thuần túy
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", execute_tools)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, ["tools", END])
    workflow.add_edge("tools", "agent")

    from langgraph.checkpoint.memory import MemorySaver
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    return app
