# 📅 AI Personal Assistant – Trợ lý Lịch trình Thông minh

Dự án xây dựng một AI Agent có khả năng quản lý thời gian, đặt lịch họp và nhắc việc tự động (Real-time Reminder) bằng ngôn ngữ tự nhiên. Hệ thống sử dụng **LangGraph** để quản lý luồng hội thoại và **GPT-4o** để xử lý logic thời gian phức tạp.

---

## 🚀 Tính năng nổi bật

### 1️⃣ Hiểu ngôn ngữ tự nhiên (NLU)

- Tự động trích xuất ngày giờ từ câu nói (VD: *"Thứ 6 tuần sau"* → `2024-05-31`)
- Sử dụng kỹ thuật **Time Context Injection** để tránh lỗi ảo giác thời gian của AI

### 2️⃣ Quản lý Lịch & Nhắc việc

- Phân biệt rõ ràng giữa **Sự kiện (Event)** và **Báo thức (Reminder)**
- `add_calendar_event`: Dành cho lịch họp, công tác
- `set_reminder`: Dành cho các việc cần thông báo ngay

### 3️⃣ Hệ thống Nhắc việc Thời gian thực (Real-time Alert)

- Sử dụng **Background Thread** chạy song song để kiểm tra thời gian
- Tự động đẩy thông báo `🔔 REMINDER ALERT` lên màn hình ngay khi đến giờ hẹn

### 4️⃣ Kiến trúc LangGraph

- Quản lý vòng lặp tác vụ: `Agent → Tool → Agent`
- Tự động vẽ sơ đồ luồng xử lý ra file `graph_structure.png`

---

## 🛠️ Hướng dẫn Cài đặt & Thiết lập Môi trường

Dự án khuyến nghị chạy trên **Virtual Environment (venv)** để tránh xung đột thư viện.

### Bước 1: Khởi tạo môi trường ảo

- python -m venv venv
### Bước 2: Kích hoạt môi trường
Windows (CMD / PowerShell):

- .\venv\Scripts\activate
macOS / Linux:
- source venv/bin/activate
Dấu hiệu thành công: (venv) xuất hiện ở đầu dòng lệnh.

### Bước 3: Cài đặt thư viện phụ thuộc
- pip install langchain langchain-openai langgraph python-dotenv grandalf
### Bước 4: Cấu hình API Key
Tạo file .env tại thư mục gốc và thêm nội dung sau:

#### Bắt buộc: OpenAI API Key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx

#### Tùy chọn: LangSmith Monitoring
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2-xxxxxxxxxxxxxxxxxxxxxxx
⚠️ Không upload file .env lên GitHub.

## 🏃 Hướng dẫn chạy chương trình
Đảm bảo bạn đang ở trong môi trường (venv):
- python main.py
#### 💬 Các câu lệnh mẫu (Demo)
- Đặt lịch họp (Sự kiện thụ động):
"Đặt lịch họp nhóm đồ án vào 9h sáng thứ Sáu tuần này."
- Đặt báo thức (Nhắc việc chủ động):
"Nhắc tôi uống thuốc sau 2 phút nữa."
(Chờ 2 phút và quan sát Terminal tự động hiện thông báo)

- Xem danh sách:

Kiểm tra lịch trình của tôi.
-  Thoát:
"quit"

