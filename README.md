# SyllaBot - AI-Powered Intelligent Syllabus Chatbot

## Overview
SyllaBot is a full-stack AI web application that allows students to instantly ask questions about their course syllabuses using natural language. Professors can upload course syllabuses as PDFs, and students can query them through an intelligent chatbot powered by OpenAI's GPT API. Built with Flask, Bootstrap, and OpenAI API.

## Key Features
- **AI-Powered Q&A** — Students ask questions in plain English and get instant answers from course syllabuses
- **PDF Processing** — Automatically extracts and indexes text from uploaded syllabus PDFs
- **Professor Dashboard** — Secure login system for professors to upload and manage syllabuses
- **Student Interface** — No login required for students to access the chatbot
- **Course Management** — Add, update, and delete courses and syllabuses
- **User Authentication** — Secure session-based login for professors

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Flask |
| **AI/LLM** | OpenAI GPT-3.5-turbo API |
| **PDF Processing** | PyMuPDF (fitz) |
| **Frontend** | HTML, Bootstrap 5, JavaScript |
| **Data Storage** | JSON (syllabus index, user accounts) |
| **Architecture** | Full-stack MVC web application |

## Project Structure
```
syllabot-ai-chatbot/
├── app.py                  # Main Flask application
├── app_fixed.py            # Updated version with bug fixes
├── llm.py                  # OpenAI API integration
├── llm_server.py           # Local LLM server (testing)
├── apikey.py               # API key configuration
├── syllabus_index.json     # Course index database
├── templates/
│   ├── login.html          # Student/Professor landing page
│   ├── ask_ui_final.html   # Student chatbot interface
│   ├── upload_ui_final.html # Professor dashboard
│   ├── manage.html         # Syllabus management
│   ├── manage_accounts.html # Account management
│   └── create_account.html  # Account creation
└── syllabi/                # Uploaded PDF storage
```

## How to Run

### Prerequisites
- Python 3.13+
- OpenAI API key

### Installation
```bash
# Clone the repository
git clone https://github.com/deepakkethavarapu-895692246/syllabot-ai-chatbot.git
cd syllabot-ai-chatbot

# Install dependencies
pip install flask pymupdf openai requests

# Add your API key
# Open apikey.py and add your OpenAI API key
OPENAI_API_KEY = "your-api-key-here"
FLASK_SECRET_KEY = "your-secret-key-here"
```

### Run the Application
```bash
python app.py
```

Then open your browser and go to:
```
http://localhost:5081
```

## How It Works

1. **Professor uploads** a course syllabus PDF through the dashboard
2. **SyllaBot extracts** the text from the PDF using PyMuPDF
3. **Student selects** their course and asks a question
4. **OpenAI GPT** processes the syllabus text and student question
5. **SyllaBot returns** an accurate, context-aware answer instantly

## Key Results
- Reduced document search time by approximately 50% compared to manual PDF reading
- Supports multiple concurrent courses and departments
- Scalable backend architecture supporting multiple users simultaneously
- Secure professor authentication with session management

## Screenshots

### Student Chatbot Interface
Students can select their course and ask questions in plain English

### Professor Dashboard  
Professors can upload, manage, and delete course syllabuses securely

## Future Improvements
- Vector database integration for faster semantic search
- Multi-document query support
- Chat history and conversation memory
- Mobile responsive design improvements
- Support for non-PDF document formats

## Author
**Deepak Kethavarapu**
- Email: deepakkethavarapu2024@gmail.com
- LinkedIn: [Deepak Kethavarapu](www.linkedin.com/in/deepak-kethavarapu-895692246)
- GitHub: [deepakkethavarapu-895692246](https://github.com/deepakkethavarapu-895692246)
