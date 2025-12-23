# 📅 AI Personal Assistant - Trợ lý Lịch trình Thông minh

Dự án xây dựng một AI Agent có khả năng quản lý thời gian, đặt lịch họp và nhắc việc tự động (Real-time Reminder) bằng ngôn ngữ tự nhiên. Hệ thống sử dụng **LangGraph** để quản lý luồng hội thoại và **GPT-4o** để xử lý logic thời gian phức tạp.

---

## 🚀 Tính năng nổi bật

1.  **Hiểu ngôn ngữ tự nhiên (NLU):**
    *   Tự động trích xuất ngày giờ từ câu nói (VD: *"Thứ 6 tuần sau"* -> `2024-05-31`).
    *   Sử dụng kỹ thuật **Time Context Injection** để tránh lỗi ảo giác thời gian của AI.

2.  **Quản lý Lịch & Nhắc việc:**
    *   Phân biệt rõ ràng giữa **Sự kiện (Event)** và **Báo thức (Reminder)**.
    *   Tool `add_calendar_event`: Dành cho lịch họp, công tác.
    *   Tool `set_reminder`: Dành cho các việc cần thông báo ngay.

3.  **Hệ thống Nhắc việc Thời gian thực (Real-time Alert):**
    *   Sử dụng **Background Thread** chạy song song để kiểm tra thời gian.
    *   Tự động đẩy thông báo `🔔 REMINDER ALERT` lên màn hình ngay khi đến giờ hẹn.

4.  **Kiến trúc LangGraph:**
    *   Quản lý vòng lặp tác vụ: Agent -> Tool -> Agent.
    *   Tự động vẽ sơ đồ luồng xử lý ra file `graph_structure.png`.

---

## 🛠️ Hướng dẫn Cài đặt & Thiết lập Môi trường

Dự án này khuyến nghị chạy trên **Môi trường ảo (Virtual Environment)** để tránh xung đột thư viện.

### Bước 1: Khởi tạo môi trường ảo (Venv)
Mở Terminal (hoặc CMD/PowerShell) tại thư mục dự án và chạy lệnh:
python -m venv venv
### Bước 2: Kích hoạt môi trường
Bạn bắt buộc phải kích hoạt môi trường trước khi cài đặt thư viện.
Đối với Windows:
.\venv\Scripts\activate
Đối với macOS / Linux:
source venv/bin/activate
Dấu hiệu thành công: Bạn sẽ thấy chữ (venv) xuất hiện ở đầu dòng lệnh.
### Bước 3: Cài đặt thư viện phụ thuộc
Sau khi kích hoạt (venv), chạy lệnh sau để tải các gói cần thiết:
pip install langchain langchain-openai langgraph python-dotenv grandalf
### Bước 4: Cấu hình API Key (.env)
Tạo một file có tên .env (không có tên, chỉ có đuôi file) tại thư mục gốc và điền thông tin sau:
Env
# Bắt buộc: Key OpenAI để chạy trí tuệ nhân tạo
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx

# Tùy chọn: LangSmith để theo dõi luồng chạy (Monitoring)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2-xxxxxxxxxxxxxxxxxxxxxxx
# 🏃 Hướng dẫn chạy chương trình
Đảm bảo bạn vẫn đang ở trong môi trường ảo (venv). Chạy lệnh:
python main.py
# Các câu lệnh mẫu (Demo)
Đặt lịch họp (Sự kiện thụ động):
"Đặt lịch họp nhóm đồ án vào 9h sáng thứ Sáu tuần này."
Đặt báo thức (Nhắc việc chủ động):
"Nhắc tôi uống thuốc sau 2 phút nữa."
(Sau đó hãy chờ 2 phút và quan sát Terminal tự động hiện thông báo)
Xem danh sách:
"Kiểm tra lịch trình của tôi."
Thoát:
"quit"
# 📂 Cấu trúc dự án
Text
├── venv/                # Thư mục môi trường ảo (Do máy tự tạo)
├── main.py              # Source code chính (Logic AI & Threading)
├── .env                 # Chứa API Keys (Bảo mật - Không upload lên Git)
├── README.md            # Tài liệu hướng dẫn
├── graph_structure.png  # Ảnh sơ đồ luồng (Tự sinh khi chạy code)
└── requirements.txt     # (Optional) Danh sách thư viện
# ❓ Xử lý lỗi thường gặp
Lỗi ModuleNotFoundError:
Nguyên nhân: Bạn chưa kích hoạt môi trường ảo hoặc chưa cài thư viện.
Khắc phục: Xem lại Bước 2 và Bước 3.
Lỗi không vẽ được ảnh Graph:
Code sẽ tự động chuyển sang chế độ in mã Text nếu máy thiếu thư viện đồ họa hệ thống. Bạn có thể copy mã đó dán vào Mermaid Live để lấy ảnh.
Lỗi RateLimitError:
Nguyên nhân: Tài khoản OpenAI hết tiền (Credit).
Khắc phục: Kiểm tra Billing tại platform.openai.com.
Người thực hiện: [Tên của bạn]