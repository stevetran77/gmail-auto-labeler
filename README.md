# 📬 Gmail Auto Labeler

Tự động phân loại, gắn nhãn và archive email trong Gmail bằng Python + Gmail API

---

## ❗ Vấn đề

Gmail là công cụ không thể thiếu trong công việc hàng ngày, nhưng:

- Hộp thư đến (Inbox) nhanh chóng trở nên **lộn xộn**
- Email quan trọng dễ bị **bỏ sót**
- Thiếu khả năng **tự động gắn nhãn theo ngữ cảnh**
- Việc quản lý email vẫn còn **thủ công và mất thời gian**

---

## ✅ Giải pháp

**Gmail Auto Labeler** là một Python project giúp bạn:

- Tự động **phân loại email** theo nội dung và người gửi
- **Gắn nhãn** phù hợp (Waiting, Follow up, Read Through – theo phương pháp GTD)
- **Archive email** sau khi được phân loại
- **Đánh dấu là chưa đọc** các email chưa xử lý được

---

## ✨ Các tính năng chính

| Tính năng                    | Mô tả                                                                 |
|-----------------------------|----------------------------------------------------------------------|
| 🧠 Rule-based Classification | Phân loại dựa vào từ khóa và địa chỉ người gửi                       |
| 🏷️ Gắn nhãn Gmail tự động   | Gắn các nhãn như `Waiting`, `Follow up`, `Read Through` theo GTD     |
| 📦 Archive sau khi xử lý     | Email được lưu trữ khỏi Inbox sau khi gắn nhãn                       |
| 🔄 Mark as Unread            | Email không phân loại được sẽ **giữ lại dưới dạng chưa đọc**         |

---

## 🧰 Công cụ sử dụng

- 🐍 **Python 3**
- ☁️ **Google Cloud Gmail API**
---

## 🚀 Hướng phát triển tiếp theo

### 🤖 Tích hợp AI (GPT / LLM)

- Phân loại ngữ cảnh nâng cao
- Tóm tắt nội dung email
- Gợi ý phản hồi tự động

### ☁️ Triển khai Cloud-native

- Dùng **Google Cloud Functions** hoặc **AWS Lambda** kết hợp Gmail Push Notification
- Luôn chạy nền, không cần mở máy

---

## ⚙️ Cài đặt & Chạy thử

```bash
git clone https://github.com/stevetran77/gmail-auto-labeler.git
cd gmail-auto-labeler
pip install -r requirements.txt
python main.py
