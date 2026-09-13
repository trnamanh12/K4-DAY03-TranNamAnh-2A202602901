# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Trần Nam Anh  
> **Mã Sinh Viên / Mã Học viên:** 2A202602901  
> **Chủ đề Lựa chọn:**  Trợ lý Quản lý Thư viện & Tài liệu: Tra cứu vị trí sách, tình trạng mượn/trả và gia hạn tài liệu.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 3/ 5 | Bài toán có các tác vụ đòi hỏi suy luận tuần tự nhiều bước (ví dụ: TC04 yêu cầu kiểm tra tình trạng sách trước, nếu đang mượn thì mới tính toán thời hạn và kích hoạt bước gia hạn tiếp theo). |
| **2. Tool Interaction** | 4/ 5 | Hệ thống bắt buộc phải tương tác với MCP Server bên ngoài qua các công cụ chuyên biệt (`get_book_location`, `get_book_status`, `renew_book_loan`) để truy xuất và cập nhật cơ sở dữ liệu sách theo thời gian thực. |
| **3. Dynamic Decision** | 4/ 5 | Bước kế tiếp phụ thuộc hoàn toàn vào kết quả quan sát (Observation) từ Tool trước: Nếu sách đang mượn (`BORROWED`) thì cho phép gia hạn; nếu sách sẵn sàng (`AVAILABLE`) hoặc không tồn tại (`NOT_FOUND`) thì dừng và trả về thông báo phù hợp. |
| **4. Long Horizon Goal** | 3/ 5 | Agent cần duy trì mục tiêu của người dùng xuyên suốt chuỗi đối thoại (từ tra cứu tình trạng đến thực hiện gia hạn thành công) và kiểm soát trạng thái giao dịch mượn/trả hoàn tất. |
| **TỔNG ĐIỂM AGENTIC FIT** | **14/ 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
  {
    "step": 1,
    "query": "Kiểm tra giúp tôi tình trạng cuốn sách có mã BK003 xem có ai đang mượn không.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "get_book_status",
    "arguments": {
      "book_id": "BK003"
    },
    "observation": {
      "status": "SUCCESS",
      "book_id": "BK003",
      "title": "Lược Sử Loài Người",
      "circulation_status": "BORROWED",
      "display_status": "Đang được mượn",
      "due_date": "2026-09-25",
      "message": "Sách 'Lược Sử Loài Người' hiện đang được mượn. Ngày hẹn trả hiện tại: 2026-09-25."
    },
    "latency_ms": 930.51
  },
  {
    "step": 2,
    "query": "Kiểm tra giúp tôi tình trạng cuốn sách có mã BK003 xem có ai đang mượn không.",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Sách 'Lược Sử Loài Người' hiện đang được mượn. Ngày hẹn trả hiện tại: 2026-09-25.",
    "latency_ms": 10.0
  }
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [ x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt.
- **Kết quả đẩy Repo nộp bài:** [ x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
