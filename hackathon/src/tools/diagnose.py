from __future__ import annotations

import json
import re
from pathlib import Path

from langchain_core.tools import tool

# ---------------------------------------------------------------------------
# Load data từ JSON
# ---------------------------------------------------------------------------

_DATA_PATH = Path(__file__).parent.parent / "data" / "vinfast_error_data.json"
def _load_data() -> tuple[list[dict], dict]:
    with open(_DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    return raw["ERROR_DATA"], raw["SEVERITY_LABEL"]

try:
    ERROR_DATA, SEVERITY_LABEL = _load_data()
except FileNotFoundError:
    raise FileNotFoundError(
        f"❌ Không tìm thấy file: {_DATA_PATH}\n"
        "Hãy đảm bảo file nằm ở: data/vinfast_error_data.json"
    )
except (KeyError, json.JSONDecodeError) as e:
    raise ValueError(f"❌ File JSON bị lỗi: {e}")


# ---------------------------------------------------------------------------
# Keyword Search
# ---------------------------------------------------------------------------

SYNONYM_MAP = {
    "phanh": ["phanh", "thắng", "hãm", "dừng"],
    "không ăn": ["không ăn", "không hoạt động", "kém", "yếu", "mất tác dụng"],
    "kêu": ["kêu", "tiếng", "âm thanh", "lạch cạch", "cọc cạch", "ken két"],
    "nóng": ["nóng", "nhiệt", "quá nhiệt", "nóng bỏng"],
    "yếu": ["yếu", "chậm", "ì", "không lên"],
    "rung": ["rung", "giật", "lắc"],
    "màn hình": ["màn hình", "hiển thị", "screen"],
    "sạc": ["sạc", "charge", "nạp điện"],
    "khởi động": ["khởi động", "nổ máy", "start"],
}


def _expand_query(query: str) -> str:
    expanded = query.lower()
    for key, synonyms in SYNONYM_MAP.items():
        for syn in synonyms:
            if syn in expanded:
                expanded += " " + " ".join(synonyms)
                break
    return expanded


def _keyword_search(query: str, top_k: int = 1) -> list[str]:
    expanded_query = _expand_query(query)
    tokens = set(re.split(r"\s+", expanded_query.lower()))
    ranked = []
    for err in ERROR_DATA:
        texts = " ".join(
            [err["description"], err["title"], err["error_code"]] + err["symptoms"]
        ).lower()
        overlap = sum(1 for t in tokens if t in texts)
        ranked.append((err["error_code"], overlap))

    ranked.sort(key=lambda x: x[1], reverse=True)

    if not ranked:
        return []

    best_score = ranked[0][1]
    if best_score == 0:
        return []

    threshold = max(1, best_score * 0.5)
    return [
        code for code, score in ranked[:top_k]
        if score >= threshold
    ]


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _get_error_by_code(code: str) -> dict | None:
    code = code.upper().strip()
    for err in ERROR_DATA:
        if err["error_code"] == code:
            return err
    return None


def _format_error(err: dict) -> str:
    sev = SEVERITY_LABEL.get(err["severity"], err["severity"])

    causes_str = "\n".join(
        f"  • {c['cause']} ({c['confidence']:.0%})" for c in err["causes"]
    )
    symptoms_str = "\n".join(f"  • {s}" for s in err["symptoms"])
    fixes_str = "\n".join(
        f"  {i+1}. {f}" for i, f in enumerate(err["fix_suggestions"])
    )

    return (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🚗 [{err['error_code']}] {err['title']}\n"
        f"📋 Mức độ nghiêm trọng: {sev}\n"
        f"📝 Mô tả: {err['description']}\n\n"
        f"⚠️  Triệu chứng thường gặp:\n{symptoms_str}\n\n"
        f"🔍 Nguyên nhân có thể:\n{causes_str}\n\n"
        f"🛠️  Cách xử lý:\n{fixes_str}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )


# ---------------------------------------------------------------------------
# LangChain Tools
# ---------------------------------------------------------------------------

@tool
def lookup_error_by_code(error_code: str) -> str:
    """
    Tra cứu thông tin lỗi VinFast theo mã lỗi chính xác.
    Ví dụ: BEV001, BAT002, ADAS003, SCR004, ELE005, SUS006, BRK007, STR008.

    Args:
        error_code: Mã lỗi (ví dụ 'BEV001').

    Returns:
        Thông tin chi tiết về lỗi đó, hoặc thông báo không tìm thấy.
    """
    err = _get_error_by_code(error_code)
    if err is None:
        return (
            f"❌ Không tìm thấy mã lỗi '{error_code}' trong cơ sở dữ liệu. "
            "Vui lòng kiểm tra lại hoặc mô tả triệu chứng để tôi hỗ trợ tìm kiếm."
        )
    return _format_error(err)


@tool
def search_error_by_symptom(symptom_description: str, top_k: int = 1) -> str:
    """
    Tìm kiếm lỗi VinFast dựa trên mô tả triệu chứng của khách hàng.
    Ví dụ: 'xe chạy yếu', 'pin nóng', 'xe kêu lạch cạch', 'phanh không ăn'.

    Args:
        symptom_description: Mô tả triệu chứng bằng ngôn ngữ tự nhiên.
        top_k: Số kết quả trả về tối đa (mặc định 1).

    Returns:
        Lỗi phù hợp nhất kèm thông tin chi tiết.
    """
    top_k = max(1, min(top_k, 5))

    codes = _keyword_search(symptom_description, top_k=top_k)
    results = []
    for code in codes:
        err = _get_error_by_code(code)
        if err:
            results.append(err)

    if not results:
        return (
            "❌ Không tìm thấy lỗi nào khớp với triệu chứng bạn mô tả. "
            "Vui lòng cung cấp thêm thông tin hoặc liên hệ tổng đài VinFast: 1800 2345."
        )

    lines = [
        f"🔎 Tìm thấy {len(results)} kết quả phù hợp với triệu chứng:\n"
        f'"{symptom_description}"\n'
    ]
    for err in results:
        lines.append(_format_error(err))

    return "\n\n".join(lines)


@tool
def get_emergency_action(error_code: str) -> str:
    """
    Lấy hướng dẫn xử lý khẩn cấp cho mã lỗi nghiêm trọng (critical/high).
    Dùng khi khách hàng đang trong tình huống cần xử lý ngay.

    Args:
        error_code: Mã lỗi cần tra cứu.

    Returns:
        Các bước xử lý khẩn cấp.
    """
    err = _get_error_by_code(error_code)
    if err is None:
        return f"❌ Không tìm thấy mã lỗi '{error_code}'."

    sev = err["severity"]
    if sev not in ("critical", "high"):
        return (
            f"ℹ️ Mã lỗi {error_code} có mức độ {SEVERITY_LABEL.get(sev, sev)}, "
            "không yêu cầu xử lý khẩn cấp. "
            "Tuy nhiên bạn vẫn nên đưa xe đi kiểm tra sớm."
        )

    fixes = "\n".join(
        f"  {i+1}. {f}" for i, f in enumerate(err["fix_suggestions"])
    )
    urgent_note = (
        "🚨 DỪNG XE NGAY VÀ GỌI CỨU HỘ: 1800 2345"
        if sev == "critical"
        else "⚠️ Không tiếp tục di chuyển xa, liên hệ VinFast: 1800 2345"
    )

    return (
        f"🚨 XỬ LÝ KHẨN CẤP — [{error_code}] {err['title']}\n"
        f"Mức độ: {SEVERITY_LABEL.get(sev)}\n\n"
        f"{urgent_note}\n\n"
        f"Các bước xử lý ngay:\n{fixes}"
    )


@tool
def diagnose(description: str, car_history: str = "") -> str:
    """
    Dự đoán lỗi dựa trên triệu chứng và ngữ cảnh lịch sử xe (ODO, lần bảo trì cuối).
    Đây là tool chính thức được sử dụng để đưa ra chẩn đoán lỗi.
    
    Args:
        description: Mô tả triệu chứng bằng ngôn ngữ tự nhiên từ người dùng.
        car_history: Lịch sử bảo dưỡng của xe (ODO, model, các lần bảo dưỡng gần nhất).
        
    Returns:
        Kết quả chẩn đoán lỗi kèm theo thông tin lịch sử xe được xử lý.
    """
    # Gọi hàm search internal
    result = search_error_by_symptom.invoke({"symptom_description": description, "top_k": 2})
    
    if "❌ Không tìm thấy" in result:
        return result
        
    return f"THÔNG TIN XE: {car_history}\n\n{result}"

# Danh sách tools export cho agent
VINFAST_TOOLS = [
    lookup_error_by_code,
    diagnose,
    get_emergency_action,
]