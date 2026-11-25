# CVMA Library AI Assistant

## Addis Ababa University
### College of Veterinary Medicine and Agriculture
### Library and Technology Services

An AI-powered academic library chatbot developed using Python, Streamlit, and Google Gemini.

The application provides students, academic staff, researchers, and other library users with information and guidance about library services, electronic resources, research support, information literacy, academic writing, and responsible AI use.

---

## 1. Project Objectives

The CVMA Library AI Assistant aims to:

- Improve access to library information and services.
- Provide 24-hour automated user assistance.
- Support students and researchers in literature searching.
- Promote information and AI literacy.
- Provide guidance on academic writing and referencing.
- Support responsible use of artificial intelligence.
- Improve the visibility and accessibility of library resources.

## 2. Main Features

- AI-powered conversational interface.
- Google Gemini integration.
- Institutional knowledge retrieval.
- PDF, DOCX, TXT, and Markdown document support.
- Library service information.
- Research and literature-search assistance.
- Information literacy guidance.
- Academic writing and referencing support.
- Source identification from uploaded institutional documents.

## 3. Technologies Used

| Component | Technology |
|---|---|
| Programming language | Python |
| Web framework | Streamlit |
| AI engine | Google Gemini |
| AI SDK | google-genai |
| Information retrieval | TF-IDF |
| PDF processing | pypdf |
| Word processing | python-docx |
| Machine learning | scikit-learn |
| Hosting | Streamlit Community Cloud |
| Source code management | GitHub |

## 4. Project Structure

```text
cvma_library_chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   └── secrets.toml
│
└── knowledge_base/
    ├── library_profile.pdf
    ├── library_guidelines.pdf
    ├── digital_library_guide.pdf
    └── information_literacy.pdf
```

Note: The documents shown above are examples. Add your approved institutional documents.

## 5. Installation and Setup

### Step 1: Install Python

Download Python from:

https://www.python.org/downloads/

Python 3.10–3.12 is recommended.

### Step 2: Download the project

Clone the GitHub repository:

```bash
git clone https://github.com/YOUR_USERNAME/cvma-library-chatbot.git
```

Navigate to the project folder:

```bash
cd cvma-library-chatbot
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

## 6. Configure Google Gemini API

Obtain a Gemini API key from:

https://aistudio.google.com/apikey

Set the API key as an environment variable.

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Set the model:

```powershell
$env:GEMINI_MODEL="gemini-3.8-flash"
```

Never upload your API key to GitHub.

## 7. Run the Application Locally

Execute:

```bash
streamlit run app.py
```

The application will open in your web browser.

Default local address:

http://localhost:8501

## 8. Deploy on Streamlit Community Cloud

1. Push the project to GitHub.
2. Visit https://share.streamlit.io/
3. Sign in using your GitHub account.
4. Select Create App.
5. Select your repository.
6. Choose the main branch.
7. Set the main file path to:

```text
app.py
```

8. Open Advanced Settings or the application Secrets settings.
9. Add the following secrets:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
GEMINI_MODEL = "gemini-3.8-flash"
```

10. Click Deploy.

## 9. Institutional Knowledge Base

The chatbot retrieves relevant information from documents stored in:

```text
knowledge_base/
```

Supported formats:

- PDF
- DOCX
- TXT
- MD

The application uses TF-IDF retrieval to identify relevant document passages before generating responses using Gemini.

Scanned PDF documents may require OCR before uploading.

## 10. Future Development

Potential improvements include:

- English and Amharic language support.
- Integration with Koha Library Management System.
- Integration with DSpace Institutional Repository.
- Advanced semantic search.
- Research database discovery.
- Reference management assistance.
- Chat history and user analytics.
- Feedback and service evaluation.
- Institutional server deployment.

## 11. Privacy and Responsible AI

- Never upload confidential student records.
- Do not upload unpublished research without authorization.
- Protect API keys and credentials.
- Verify AI-generated information.
- Follow institutional information security and data protection requirements.
- Use only documents authorized for distribution.

The chatbot does not replace professional librarians or official institutional policies.

## 12. Acknowledgment

Developed for:

**Addis Ababa University**  
**College of Veterinary Medicine and Agriculture**  
**Library and Technology Services**

Project: CVMA Library AI Assistant

---

© 2026 AAU-CVMA Library and Technology Services.
