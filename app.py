import streamlit as st
import json
from pathlib import Path

import torch
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

DEVICE = "cpu"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GEN_MODEL = "google/flan-t5-base"

TOP_K = 3

DATA_PATH = Path("outputs/task2/contextual_chunks.json")

if not DATA_PATH.exists():
    st.error("contextual_chunks.json not found.")
    st.stop()

with open(DATA_PATH, "r", encoding="utf-8") as f:
    contextual_chunks = json.load(f)

@st.cache_resource
def load_models():
    embedder = SentenceTransformer(EMBED_MODEL)

    tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)
    model = AutoModelForSeq2SeqLM.from_pretrained(GEN_MODEL)

    return embedder, tokenizer, model


embedder, tokenizer, model = load_models()

@st.cache_resource
def build_index():
    texts = [c["text"] for c in contextual_chunks]

    embeddings = embedder.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index


index = build_index()

def retrieve(query):
    q_emb = embedder.encode([query], normalize_embeddings=True).astype("float32")
    scores, idxs = index.search(q_emb, TOP_K)

    results = []
    for rank, (i, s) in enumerate(zip(idxs[0], scores[0]), start=1):
        c = contextual_chunks[int(i)]
        results.append({
            "rank": rank,
            "chunk_id": c["chunk_id"],
            "score": float(s),
            "text": c["text"]
        })

    return results

def generate_answer(question, retrieved_chunks):

    context = "\n\n".join([
        f"[Chunk {c['chunk_id']}]\n{c['text'][:300]}"
        for c in retrieved_chunks
    ])

    prompt = f"""
You are an academic assistant.

Answer the question using ONLY the context below.

Write a detailed explanation in 2-3 sentences.

Question:
{question}

Context:
{context}

Answer in 2-3 sentences:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=120,
        min_length=40,             
        temperature=0.7,
        top_p=0.95,
        do_sample=True,
        repetition_penalty=1.1
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return answer.strip()

# =========================
# UI
# =========================
st.set_page_config(page_title="RAG Chatbot", layout="wide")

# HEADER
st.markdown("""
# QA Chatbot  
### Contextual Retrieval, Chapter 9
""")

st.markdown("---")

# INPUT
st.markdown("### Ask a Question")

query = st.text_area(
    "Enter your question:",
    height=100,
    placeholder="e.g. What is instruction tuning?"
)

col1, col2 = st.columns([1, 5])

with col1:
    ask_btn = st.button("Ask")

# =========================
# RESPONSE
# =========================
if ask_btn and query:

    with st.spinner("🔍 Retrieving relevant chunks..."):
        retrieved = retrieve(query)

    with st.spinner("Generating answer..."):
        answer = generate_answer(query, retrieved)

    st.markdown("---")

    # ANSWER BOX
    st.markdown("##  Answer")

    st.markdown(
        f"""
        <div style="
            background: #111827;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #374151;
            font-size: 16px;
            line-height: 1.7;
            color: #f9fafb;
        ">
        {answer}
        </div>
        """,
        unsafe_allow_html=True
    )

    # CHUNKS
    st.markdown("##  Retrieved Chunks")

    for c in retrieved:
        with st.expander(
            f" Chunk {c['chunk_id']} | Rank {c['rank']} | Score: {c['score']:.3f}"
        ):
            st.markdown(
                f"""
                <div style="
                    background: #0f172a;
                    padding: 15px;
                    border-radius: 10px;
                    border: 1px solid #334155;
                    color: #e5e7eb;
                ">
                {c["text"]}
                </div>
                """,
                unsafe_allow_html=True
            )

# FOOTER
st.markdown("---")
st.markdown(
    "<center> Contextual Retrieval + RAG | NLP Assignment</center>",
    unsafe_allow_html=True
)