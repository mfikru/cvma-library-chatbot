import os
from pathlib import Path
from typing import List, Dict

import streamlit as st
from google import genai
from pypdf import PdfReader
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

APP_DIR = Path(__file__).parent
KB_DIR = APP_DIR / "knowledge_base"

st.set_page_config(
    page_title="CVMA Library AI Assistant",
    page_icon="📚",
    layout="wide",
)

DEFAULT_PROFILE = """
CVMA LIBRARY AND TECHNOLOGY SERVICES
Addis Ababa University, College of Veterinary Medicine and Agriculture

ABOUT
The CVMA Library and Technology Services supports teaching, learning,
research, innovation, and community engagement.

SERVICES
- Book lending and circulation
- Reference and information services
- Electronic information services
- Digital library and repository guidance
- Research and literature-search support
- Information literacy and user orientation
- Reference-management guidance
- Electronic document delivery
- Academic writing, copyright, and plagiarism awareness
- Responsible artificial-intelligence literacy

DIGITAL AND RESEARCH SUPPORT
The Library supports discovery and use of scholarly information,
institutional research outputs, theses and dissertations, and electronic
resources. Access conditions depend on the relevant resource licence
and institutional arrangements.

INFORMATION AND AI LITERACY
Users can receive guidance on identifying information needs, searching,
evaluating source credibility, using information ethically, citing sources,
and using AI tools responsibly. AI-generated information and references
must be independently verified.

IMPORTANT LIMITATION
This starter profile is not a substitute for approved institutional policy.
Do not assume opening hours, borrowing periods, fines, database subscriptions,
contact details, or other operational rules unless these are stated in an
uploaded official document. If a specific institutional fact is not available,
tell the user that it could not be verified and direct them to the Library.
"""

SYSTEM_INSTRUCTIONS = """
You are the CVMA Library AI Assistant for Addis Ababa University,
College of Veterinary Medicine and Agriculture.

Help students, academic staff, researchers, and other library users with
library services, information discovery, literature searching, research
support, information literacy, academic writing, referencing, copyright,
plagiarism awareness, and responsible AI use.

Accuracy and safety rules:
1. Use the supplied institutional excerpts for CVMA-specific facts.
2. Never invent opening hours, fees, borrowing rules, contact details,
   database subscriptions, policies, or service availability.
3. If the supplied excerpts do not establish a CVMA-specific fact, say
   that you cannot verify it from the available Library information.
4. You may give general academic guidance, clearly distinguishing it from
   official CVMA policy.
5. Do not fabricate citations, DOIs, article titles, authors, or URLs.
6. When asked for sources, identify only the uploaded source files and
   page numbers supplied in the context. Do not present these as published
   scholarly references unless the document itself supports that.
7. Be concise, respectful, practical, and clear.
8. Protect personal, confidential, and unpublished information.
"""

@st.cache_resource(show_spinner=False)
def load_knowledge():
    items = [{
        "source": "Built-in CVMA Library starter profile",
        "page": None,
        "text": DEFAULT_PROFILE,
    }]

    if not KB_DIR.exists():
        return items

    for path in sorted(KB_DIR.iterdir()):
        suffix = path.suffix.lower()
        try:
            if suffix == ".pdf":
                reader = PdfReader(str(path))
                for page_no, page in enumerate(reader.pages, start=1):
                    txt = page.extract_text() or ""
                    if txt.strip():
                        items.append({
                            "source": path.name,
                            "page": page_no,
                            "text": txt,
                        })
            elif suffix == ".docx":
                doc = Document(str(path))
                txt = "\n".join(p.text for p in doc.paragraphs)
                if txt.strip():
                    items.append({
                        "source": path.name,
                        "page": None,
                        "text": txt,
                    })
            elif suffix in {".txt", ".md"}:
                txt = path.read_text(encoding="utf-8", errors="ignore")
                if txt.strip():
                    items.append({
                        "source": path.name,
                        "page": None,
                        "text": txt,
                    })
        except Exception as exc:
            st.warning(f"Could not read {path.name}: {exc}")

    return items

def make_chunks(items: List[Dict], chunk_size: int = 1100, overlap: int = 150):
    chunks = []
    for item in items:
        content = item["text"]
        start = 0
        while start < len(content):
            part = content[start:start + chunk_size].strip()
            if part:
                chunks.append({
                    "source": item["source"],
                    "page": item["page"],
                    "text": part,
                })
            start += max(1, chunk_size - overlap)
    return chunks

@st.cache_resource(show_spinner=False)
def build_retriever():
    items = load_knowledge()
    chunks = make_chunks(items)
    texts = [c["text"] for c in chunks]
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        max_features=50000,
        strip_accents="unicode",
    )
    matrix = vectorizer.fit_transform(texts)
    return chunks, vectorizer, matrix

def retrieve(question: str, top_k: int = 5):
    chunks, vectorizer, matrix = build_retriever()
    q_vec = vectorizer.transform([question])
    scores = cosine_similarity(q_vec, matrix).ravel()
    ranked = scores.argsort()[::-1][:top_k]
    results = []
    for idx in ranked:
        if scores[idx] > 0:
            item = dict(chunks[idx])
            item["score"] = float(scores[idx])
            results.append(item)
    return results

def get_api_key():
    key = None
    try:
        key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass
    return key or os.getenv("GEMINI_API_KEY")

def answer_question(question: str, history: List[Dict]):
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "Gemini API key is missing. Add GEMINI_API_KEY in "
            "Streamlit Community Cloud → App settings → Secrets."
        )

    docs = retrieve(question)
    if docs:
        context_parts = []
        for i, doc in enumerate(docs, start=1):
            page = f", page {doc['page']}" if doc["page"] else ""
            context_parts.append(
                f"[Source {i}: {doc['source']}{page}]\n{doc['text']}"
            )
        context = "\n\n".join(context_parts)
    else:
        context = (
            "No matching passage was found in the local CVMA knowledge base. "
            "Do not infer official institutional facts."
        )

    client = genai.Client(api_key=api_key)

    # Keep a short conversation window to control token use.
    recent_history = history[-8:] if history else []
    history_text = "\n".join(
        f"{'User' if m.get('role') == 'user' else 'Assistant'}: {m.get('content', '')}"
        for m in recent_history
    )

    prompt = f"""
{SYSTEM_INSTRUCTIONS}

CONVERSATION SO FAR:
{history_text or "(No previous conversation)"}

RETRIEVED CVMA LIBRARY KNOWLEDGE:
{context}

USER'S CURRENT QUESTION:
{question}

Answer the current question. If relevant, include a short "Sources consulted"
section listing the source filenames and page numbers shown above. Only list
sources that you actually used. If no relevant source was found, say so.
"""

    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    response = client.interactions.create(
        model=model,
        input=prompt,
    )
    return response.output_text or "I could not generate an answer. Please try again."

def main():
    st.title("📚 CVMA Library AI Assistant")
    st.caption(
        "Addis Ababa University · College of Veterinary Medicine and Agriculture"
    )

    with st.sidebar:
        st.header("About this assistant")
        st.write(
            "Ask about Library services, research support, information literacy, "
            "academic writing, referencing, and responsible AI use."
        )
        st.divider()
        st.subheader("Knowledge base")
        try:
            items = load_knowledge()
            extra_files = [x for x in items if x["source"] != "Built-in CVMA Library starter profile"]
            st.metric("Loaded source files", len(set(x["source"] for x in extra_files)))
            st.metric("Extracted text sections", len(items))
        except Exception:
            st.info("Knowledge base will load when the app starts.")
        st.caption(
            "Institutional answers are limited to the documents included with "
            "this application. Verify important policies with the Library."
        )
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask the CVMA Library a question...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching Library information and preparing an answer..."):
                try:
                    history = st.session_state.messages[:-1]
                    reply = answer_question(prompt, history)
                    st.markdown(reply)
                except Exception as exc:
                    reply = (
                        "Sorry, I could not complete your request.\n\n"
                        f"**Details:** {exc}"
                    )
                    st.error(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()
