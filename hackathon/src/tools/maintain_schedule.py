import random
from langchain_core.tools import tool

@tool
def maintain_schedule(garage_id: str, service_type: str, is_emergency: bool = False, user_location: str = "") -> str:
    """
    Đặt lịch hẹn sửa chữa xe với gara hoặc yêu cầu cứu hộ khẩn cấp.
    Sử dụng tool này khi người dùng đã đồng ý chọn một gara, hoặc khi hệ thống phát hiện tình trạng khẩn cấp cần gọi xe cứu hộ ngay.

    Args:
        garage_id (str): Mã ID hoặc tên của gara được gửi yêu cầu.
        service_type (str): Loại dịch vụ cần thực hiện (ví dụ: 'Sửa chữa động cơ', 'Thay lốp', 'Kiểm tra phanh').
        is_emergency (bool): Đánh dấu True nếu đây là trường hợp khẩn cấp, nguy hiểm (ví dụ: mất phanh, bốc khói, cháy, tai nạn, chết máy giữa đường).

    Returns:
        str: Thông báo xác nhận đặt lịch hẹn (bảo gồm thông tin gara, dịch vụ) kèm theo thời gian kỹ thuật viên / xe kéo dự kiến đến nơi.
    """
    # Dựa theo rule trong plan.md:
    # Nếu is_emergency, ưu tiên auto-select "Cứu hộ/Xe kéo" thay vì dịch vụ thông thường.
    if is_emergency:
        final_service = "Cứu hộ/Xe kéo"
        # Trường hợp khẩn cấp, ưu tiên thời gian tới nhanh hơn (10 - 25 phút)
        eta_minutes = random.randint(10, 25)
        
        return (
            f"🚨 ĐẶT LỊCH CỨU HỘ KHẨN CẤP THÀNH CÔNG\n"
            f"- Gara tiếp nhận: {garage_id}\n"
            f"- Dịch vụ điều động: **{final_service}**\n"
            f"- Vị trí cứu hộ: **{user_location if user_location else 'Chưa cung cấp'}**\n"
            f"- Trạng thái: Đã kết nối khẩn cấp, xe cứu hộ đang di chuyển tới vị trí của bạn.\n"
            f"- Thời gian dự kiến đến nơi: **{eta_minutes} phút**.\n"
            f"\n*Lưu ý an toàn: Vui lòng bật đèn cảnh báo nguy hiểm, giữ khoảng cách an toàn với phương tiện và chú ý điện thoại liên hệ!*"
        )
    else:
        final_service = service_type
        # Đặt lịch bình thường, user sẽ tự lái xe đến gara, mô phỏng thời gian gara sẵn sàng
        eta_minutes = random.randint(30, 120)
        
        return (
            f"✅ ĐẶT LỊCH SỬA CHỮA THÀNH CÔNG\n"
            f"- Gara tiếp nhận: {garage_id}\n"
            f"- Dịch vụ: **{final_service}**\n"
            f"- Trạng thái: Đã xác nhận trên hệ thống gara.\n"
            f"- Thời gian gara sẵn sàng tiếp nhận xe: khoảng **{eta_minutes} phút** nữa.\n"
            f"\n*Bạn có thể xuất phát đến gara theo thời gian trên. Xin cảm ơn!*"
        )

if __name__ == "__main__":
    # Script test thử tool 
    print("--- Test Normal ---")
    print(maintain_schedule.invoke({"garage_id": "GARA_01 - VinFast Thảo Điền", "service_type": "Bảo dưỡng định kỳ", "is_emergency": False}))
    
    print("\n--- Test Emergency ---")
    print(maintain_schedule.invoke({"garage_id": "GARA_02 - Cứu hộ 24/7", "service_type": "Thay bình ắc quy", "is_emergency": True}))
