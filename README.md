# ⚖️ ClauseWise – AI-Powered Legal Document Analyzer

> Simplifying complex legal documents using AI and Natural Language Processing.

## 📌 Overview

**ClauseWise** is an AI-powered legal document analysis platform designed to simplify, analyze, and classify complex legal texts for lawyers, businesses, and individuals.

Legal documents such as contracts, NDAs, and agreements often contain complex terminology that makes them difficult to understand without legal expertise. ClauseWise leverages Generative AI and Natural Language Processing (NLP) to transform lengthy legal documents into clear, understandable insights.

The platform enables users to extract important clauses, simplify legal language, identify key entities, and classify documents automatically.

---

## 🎯 Problem Statement

Understanding legal documents is often:

- ⏳ Time-consuming due to lengthy contracts and agreements.
- ⚠️ Error-prone when important clauses or obligations are overlooked.
- ⚖️ Dependent on specialized legal knowledge.
- 🔍 Difficult for individuals without a legal background.

ClauseWise addresses these challenges by automating legal document analysis and making legal information more accessible and easier to understand.

---

## 🚀 Features

### 1. 📝 Clause Simplification
- Converts complex legal language into plain, easy-to-understand explanations.
- Helps users understand their rights, responsibilities, and obligations.
- Uses Generative AI to provide context-aware explanations.

### 2. 🔍 Named Entity Recognition (NER)
Extracts important information from legal documents, including:
- Parties involved
- Dates and deadlines
- Monetary amounts
- Obligations
- Important legal terms

### 3. 📑 Clause Extraction & Breakdown
- Identifies and extracts individual clauses from lengthy documents.
- Organizes legal content into manageable sections.
- Enables clause-level analysis for easier understanding.

### 4. 🗂️ Document Type Classification
Automatically categorizes legal documents into types such as:
- Non-Disclosure Agreements (NDA)
- Lease Agreements
- Employment Contracts
- Service Agreements

### 5. 📂 Multi-Format Document Support
Supports uploading and analyzing documents in multiple formats:
- PDF
- DOCX
- TXT

### 6. 💻 User-Friendly Interface
- Interactive interface built using Streamlit or Gradio.
- Simple document upload and analysis workflow.
- Designed for users with and without legal expertise.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| AI & NLP | Gemini API |
| Generative AI | Gemini 3.5 Flash-Lite |
| Frontend | Streamlit, Gradio |
| Document Processing | PDF, DOCX, TXT |
| Version Control | Git, GitHub |

---

## 📁 Project Structure

```text
ClauseWise/
├── backend/                # FastAPI API and document analysis
│   ├── main.py
│   ├── gemini_api.py       # Gemini API client
│   └── requirements.txt
├── frontend/               # Streamlit interface
│   ├── app.py
│   └── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.9+
- pip
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### 1. Install dependencies

From the project directory, create and activate a virtual environment, then install both requirements files:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
pip install -r frontend\requirements.txt
```

### 2. Start the backend

In the first PowerShell terminal:

```powershell
$env:GEMINI_API_KEY = "your-gemini-api-key"
cd backend
python main.py
```

The backend sends clause text to Gemini 3.5 Flash-Lite using the Gemini API. Google’s free tier may use submitted content to improve its products, so do not upload confidential documents when using it.

### 3. Start the frontend

In a second terminal, from the project directory:

```powershell
.\.venv\Scripts\Activate.ps1
cd frontend
streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

---

## 🔮 Future Enhancements

- Legal risk identification and flagging.
- Multi-language legal document support.
- Document summarization.
- Comparison of multiple legal documents.
- Interactive question-answering system for uploaded documents.
- Improved legal clause classification models.

---

## ⚠️ Disclaimer

ClauseWise is an AI-powered tool intended for informational and educational purposes only. Its outputs should not be considered legal advice. Users should consult qualified legal professionals before making legal decisions.

---

## 👨‍💻 Author

**Abhishek Thakur**

GitHub: [@abhioder](https://github.com/abhioder)

---

⭐ If you find this project useful, consider giving it a star!
