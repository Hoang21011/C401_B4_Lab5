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

    with open("../data/mock_garages.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for city, districts in data.items():
        for district, garages in districts.items():

            # check match: city hoặc district
            if city.lower() == location.lower() or district.lower() == location.lower():

                for garage in garages:
                    results.append(
                        f"{garage['name']} ({garage['id']}) | "
                        f"{district}, {city} | "
                        f"{garage['open_hours']} | "
                        f"{garage['current_status']['cars_in_service']} | "
                        f"{garage['current_status']['cars_waiting']} | "
                        f"{garage['current_status']['total_mechanics']}"
                    )

    if not results:
        return f"Không tìm thấy garage tại '{location}'."

    return "\n".join(results)
