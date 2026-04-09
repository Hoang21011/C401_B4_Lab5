import os
import sys
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode

# Thiết lập đường dẫn để import chuẩn các tools
current_dir = os.path.dirname(os.path.abspath(__file__))
hackathon_dir = os.path.dirname(current_dir)
sys.path.append(hackathon_dir)

from agent.state import AgentState
from tools.diagnose import VINFAST_TOOLS
from tools.search_garages import search_garages
from tools.search_mechanic import search_mechanic
from tools.maintain_schedule import maintain_schedule

# Khởi tạo list các tool
all_tools = VINFAST_TOOLS + [search_garages, search_mechanic, maintain_schedule]
tool_node = ToolNode(all_tools)

# Khởi tạo model
model_name = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")
if "gpt" in model_name.lower():
    model_name = "gemini-1.5-flash"

llm = ChatGoogleGenerativeAI(model=model_name)
llm_with_tools = llm.bind_tools(all_tools)

def get_system_prompt() -> str:
    prompt_path = os.path.join(hackathon_dir, 'system_prompt.txt')
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Bạn là trợ lý ảo VinFast."

def triage_node(state: AgentState):
    """
    Node A: Triage (Safety Gate) - Cổng kiểm duyệt từ khóa khẩn cấp
    """
    messages = state.get("messages", [])
    if not messages:
        return {"is_emergency": False}
        
    last_msg = messages[-1].content.lower()
    emergency_keywords = ["cháy", "khói", "mất phanh", "hệ thống lái", "pin", "cao tốc", "tai nạn", "bốc khói", "chết máy"]
    
    is_emergency = state.get("is_emergency", False)
    
    if not is_emergency:
        for kw in emergency_keywords:
            if kw in last_msg:
                is_emergency = True
                break
                
    return {"is_emergency": is_emergency}

def agent_node(state: AgentState):
    """
    Node B + C + D: Chịu trách nhiệm Reasoning vòng lặp (LLM Agent) và quyết định gọi Tool nào.
    """
    messages = state.get("messages", [])
    sys_prompt_content = get_system_prompt()
    
    # Nếu vòng lặp > 3, nhắc LLM không được hỏi dông dài nữa
    loop_count = state.get("loop_count", 0)
    if loop_count >= 3:
        sys_prompt_content += "\n\n[WARNING]: Đã hết số lần hỏi (3 lần). Bạn PHẢI GỌI tool diagnose ngay lập tức với thông tin hiện có!"
        
    # Ép xử lý khẩn cấp
    if state.get("is_emergency"):
        sys_prompt_content += "\n\n[LƯU Ý KHẨN CẤP]: CÓ TỪ KHÓA NGUY HIỂM TRONG NỘI DUNG. Hãy thực hiện đúng protocol ưu tiên: Báo người dùng rời xe, lấy vị trí và gọi maintain_schedule với is_emergency=True ngay lập tức!"
        
    sys_msg = SystemMessage(content=sys_prompt_content)
    
    # Nạp system prompt vào đầu
    if not messages or not isinstance(messages[0], SystemMessage):
        msgs_to_run = [sys_msg] + messages
    else:
        msgs_to_run = [sys_msg] + messages[1:]
        
    response = llm_with_tools.invoke(msgs_to_run)
    
    # Logic tăng loop nếu LLM ra câu hỏi thay vì gọi tool
    if not response.tool_calls:
        loop_count += 1
        
    return {"messages": [response], "loop_count": loop_count}

def should_continue(state: AgentState):
    """
    Điều hướng đi tiếp hoặc rẽ nhánh tool
    """
    messages = state.get("messages", [])
    last_message = messages[-1]
    
    # Kiểm tra LLM có ra output gọi tool không
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    return "end"
