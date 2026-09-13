"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Khai báo Tool Schemas và dữ liệu mock cho Trợ lý Quản lý Thư viện.

Trong phạm vi bài lab, ``book_id`` là mã duy nhất của từng bản sách
vật lý. ``location`` là vị trí kệ được chỉ định, kể cả khi sách
đang được mượn.
"""

import json
from datetime import date, timedelta
from typing import Any, Dict


# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "get_book_location",
        "description": (
            "Tra cứu vị trí kệ được chỉ định cho một bản sách "
            "bằng mã sách."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "book_id": {
                    "type": "string",
                    "description": "Mã duy nhất của bản sách, ví dụ 'BK001'.",
                }
            },
            "required": ["book_id"],
        },
    },
    {
        "name": "get_book_status",
        "description": (
            "Tra cứu tình trạng lưu thông của một bản sách và ngày hẹn "
            "trả hiện tại nếu sách đang được mượn."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "book_id": {
                    "type": "string",
                    "description": "Mã duy nhất của bản sách, ví dụ 'BK002'.",
                }
            },
            "required": ["book_id"],
        },
    },
    {
        "name": "renew_book_loan",
        "description": (
            "Gia hạn một bản sách đang được mượn thêm từ 1 đến 30 "
            "ngày, tính từ ngày hẹn trả hiện tại."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "book_id": {
                    "type": "string",
                    "description": "Mã duy nhất của bản sách, ví dụ 'BK002'.",
                },
                "extra_days": {
                    "type": "integer",
                    "description": "Số ngày muốn gia hạn (số nguyên từ 1 đến 30).",
                },
            },
            "required": ["book_id", "extra_days"],
        },
    },
]


# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "BK001": {
        "title": "Nhà Giả Kim",
        "circulation_status": "AVAILABLE",
        "due_date": None,
        "location": "Kệ A1 - Tầng 2",
    },
    "BK002": {
        "title": "Rừng Na Uy",
        "circulation_status": "BORROWED",
        "due_date": "2026-10-05",
        "location": "Kệ B3 - Tầng 1",
    },
    "BK003": {
        "title": "Lược Sử Loài Người",
        "circulation_status": "BORROWED",
        "due_date": "2026-09-25",
        "location": "Kệ C2 - Tầng 2",
    },
    "BK004": {
        "title": "Đắc Nhân Tâm",
        "circulation_status": "AVAILABLE",
        "due_date": None,
        "location": "Kệ A2 - Tầng 1",
    },
}


def _json_response(payload: Dict[str, Any]) -> str:
    """Mã hóa phản hồi Tool thành JSON tiếng Việt."""
    return json.dumps(payload, ensure_ascii=False)


def _normalize_book_id(book_id: Any) -> str | None:
    """Chuẩn hóa mã sách; trả về None nếu đầu vào không hợp lệ."""
    if not isinstance(book_id, str) or not book_id.strip():
        return None
    return book_id.strip().upper()


def execute_get_book_location(book_id: str) -> str:
    """Tra cứu vị trí kệ được chỉ định cho một bản sách."""
    normalized_id = _normalize_book_id(book_id)
    if normalized_id is None:
        return _json_response({
            "status": "INVALID_ARGUMENT",
            "message": "Mã sách phải là chuỗi không rỗng.",
        })

    book = MOCK_DATABASE.get(normalized_id)
    if book is None:
        return _json_response({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy sách có mã '{normalized_id}'.",
        })

    message = f"Sách được xếp tại {book['location']}."
    if book["circulation_status"] == "BORROWED":
        message = (
            f"Sách hiện đang được mượn; {book['location']} là vị trí "
            "lưu trữ khi sách được trả."
        )

    return _json_response({
        "status": "SUCCESS",
        "book_id": normalized_id,
        "title": book["title"],
        "location": book["location"],
        "circulation_status": book["circulation_status"],
        "message": message,
    })


def execute_get_book_status(book_id: str) -> str:
    """Tra cứu tình trạng lưu thông và hạn trả của một bản sách."""
    normalized_id = _normalize_book_id(book_id)
    if normalized_id is None:
        return _json_response({
            "status": "INVALID_ARGUMENT",
            "message": "Mã sách phải là chuỗi không rỗng.",
        })

    book = MOCK_DATABASE.get(normalized_id)
    if book is None:
        return _json_response({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy sách có mã '{normalized_id}'.",
        })

    is_available = book["circulation_status"] == "AVAILABLE"
    display_status = "Sẵn sàng" if is_available else "Đang được mượn"
    message = f"Sách '{book['title']}' hiện {display_status.lower()}."
    if not is_available:
        message = f"{message} Ngày hẹn trả hiện tại: {book['due_date']}."

    return _json_response({
        "status": "SUCCESS",
        "book_id": normalized_id,
        "title": book["title"],
        "circulation_status": book["circulation_status"],
        "display_status": display_status,
        "due_date": book["due_date"],
        "message": message,
    })


def execute_renew_book_loan(book_id: str, extra_days: int) -> str:
    """Gia hạn ngày trả của một bản sách đang được mượn."""
    normalized_id = _normalize_book_id(book_id)
    if normalized_id is None:
        return _json_response({
            "status": "INVALID_ARGUMENT",
            "message": "Mã sách phải là chuỗi không rỗng.",
        })

    book = MOCK_DATABASE.get(normalized_id)
    if book is None:
        return _json_response({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy sách có mã '{normalized_id}'.",
        })

    if book["circulation_status"] != "BORROWED":
        return _json_response({
            "status": "INVALID_STATE",
            "message": f"Không thể gia hạn vì sách {normalized_id} hiện chưa được mượn.",
        })

    if isinstance(extra_days, bool) or not isinstance(extra_days, int) or not 1 <= extra_days <= 30:
        return _json_response({
            "status": "INVALID_ARGUMENT",
            "message": "Số ngày gia hạn không hợp lệ; chỉ chấp nhận số nguyên từ 1 đến 30.",
        })

    old_due_date = book["due_date"]
    new_due_date = (date.fromisoformat(old_due_date) + timedelta(days=extra_days)).isoformat()
    book["due_date"] = new_due_date

    return _json_response({
        "status": "SUCCESS",
        "book_id": normalized_id,
        "title": book["title"],
        "old_due_date": old_due_date,
        "new_due_date": new_due_date,
        "extra_days": extra_days,
        "message": f"Gia hạn sách thành công đến ngày {new_due_date}.",
    })


# Router gọi tool thực tế
TOOL_ROUTER = {
    "get_book_location": execute_get_book_location,
    "get_book_status": execute_get_book_status,
    "renew_book_loan": execute_renew_book_loan,
}


def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Trung chuyển yêu cầu đến hàm thực thi Tool tương ứng."""
    if tool_name not in TOOL_ROUTER:
        return _json_response({
            "status": "UNKNOWN_TOOL",
            "message": f"Tool '{tool_name}' không tồn tại.",
        })

    try:
        return TOOL_ROUTER[tool_name](**arguments)
    except (TypeError, AttributeError) as error:
        return _json_response({
            "status": "INVALID_ARGUMENT",
            "message": f"Tham số gọi tool không hợp lệ: {error}",
        })
    except Exception as error:
        return _json_response({
            "status": "EXECUTION_ERROR",
            "message": f"Không thể thực thi tool: {error}",
        })
