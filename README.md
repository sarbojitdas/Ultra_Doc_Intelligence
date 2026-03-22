# 📄 Ultra Doc Intelligence

An AI-powered document understanding system that allows you to **upload PDFs, ask questions, and extract structured data** using LLMs, embeddings, and vector search.

---

## 🚀 Features

* 📂 Upload PDF documents
* 💬 Ask questions from document context (RAG-based)
* 📊 Confidence score for answers
* 🛡️ Guardrails for safe and relevant responses
* 📦 Structured data extraction
* ⚡ FastAPI backend + Streamlit frontend
* 🧠 Uses embeddings + vector database (FAISS)

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **Frontend:** Streamlit
* **LLM:** Groq / LLM API
* **Embeddings:** Sentence Transformers
* **Vector DB:** FAISS
* **Frameworks:** LangChain

---

## 📁 Project Structure

```
project-root/
│
├── api.py                 # FastAPI backend
├── app.py                 # Streamlit frontend
├── requirements.txt
├── start.sh
│
├── core/                  # Core pipeline modules
│   ├── loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vectorstore.py
│   ├── retriever.py
│   ├── llm.py
│   ├── confidence.py
│   └── guardrail.py
│
├── extraction/            # Structured extraction
│   ├── extractor.py
│   └── schema.py
```

---

## ⚙️ Installation (Local Setup)

### 1. Clone the repository

```
git clone https://github.com/your-username/ultra-doc-intelligence.git
cd ultra-doc-intelligence
```

---

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Set environment variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key
```

---

## ▶️ Run Locally

### Start FastAPI

```
uvicorn api:app --reload
```

API runs at:

```
http://127.0.0.1:8000
```

---

### Start Streamlit

```
streamlit run app.py
```

---

## 🌐 Deployment (Free)

### 🔹 Backend → Render

1. Push code to GitHub
2. Go to https://render.com
3. Create **Web Service**
4. Use:

   * Build Command:

     ```
     pip install -r requirements.txt
     ```
   * Start Command:

     ```
     bash start.sh
     ```

---

### 🔹 start.sh file

```
#!/bin/bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```

---

### 🔹 Frontend → Streamlit Cloud

1. Go to https://share.streamlit.io
2. Deploy `app.py`
3. Update API URL:

```
API_BASE_URL = "https://your-api-name.onrender.com"
```

---

## 🧪 API Endpoints

### 📂 Upload Document

```
POST /upload
```

---

### 💬 Ask Question

```
POST /ask
```

Body:

```
{
  "query": "Your question"
}
```

---

### 📊 Extract Data

```
POST /extract
```

---

## ⚠️ Limitations (Free Tier)

* ⏳ Render sleeps after inactivity (~15 min)
* 🧠 In-memory storage resets
* 📄 Re-upload required after restart

---

## 🔮 Future Improvements

* Persistent vector database (Chroma / Pinecone)
* Authentication system
* Multi-document support
* Bett
