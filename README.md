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
| AI & NLP | IBM Watson, Hugging Face |
| Generative AI | IBM Granite Models |
| Frontend | Streamlit, Gradio |
| Document Processing | PDF, DOCX, TXT |
| Version Control | Git, GitHub |

---

## 📁 Project Structure

```text
ClauseWise/
│
├── backend/
│   ├── models/             # AI models and NLP components
│   ├── processing/         # Document processing and analysis
│   └── utils/              # Helper functions
│
├── frontend/               # Streamlit / Gradio interface
│
├── app.py                 # Application entry point
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.9+
- Git
- pip

### 1. Clone the repository

```bash
git clone https://github.com/abhioder/ClauseWise.git
```

### 2. Navigate to the project directory

```bash
cd ClauseWise
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will start locally, and you can access it through the URL provided in your terminal.

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
