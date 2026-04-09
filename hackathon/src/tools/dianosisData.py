"""
mockData.py - VinFast EV Error Database
"""

ERROR_DATA = [
    {
        "error_code": "BEV001",
        "title": "Motor Power Reduction",
        "description": "Hệ thống động cơ điện bị giảm công suất bất thường.",
        "symptoms": [
            "Xe tăng tốc yếu",
            "Hiện biểu tượng con rùa",
            "Xe bị giật nhẹ khi chạy",
            "Xe không tăng tốc được dù đạp ga",
            "Cảm giác xe bị kéo ngược khi tăng tốc",
        ],
        "causes": [
            {"cause": "Lỗi bộ điều khiển động cơ", "confidence": 0.6},
            {"cause": "Pin yếu hoặc quá nhiệt", "confidence": 0.3},
            {"cause": "Lỗi phần mềm", "confidence": 0.1},
        ],
        "severity": "high",
        "fix_suggestions": [
            "Tắt xe và khởi động lại",
            "Không tiếp tục chạy xa",
            "Đưa xe đến trung tâm VinFast",
        ],
    },
    {
        "error_code": "BAT002",
        "title": "Battery Overheat",
        "description": "Pin đang ở nhiệt độ cao bất thường.",
        "symptoms": [
            "Cảnh báo pin nóng",
            "Xe tự giảm công suất",
            "Quạt làm mát chạy mạnh",
            "Mùi khét hoặc mùi lạ phát ra từ gầm xe",
            "Xe nóng bất thường dù không chạy lâu",
        ],
        "causes": [
            {"cause": "Sạc trong môi trường nhiệt độ cao", "confidence": 0.5},
            {"cause": "Hệ thống làm mát pin lỗi", "confidence": 0.4},
            {"cause": "Pin xuống cấp", "confidence": 0.1},
        ],
        "severity": "critical",
        "fix_suggestions": [
            "Dừng xe ngay",
            "Để xe nguội tự nhiên",
            "Không tiếp tục sạc",
            "Gọi cứu hộ nếu cần",
        ],
    },
    {
        "error_code": "ADAS003",
        "title": "Sensor Malfunction",
        "description": "Lỗi cảm biến hỗ trợ lái (ADAS).",
        "symptoms": [
            "Cảnh báo hệ thống hỗ trợ lái",
            "Không dùng được cruise control",
            "Camera/cảm biến không hoạt động",
            "Màn hình hiển thị lỗi camera trước hoặc sau",
            "Hệ thống phanh tự động không phản hồi",
        ],
        "causes": [
            {"cause": "Camera bị bẩn", "confidence": 0.5},
            {"cause": "Lỗi phần mềm", "confidence": 0.3},
            {"cause": "Hỏng cảm biến", "confidence": 0.2},
        ],
        "severity": "medium",
        "fix_suggestions": [
            "Lau sạch camera và cảm biến",
            "Khởi động lại xe",
            "Cập nhật phần mềm",
        ],
    },
    {
        "error_code": "SCR004",
        "title": "Charging Failure",
        "description": "Xe không thể sạc pin.",
        "symptoms": [
            "Không nhận sạc",
            "Báo lỗi khi cắm sạc",
            "Sạc ngắt liên tục",
            "Đèn sạc không sáng khi cắm vào",
            "Phần trăm pin không tăng dù cắm sạc lâu",
        ],
        "causes": [
            {"cause": "Lỗi trụ sạc", "confidence": 0.4},
            {"cause": "Cổng sạc bẩn hoặc hỏng", "confidence": 0.3},
            {"cause": "Lỗi module sạc trên xe", "confidence": 0.3},
        ],
        "severity": "high",
        "fix_suggestions": [
            "Thử trụ sạc khác",
            "Kiểm tra cổng sạc",
            "Mang xe đi kiểm tra",
        ],
    },
    {
        "error_code": "ELE005",
        "title": "12V Battery Low",
        "description": "Ắc quy 12V yếu hoặc sắp hết.",
        "symptoms": [
            "Xe không khởi động",
            "Màn hình chập chờn",
            "Nhiều lỗi hệ thống xuất hiện cùng lúc",
            "Đèn trong xe tự tắt hoặc yếu đi",
            "Còi xe kêu nhỏ hoặc không kêu",
        ],
        "causes": [
            {"cause": "Ắc quy yếu", "confidence": 0.7},
            {"cause": "Xe để lâu không sử dụng", "confidence": 0.2},
            {"cause": "Hệ thống sạc lỗi", "confidence": 0.1},
        ],
        "severity": "medium",
        "fix_suggestions": [
            "Sạc hoặc thay ắc quy 12V",
            "Khởi động lại hệ thống",
            "Không để xe lâu không chạy",
        ],
    },
    {
        "error_code": "SUS006",
        "title": "Suspension Noise",
        "description": "Hệ thống treo hoặc gầm xe phát ra tiếng kêu bất thường khi di chuyển.",
        "symptoms": [
            "Xe kêu lạch cạch khi đi qua ổ gà",
            "Tiếng gõ lộc cộc phát ra từ gầm xe",
            "Xe rung lắc bất thường khi đi tốc độ thấp",
            "Tiếng kêu cọ xát khi đánh lái",
            "Vô lăng rung khi chạy trên đường xấu",
            "Tiếng ken két khi phanh hoặc qua cua",
        ],
        "causes": [
            {"cause": "Cao su giảm chấn bị mòn hoặc nứt", "confidence": 0.4},
            {"cause": "Bulong gầm bị lỏng", "confidence": 0.3},
            {"cause": "Thanh ổn định (stabilizer) bị mòn", "confidence": 0.2},
            {"cause": "Lốp xe không đều hoặc mất cân bằng", "confidence": 0.1},
        ],
        "severity": "medium",
        "fix_suggestions": [
            "Kiểm tra và siết lại bulong gầm",
            "Đưa xe đến trung tâm để kiểm tra hệ thống treo",
            "Không chạy tốc độ cao khi chưa kiểm tra",
            "Kiểm tra áp suất và cân bằng lốp",
        ],
    },
    {
        "error_code": "BRK007",
        "title": "Brake System Warning",
        "description": "Hệ thống phanh có dấu hiệu bất thường, cần kiểm tra ngay.",
        "symptoms": [
            "Phanh kêu ken két khi đạp",
            "Xe không dừng ngay khi đạp phanh gấp",
            "Cần đạp phanh sâu hơn bình thường",
            "Cảm giác phanh bị rung hoặc giật",
            "Đèn cảnh báo phanh sáng trên bảng đồng hồ",
            "Xe bị lệch sang một bên khi phanh",
        ],
        "causes": [
            {"cause": "Má phanh mòn", "confidence": 0.5},
            {"cause": "Đĩa phanh bị cong hoặc trầy xước", "confidence": 0.3},
            {"cause": "Dầu phanh thấp hoặc rò rỉ", "confidence": 0.2},
        ],
        "severity": "critical",
        "fix_suggestions": [
            "Dừng xe ngay nếu phanh không ăn",
            "Không tiếp tục lái khi chưa kiểm tra phanh",
            "Gọi cứu hộ: 1800 2345",
            "Đưa xe đến trung tâm VinFast kiểm tra ngay",
        ],
    },
    {
        "error_code": "STR008",
        "title": "Steering System Error",
        "description": "Hệ thống lái điện tử gặp sự cố.",
        "symptoms": [
            "Vô lăng nặng bất thường",
            "Xe khó đánh lái hoặc lái bị đơ",
            "Cảnh báo hệ thống lái trên màn hình",
            "Vô lăng bị rung khi đi thẳng",
            "Xe tự lệch hướng khi không đánh lái",
        ],
        "causes": [
            {"cause": "Lỗi mô-tơ lái điện (EPS)", "confidence": 0.5},
            {"cause": "Cảm biến góc lái lỗi", "confidence": 0.3},
            {"cause": "Lỗi phần mềm điều khiển lái", "confidence": 0.2},
        ],
        "severity": "high",
        "fix_suggestions": [
            "Tắt và khởi động lại xe",
            "Không chạy tốc độ cao",
            "Đưa xe đến trung tâm VinFast ngay",
        ],
    },
]

SEVERITY_LABEL = {
    "critical": "🔴 NGHIÊM TRỌNG",
    "high":     "🟠 CAO",
    "medium":   "🟡 TRUNG BÌNH",
    "low":      "🟢 THẤP",
}