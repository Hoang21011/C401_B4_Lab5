import os
import json
from dotenv import load_dotenv

# Load env before importing agent
load_dotenv()

from agent import get_agent

def create_car_history_string(car_data: dict) -> str:
    return f"Model: {car_data.get('model', 'Unknown')}, ODO: {car_data.get('odo', 'Unknown')}, History: {car_data.get('history', 'Unknown')}"

def main():
    print("========================================")
    print("   VINFAST VEHICLE AI ASSISTANT (CLI)   ")
    print("========================================")
    
    # Load car history mock data
    history_path = os.path.join(os.path.dirname(__file__), "data", "car_history.json")
    with open(history_path, "r", encoding="utf-8") as f:
        car_histories = json.load(f)

    print("\nChọn hồ sơ xe để khởi tạo (Nhập VIN001 hoặc VIN002):")
    for vin, details in car_histories.items():
        print(f" - {vin}: {details['model']} | ODO: {details['odo']}")
        
    selected_vin = input("\nMã xe của bạn: ").strip().upper()
    if selected_vin not in car_histories:
        print("Không tìm thấy mã xe, mặc định chọn VIN001.")
        selected_vin = "VIN001"
        
    car_profile_str = create_car_history_string(car_histories[selected_vin])
    print(f"\n[ HỆ THỐNG ĐÃ TẢI LỊCH SỬ XE: {car_profile_str} ]\n")
    
    print("Vivi: Chào bạn, tôi là Vivi trợ lý kỹ thuật thông minh của VinFast. Xe của bạn đang gặp vấn đề gì?")
    
    agent = get_agent()
    # Configuration for MemorySaver
    config = {"configurable": {"thread_id": "1"}}
    
    # Inject context system-like note as first message
    initial_message = {"role": "user", "content": f"Lưu ý: Thông tin lịch sử xe của tôi là: {car_profile_str}. Bạn không cần nhắc lại thông tin này trừ khi cần thiết phục vụ chẩn đoán. Ghi nhớ nó ở dưới background."}
    
    # Run silently once to stash context
    for _ in agent.stream({"messages": [initial_message]}, config=config):
        pass

    while True:
        try:
            user_input = input("\nBạn: ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Tạm biệt!")
                break
                
            # Stream events, now utilizing LangGraph MemorySaver correctly
            final_response = ""
            for event in agent.stream({"messages": [{"role": "user", "content": user_input}]}, config=config):
                
                if "agent" in event:
                    msg = event['agent']['messages'][-1]
                    
                    if msg.tool_calls:
                        print("\n" + "="*50)
                        print("🛠️  [TOOL CALLED]")
                        for tool_call in msg.tool_calls:
                            print(f" - Tên: {tool_call['name']}")
                            print(f" - Tham số: {json.dumps(tool_call['args'], ensure_ascii=False, indent=2)}")
                        print("="*50)
                        
                    if msg.content:
                        if isinstance(msg.content, str):
                            final_response = msg.content
                        elif isinstance(msg.content, list):
                            # Handle Gemini returning a list of content blocks
                            texts = []
                            for block in msg.content:
                                if isinstance(block, str):
                                    texts.append(block)
                                elif isinstance(block, dict) and "text" in block:
                                    texts.append(block["text"])
                            final_response = " ".join(texts)
                        else:
                            final_response = str(msg.content)
                        
                elif "tools" in event:
                    # In our custom execute_tools node, we return multiple tool messages if there are multiple calls
                    for msg in event['tools']['messages']:
                        print("\n" + "="*50)
                        print(f"📤 [TOOL OUTPUT - {msg.name}]:")
                        print(msg.content)
                        print("="*50)
            
            # Print the final synthesized string response from Gemini
            print(f"\nVivi: {final_response}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n[LỖI]: {e}")

if __name__ == "__main__":
    main()
