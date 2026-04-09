from langgraph.graph import StateGraph, START, END

from .state import AgentState
from .nodes import triage_node, agent_node, tool_node, should_continue

# 1. Khởi tạo StateGraph
builder = StateGraph(AgentState)

# 2. Add Nodes
builder.add_node("triage", triage_node)
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

# 3. Add Edges (Luồng điều khiển)
# Bắt đầu luồng tại Triage để kiểm duyệt từ khóa khẩn cấp
builder.add_edge(START, "triage")

# Triage xong thì đẩy Context State qua cho LLM Agent xử lý
builder.add_edge("triage", "agent")

# Logic điều hướng Conditional (Tự động quyết định)
builder.add_conditional_edges("agent", should_continue, {
    "tools": "tools",  # LLM muốn gọi tool
    "end": END         # Trả lời luôn cho user
})

# Tool chạy xong quay lại Agent để lấy kết quả nhồi vào Chat Result
builder.add_edge("tools", "agent")

# 4. Biên dịch đồ thị
vivi_app = builder.compile()
