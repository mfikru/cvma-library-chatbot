# CVMA Library AI Assistant — Streamlit

A starter Streamlit chatbot for the Addis Ababa University College of Veterinary
Medicine and Agriculture (CVMA) Library. It uses Gemini for answer generation
and TF-IDF retrieval over local institutional documents.

## Files

- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies
- `knowledge_base/` — put approved PDF, DOCX, TXT, or Markdown files here
- `.gitignore` — prevents secrets and local files from being committed

## 1. Test locally

Python 3.10–3.12 is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Set your Gemini API key as an environment variable.

Windows PowerShell:
```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
streamlit run app.py
```

macOS/Linux:
```bash
export GEMINI_API_KEY="YOUR_API_KEY"
streamlit run app.py
```

Optional model override:
```bash
# Windows PowerShell
$env:GEMINI_MODEL="gemini-3.8-flash"
```

## 2. Add institutional documents

Place approved and non-confidential documents in `knowledge_base/`.
Supported formats: PDF, DOCX, TXT, MD.

Restart the app after adding or replacing documents. Scanned PDFs may need OCR
before their text can be retrieved. Do not upload personal student records,
confidential documents, or unpublished research without institutional approval.

## 3. Deploy on Streamlit Community Cloud

1. Create a GitHub repository for this project.
2. Upload `app.py`, `requirements.txt`, `.gitignore`, `README.md`, and the
   `knowledge_base/` folder containing only approved documents.
3. Do **not** upload your Gemini API key.
4. Sign in to https://share.streamlit.io/ using GitHub.
5. Choose **Create app**, select the repository, branch, and `app.py`.
6. Before or after deployment, open the app's **Settings → Secrets** and add:

```toml
GEMINI_API_KEY = "paste-your-key-here"
GEMINI_MODEL = "gemini-3.8-flash"
```

7. Save and reboot/redeploy the app.

## 4. Important deployment notes

- Keep the GitHub repository private if institutional policy requires it.
  Confirm your hosting plan supports private repositories.
- Streamlit Community Cloud is a hosted service, not an AAU institutional server.
  Obtain institutional approval before publishing institutional documents.
- The API key is stored in Streamlit secrets, not in GitHub.
- This starter app uses basic keyword retrieval (TF-IDF), not a fully validated
  retrieval-augmented generation system. Test answers against official documents.
- It does not connect directly to Koha, DSpace, subscribed databases, or student
  records. Such integrations require authorized APIs and access controls.
- Add only documents that the Library is authorized to distribute.
- Establish privacy, retention, user-notice, and human-escalation procedures
  before public institutional use.

## 5. Troubleshooting

**Missing Gemini API key**: Set `GEMINI_API_KEY` in Streamlit Cloud Secrets.

**Model not found**: Check the currently available Gemini model names for your
API project and set `GEMINI_MODEL` accordingly in Secrets.

**PDF text is empty**: The PDF may be scanned; OCR it before adding it.

**New documents do not appear**: Restart/reboot the app to clear cached data.

**Build failure**: Check the Streamlit Cloud logs and verify that the dependency
versions in `requirements.txt` are compatible with the Python runtime.
