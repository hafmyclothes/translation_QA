# 🔍 Translation QA · Thai Language Studio

ระบบตรวจสอบคุณภาพการแปล (Translation QA) สำหรับบริษัทแปลภาษาไทย  
Powered by **Claude AI (Anthropic)**

---

## ✨ ฟีเจอร์

- ตรวจสอบคุณภาพงานแปลตาม **RUBRIC 4 ด้าน**
  - 🎯 Accuracy · ความถูกต้องของความหมาย
  - 📚 Terminology · การใช้คำศัพท์เฉพาะทาง
  - 🗣️ Register · ระดับภาษา
  - 🌊 Fluency · ความลื่นไหล
- ให้คะแนน 1–5 พร้อม comment วิเคราะห์เชิงลึก
- แสดงปัญหาที่พบและข้อแนะนำการแก้ไขในแต่ละด้าน
- ตัวอย่างงานแปลที่ควรแก้ไข

---

## 🚀 วิธี Deploy บน Streamlit Cloud

### 1. สร้าง GitHub Repository
```bash
git init
git add translation_qa_app.py requirements.txt README.md
git commit -m "Initial commit: Translation QA app"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
git push -u origin main
```

### 2. ตั้งค่า Streamlit Secrets
ที่ [share.streamlit.io](https://share.streamlit.io) → **New app** → เลือก repo → ไปที่ **Advanced settings → Secrets** แล้วใส่:

```toml
[anthropic]
api_key = "sk-ant-..."
```

### 3. Deploy
- **Main file path:** `translation_qa_app.py`
- กด **Deploy** รอสักครู่ แอปจะพร้อมใช้งาน

---

## 🔑 API Key

แอปนี้ใช้ **Anthropic Claude API**  
สมัครและรับ API key ได้ที่: https://console.anthropic.com

> ⚠️ ห้าม commit API key ลง GitHub โดยตรง ให้ใช้ Streamlit Secrets เสมอ

---

## 💻 รัน Local

```bash
pip install streamlit

# ตั้งค่า API key
export ANTHROPIC_API_KEY="sk-ant-..."

streamlit run translation_qa_app.py
```

หรือสร้างไฟล์ `.streamlit/secrets.toml`:
```toml
[anthropic]
api_key = "sk-ant-..."
```

---

## 📁 โครงสร้างไฟล์

```
.
├── translation_qa_app.py   # แอปหลัก
├── requirements.txt        # Python dependencies
└── README.md               # เอกสารนี้
```

---

## 🛠️ Tech Stack

| ส่วนประกอบ | เทคโนโลยี |
|---|---|
| Frontend | Streamlit + Custom CSS |
| AI Engine | Claude claude-sonnet-4-20250514 (Anthropic) |
| Language | Python 3.10+ |
| Deploy | Streamlit Cloud |
