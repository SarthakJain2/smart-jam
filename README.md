# 💼 Smart Job Application Manager

A full-stack project that helps you **track job applications**, manage deadlines, and use **AI to match your resume to job descriptions** for personalized insights.

Built with **FastAPI (backend)**, **React + Vite + Tailwind (frontend)**, and **PostgreSQL**.

---

## 🚀 Features
- 🧾 **Application Tracking** — Add, edit, and organize applications by status (Applied, OA, Interview, Offer, Rejected).
- 🔐 **Authentication (JWT)** — Secure user accounts with hashed passwords.
- 🤖 **AI Resume–JD Matching** — Upload your resume (PDF/DOCX) and paste a JD to get:
  - Similarity score (0–100)
  - Keywords present and missing
- 📅 **Deadlines & Notes** — Track recruiter contacts, deadlines, and interview notes.
- 📈 **Future Extensions**
  - Email reminders via SendGrid
  - Analytics dashboards
  - Gmail/Calendar integration

---

## 🧩 Tech Stack
| Layer | Tech |
|-------|------|
| **Frontend** | React, Vite, TailwindCSS, Axios |
| **Backend** | FastAPI, SQLAlchemy, Pydantic, JWT |
| **Database** | PostgreSQL (local or Docker) |
| **AI/NLP** | Sentence-Transformers or OpenAI embeddings |
| **Deployment** | Render / Vercel (recommended) |

---

## ⚙️ Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/smart-jam.git
cd smart-jam
```
---
### 2. Backend Setup
```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
