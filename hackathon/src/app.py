import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Vivi AI - VinFast", page_icon="🚘", layout="centered")

@st.cache_resource
def init_model():
    """Hàm khởi tạo API Key và load System Prompt, dùng cache để không bị load lại nhiều lần"""
    # Tìm đường dẫn tuyệt đối tới file .env và system_prompt.txt
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hackathon_dir = os.path.dirname(current_dir)
    env_path = os.path.join(hackathon_dir, '.env')
    prompt_path = os.path.join(current_dir, 'system_prompt.txt')
    
    # Load file .env
    load_dotenv(env_path)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Lỗi: Không tìm thấy GEMINI_API_KEY trong file .env!")
        st.stop()
        
    genai.configure(api_key=api_key)
    
    # Load system prompt
    system_instruction = "Bạn là trợ lý ảo."
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_instruction = f.read()
    else:
        st.warning("⚠️ Không tìm thấy file system_prompt.txt, sử dụng prompt mặc định.")

    # Khởi tạo model (sử dụng DEFAULT_MODEL từ file .env nếu có, hoặc gemini-1.5-flash)
    model_name = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction
    )
    return model

# ----------------- Khởi tạo -----------------
st.title("🚘 Vivi - Trợ Lý VinFast (Mock Prototype)")
st.caption("Bản demo thử nghiệm System Prompt bằng Gemini API (Chưa gọi Code Tools)")

# Đưa model và memory chat vào session_state của Streamlit
if "model" not in st.session_state:
    st.session_state.model = init_model()
    
if "chat_session" not in st.session_state:
    # Bắt đầu 1 session hội thoại (tự động nhớ quá khứ)
    st.session_state.chat_session = st.session_state.model.start_chat(history=[])

# ----------------- Giao diện Chat -----------------
# Render lại lịch sử chat khi reload
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Input từ người dùng
if prompt := st.chat_input("Hãy mô tả biểu hiện của xe... (VD: xe tự nhiên hú lên rồi bốc khói)"):
    # Render câu của user ngay lên giao diện
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Gọi tới Gemini API (gửi tin nhắn và nhận về theo dạng dữ liệu stream)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Gửi câu hỏi vào API, bật cờ stream=True để chữ chạy mượt hơn
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
                    
            # Xóa con trỏ nhấp nháy ở cuối
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Đã có lỗi từ API: {e}")
