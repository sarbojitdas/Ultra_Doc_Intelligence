from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import hashlib

# ---------------- Core Modules ----------------
from core.loader import load_document
from core.chunking import chunk_text
from core.embeddings import get_embeddings
from core.vectorstore import create_vectorstore, get_retriever
from core.retriever import retrieve_docs
from core.llm import llm_call
from core.confidence import compute_confidence
from core.guardrail import apply_guardrails

# ---------------- Extraction Modules ----------------
from extraction.extractor import extract_structured
from extraction.schema import schema

# ---------------- App Init ----------------
app = FastAPI()

# ---------------- In-memory storage ----------------
db = {}
cache = {}


# ---------------- Request Model ----------------
class QueryRequest(BaseModel):
    query: str


# ---------------- File Hash ----------------
async def get_file_hash(file: UploadFile) -> str:
    content = await file.read()
    await file.seek(0)
    return hashlib.md5(content).hexdigest()


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

    # Embeddings
    embeddings = get_embeddings()

    # Vectorstore + Retriever
    vectorstore = create_vectorstore(chunks, embeddings)
    retriever = get_retriever(vectorstore)

    # Store
    db["retriever"] = retriever
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
    retriever = db.get("retriever")

    if not retriever:
        return {"error": "Upload document first"}

    docs = retrieve_docs(query, retriever)

    # Convert Document -> text
    doc_texts = [doc.page_content for doc in docs]

    context = "\n".join(doc_texts)

    prompt = f"""
    Answer the question using only the context below.

    Context:
    {context}

    Question:
    {query}
    """

    raw_answer = llm_call(prompt)

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