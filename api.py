from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
from groq import Groq

# ---------------- Core Modules ----------------
from core.chunking import chunk_text
from core.confidence import compute_confidence
from core.guardrail import apply_guardrails

# ---------------- Extraction Modules ----------------
from extraction.extractor import extract_structured
from extraction.schema import schema

# ---------------- Load ENV ----------------
load_dotenv()

# ---------------- App Init ----------------
app = FastAPI()

# ---------------- CORS (IMPORTANT FOR STREAMLIT) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- In-memory storage ----------------
db = {}
cache = {}

# ---------------- Groq Client ----------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not set in environment variables")

client = Groq(api_key=GROQ_API_KEY)

# ---------------- Request Model ----------------
class QueryRequest(BaseModel):
    query: str


# ---------------- File Hash ----------------
async def get_file_hash(file: UploadFile) -> str:
    content = await file.read()
    await file.seek(0)
    return hashlib.md5(content).hexdigest()


# ---------------- Load Document ----------------
def load_document(file: UploadFile):
    content = file.file.read()
    pdf = fitz.open(stream=content, filetype="pdf")

    text = ""
    for page in pdf:
        text += page.get_text()

    # 🔒 limit size (prevents token overflow)
    if len(text) > 20000:
        text = text[:20000]

    return text


# ---------------- Upload Endpoint ----------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_id = await get_file_hash(file)

    if file_id in cache:
        return {"status": "loaded from cache", "file_id": file_id}

    # Load document
    full_text = load_document(file)

    # Chunking
    chunks = chunk_text(full_text)

    # Store
    db["chunks"] = chunks
    db["full_text"] = full_text

    cache[file_id] = True

    return {
        "status": "processed",
        "file_id": file_id,
        "chunks": len(chunks)
    }


# ---------------- Ask Endpoint ----------------
@app.post("/ask")
async def ask(request: QueryRequest):

    query = request.query
    chunks = db.get("chunks")

    if not chunks:
        return {"error": "Upload document first"}

    # 🔍 simple retrieval
    relevant_chunks = [
        chunk for chunk in chunks
        if query.lower() in chunk.lower()
    ]

    # fallback
    if not relevant_chunks:
        relevant_chunks = chunks[:5]

    doc_texts = relevant_chunks[:5]

    context = "\n".join(doc_texts)

    prompt = f"""
    Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {query}
    """

    # 🤖 GROQ LLM CALL
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Answer only from context."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_answer = response.choices[0].message.content

    # Guardrails
    answer, guard_score = apply_guardrails(raw_answer, doc_texts)

    # Confidence
    confidence = compute_confidence(answer, doc_texts)

    return {
        "answer": answer,
        "confidence": confidence,
        "guard_score": guard_score,
        "sources": doc_texts
    }


# ---------------- Extract Endpoint ----------------
@app.post("/extract")
async def extract():

    full_text = db.get("full_text")

    if not full_text:
        return {"error": "Upload document first"}

    structured = extract_structured(full_text)

    return {
        "data": structured,
        "schema": schema
    }


# ---------------- Health ----------------
@app.get("/")
def root():
    return {"status": "API running"}
