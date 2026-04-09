from langchain.tools import tool
from typing import List, Dict
import json

@tool
def search_mechanic(garage_id: str) -> List[Dict]:
    """
Tìm thợ sửa xe gần vị trí người dùng nhất và còn lịch trống,
dựa trên mô tả sự cố của xe và thời gian yêu cầu. Có thể dùng trong cả trường hợp bình thường hoặc sau khi xử lý tình huống khẩn cấp.

Args:
    garage_id (str): ID của garage cần tìm kiếm thợ sửa xe.

Returns:
    List[Dict]: Danh sách thợ phù hợp (bao gồm tên, số điện thoại, khoảng cách, thời gian hỗ trợ).
"""

    # =========================
    # 1. Đọc dữ liệu từ file .txt
    # =========================
    import os
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'mock_mechanics.json')
    with open(data_path, "r", encoding="utf-8") as file:
        data = json.load(file)  # parse JSON từ txt

    results = []

    # =========================
    # 2. Duyệt qua data
    # =========================
    results = []

    # lấy danh sách mechanics của garage
    mechanics_list = data.get(garage_id, [])

    # lọc available
    for mech in mechanics_list:
        if mech.get("status") == "available":
            results.append({
                "id": mech["id"],
                "name": mech["name"],
                "garage_name": mech["garage_name"],
                "experience_years": mech["experience_years"],
                "rating": mech["rating"]
            })

    return results


