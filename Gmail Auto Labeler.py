# %% [markdown]
# ✨ Cài đặt thư viện yêu cầu
!pip install --quiet google-api-python-client google-auth google-auth-oauthlib nltk

# %% [markdown]
# 🚀 Cài thêm OpenAI (nếu muốn tích hợp GPT sau này)
!pip install openai

# %% [markdown]
# 📚 Nạp thư viện & biến API key (nếu dùng OpenAI)
import json
import openai

# %% [markdown]
# # Lấy GPT API Key (nếu muốn)
# from openai import OpenAI
# client = OpenAI(api_key="<YOUR_API_KEY>")

# %% [markdown]
# # Test connection GPT (tùy chọn)
# response = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user", "content": "What is Getting Things Done?"}]
# )
# print(response.choices[0].message.content)

# %% [markdown]
# 🌐 Kết nối Gmail API
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)

# Lưu token để dùng cho lần sau
with open("token.json", "w") as token:
    token.write(creds.to_json())

# %% [markdown]
# 📂 Trích xuất nội dung email & lấy danh sách email trong INBOX
import base64

def extract_body(payload):
    if "body" in payload and "data" in payload["body"]:
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
    elif "parts" in payload:
        for part in payload["parts"]:
            result = extract_body(part)
            if result:
                return result
    return ""

def get_unlabeled_emails(max_results=10):
    query = "label:INBOX"
    results = service.users().messages().list(userId="me", maxResults=max_results, q=query).execute()
    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        label_ids = data.get("labelIds", [])
        payload = data.get("payload", {})
        headers = payload.get("headers", [])

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown Sender)")
        body = extract_body(payload)

        print(f"📧 {subject} | 👤 From: {sender}")

        emails.append({
            "id": msg["id"],
            "subject": subject,
            "body": body,
            "from": sender,
            "label_ids": label_ids
        })

    return emails

# %% [markdown]
# 🧰 Rule-based classifier
import re

def extract_email_address(sender):
    match = re.search(r'<(.+?)>', sender)
    return match.group(1) if match else sender

def classify_email(subject, body, sender):
    text = f"{subject} {body}".lower()
    sender_email = extract_email_address(sender)

    print("🔎 Nội dung email (chuẩn hoá):", text)
    print("📨 Từ địa chỉ:", sender_email)

    if any(kw in text for kw in ["\u0111ơn hàng", "mã đơn", "tracking", "vận chuyển", "giao hàng", "order", "đơn số"]):
        return ["ARCHIVE"]

    labels = []

    sender_label_map = {
        "connect@thepresentwriter.com": "Read Through",
        "hello@lukejbyrne.com": "Read Through",
    }

    if sender_email in sender_label_map:
        labels.append(sender_label_map[sender_email])

    if any(kw in text for kw in ["payslip", "bảng lương"]):
        labels.append("Payslip")
    if any(kw in text for kw in ["cần phản hồi", "gửi lại", "phản hồi giúp", "deadline", "trả lời", "check lại"]):
        labels.append("Follow up")
    if any(kw in text for kw in ["đang chờ", "chờ xác nhận", "đã gửi trước đó", "pending"]):
        labels.append("Waiting")
    if any(kw in text for kw in ["thông báo", "tóm tắt", "fyi", "vui lòng đọc"]):
        labels.append("Read Through")

    return list(set(labels))

# %% [markdown]
# 🔺 Gắn nhãn

def add_label_to_email(msg_id, label_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"addLabelIds": [label_id]}
    ).execute()

# # Tìm các nhãn trong Gmail
# from googleapiclient.discovery import build

# # Initialize the Gmail API service
# service = build("gmail", "v1", credentials=creds)

# labels = service.users().labels().list(userId="me").execute().get("labels", [])
# for label in labels:
#     print(f"{label['name']} ➜ {label['id']}")

# %% [markdown]
# 🔹 Nạp file mapping nhãn (label name → label ID)
with open("labels_config.json", "r") as f:
    label_map = json.load(f)

# %% [markdown]
# 🌐 Phân loại toàn bộ email & gắn nhãn
from googleapiclient.discovery import build
service = build("gmail", "v1", credentials=creds)

emails = get_unlabeled_emails(max_results=20)

for email in emails:
    subject = email.get("subject", "")
    body = email.get("body", "")
    msg_id = email.get("id")
    sender = email.get("from", "")
    labels = classify_email(subject, body, sender)

    if "ARCHIVE" in labels:
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["INBOX"]}
        ).execute()
        print(f"📦 [ARCHIVE] {subject}")
        continue

    matched_labels = [label_map[lbl] for lbl in labels if lbl in label_map]

    if matched_labels:
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"addLabelIds": matched_labels, "removeLabelIds": ["INBOX"]}
        ).execute()
        print(f"🌏 {subject} → Labels: {labels}")
    else:
        print(f"🟡 [UNCLASSIFIED] {subject}")

# %% [markdown]
# 🔄 Mark as Unread toàn bộ email đã đọc trong Inbox
results = service.users().messages().list(userId="me", q="label:INBOX is:read").execute()
remaining_messages = results.get("messages", [])

for msg in remaining_messages:
    service.users().messages().modify(
        userId="me",
        id=msg["id"],
        body={"addLabelIds": ["UNREAD"]}
    ).execute()
    print(f"🔄 Marked as UNREAD: {msg['id']}")
