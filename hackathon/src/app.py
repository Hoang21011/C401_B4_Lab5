import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Tìm đường dẫn gốc
current_dir = os.path.dirname(os.path.abspath(__file__))
hackathon_dir = os.path.dirname(current_dir)
sys.path.append(hackathon_dir)

# Đọc file env
env_path = os.path.join(hackathon_dir, '.env')
load_dotenv(env_path)

# Inject API Key cho langchain-google-genai dùng auto
if not os.getenv("GEMINI_API_KEY"):
    st.error("Lỗi: Không tìm thấy GEMINI_API_KEY trong file .env!")
    st.stop()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

from langchain_core.messages import HumanMessage
from agent.graph import vivi_app

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Vivi AI - VinFast", page_icon="🚘", layout="centered")

st.title("🚘 Vivi - Trợ Lý VinFast (LangGraph)")
st.caption("Bản demo tích hợp Stateful Workflow 4 Nodes và Tools ReAct Loop")

# ----------------- Khởi tạo -----------------
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "user_demo_session"

# Phân biệt tin nhắn thuần túy hiển thị trên UI và State của LangGraph
if "ui_messages" not in st.session_state:
    st.session_state.ui_messages = []
    
if "agent_state" not in st.session_state:
    # State gốc để giữ lặp, đẩy ngược lại cho graph nếu tiếp tục chat
    st.session_state.agent_state = {"messages": [], "loop_count": 0, "is_emergency": False}

# ----------------- Giao diện Chat -----------------
# Render lại lịch sử chat trên UI
for msg in st.session_state.ui_messages:
    role = "assistant" if msg["role"] == "assistant" else "user"
    with st.chat_message(role):
        st.markdown(msg["content"])

# Xử lý input 
if prompt := st.chat_input("Hãy mô tả biểu hiện của xe... (VD: xe mất phanh, xe bốc khói)"):
    # Render user part
    st.session_state.ui_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Xử lý agent part
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Add câu nói vào state nội bộ
            st.session_state.agent_state["messages"].append(HumanMessage(content=prompt))
            
            # Gói lại input để truyền vào đồ thị LangGraph
            inputs = {
                "messages": st.session_state.agent_state["messages"],
                "loop_count": st.session_state.agent_state["loop_count"],
                "is_emergency": st.session_state.agent_state["is_emergency"]
            }
            
            final_content = ""
            
            # Dùng stream() để hứng kết quả
            for event in vivi_app.stream(inputs, config={"configurable": {"thread_id": st.session_state.thread_id}}, stream_mode="values"):
                last_msg = event["messages"][-1]
                
                # Check Tool Calls: Hiển thị toast thông báo cho đẹp
                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                    for tool in last_msg.tool_calls:
                        st.toast(f"⚙️ Running tool: {tool['name']}", icon="🔧")
                
                # In ra text nếu có (tránh in nội dung rỗng)
                if last_msg.type == "ai" and last_msg.content:
                    final_content = last_msg.content
                    message_placeholder.markdown(final_content)
                    
            # Update lại State trên phiên hiện tại sau khi graph chạy xong
            st.session_state.agent_state["messages"] = event["messages"]
            st.session_state.agent_state["loop_count"] = event.get("loop_count", 0)
            st.session_state.agent_state["is_emergency"] = event.get("is_emergency", False)
            
            # Lưu lại câu cuối vào UI history
            if final_content:
                st.session_state.ui_messages.append({"role": "assistant", "content": final_content})

        except Exception as e:
            st.error(f"Đã có lỗi từ Agent: {e}")
