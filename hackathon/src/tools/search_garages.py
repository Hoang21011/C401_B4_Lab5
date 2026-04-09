from langchain.tools import tool
import json


@tool
def search_garages(location: str) -> str:
    """
    Tìm danh sách garage theo quận/huyện hoặc thành phố.

    Args:
        location (str): ví dụ "Thanh Xuân", "Hà Nội"

    Returns:
        str: danh sách garage format đẹp
    """

    with open("mock_garages.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for city, districts in data.items():

        # Nếu nhập thành phố
        if city.lower() == location.lower():
            for district, garages in districts.items():
                for garage in garages:
                    results.append(
                        f"{garage['name']} ({garage['id']}) | "
                        f"{district}, {city} | "
                        f"{garage['open_hours']} | "
                        f"{garage['current_status']['cars_in_service']} | "
                        f"{garage['current_status']['cars_waiting']} | "
                        f"{garage['current_status']['total_mechanics']}"
                    )

        # Nếu nhập quận/huyện
        for district, garages in districts.items():
            if district.lower() == location.lower():
                for garage in garages:
                    results.append(
                        f"{garage['name']} ({garage['id']}) \n "
                        f"{district}, {city} | "
                        f"{garage['open_hours']} | "
                        f"{garage['current_status']['cars_in_service']} | "
                        f"{garage['current_status']['cars_waiting']} | "
                        f"{garage['current_status']['total_mechanics']}"
                    )

    if not results:
        return f"Không tìm thấy garage tại '{location}'."

    return "\n".join(results)