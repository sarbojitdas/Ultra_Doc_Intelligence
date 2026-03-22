import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Ultra Doc Intelligence", layout="wide")
st.title("📄 Ultra Doc Intelligence")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Upload PDF")

uploaded_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    if st.sidebar.button("Process Document"):
        with st.spinner("Processing..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            res = requests.post(f"{API_BASE_URL}/upload", files=files)

            if res.status_code == 200:
                data = res.json()
                st.success(data.get("status"))
                st.info(f"Chunks: {data.get('chunks', 'N/A')}")
            else:
                st.error("Upload failed")
                st.text(res.text)

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["💬 Ask", "📊 Extract"])

# ---------------- ASK ----------------
with tab1:
    st.subheader("Ask Questions")

    query = st.text_input("Enter your question")

    if st.button("Get Answer"):
        if not query:
            st.warning("Enter a question")
        else:
            with st.spinner("Thinking..."):

                # ✅ FIXED: POST + json + correct variable
                res = requests.post(
                    f"{API_BASE_URL}/ask",
                    json={"query": query}
                )

                if res.status_code == 200:
                    data = res.json()

                    if "error" in data:
                        st.error(data["error"])

                    elif "answer" in data:
                        st.markdown("### 🧠 Answer")
                        st.write(data["answer"])

                        conf = data.get("confidence", 0)

                        st.markdown("### 📊 Confidence")
                        st.progress(conf)
                        st.write(conf)

                        st.markdown("### 📚 Sources")
                        for i, src in enumerate(data.get("sources", [])):
                            with st.expander(f"Source {i+1}"):
                                st.write(src)

                    else:
                        st.error("Unexpected response")
                        st.json(data)

                else:
                    st.error(f"Error {res.status_code}")
                    st.text(res.text)

# ---------------- EXTRACT ----------------
with tab2:
    st.subheader("Extract Data")

    if st.button("Run Extraction"):
        with st.spinner("Extracting..."):

            # ✅ FIXED: correct variable name
            res = requests.post(f"{API_BASE_URL}/extract")

            if res.status_code == 200:
                data = res.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.markdown("### 📦 Extracted Data")
                    st.json(data.get("data", {}))

                    st.markdown("### 🧾 Schema")
                    st.json(data.get("schema", {}))

            else:
                st.error("Extraction failed")
                st.text(res.text)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("FastAPI + Streamlit + LangChain + Groq")