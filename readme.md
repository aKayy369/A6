# 📘 A6: Naive RAG vs Contextual Retrieval

## 👤 Student Information
- **Student ID:** st125999  
- **Chapter Assigned:** Chapter 9  

---

# Overview

This assignment implements a **Retrieval-Augmented Generation (RAG)** system for answering questions based on a specific textbook chapter.

Two approaches are compared:

- **Naive RAG**
- **Contextual Retrieval**

The goal is to evaluate how adding contextual information to chunks improves retrieval and answer generation.

---

# Task 1: Source Discovery & Data Preparation

## Chapter Selection
Based on the last digit of the student ID (**9**), **Chapter 9** was selected from the textbook.

---

## Document Processing

The chapter PDF was processed using **PyMuPDF (`fitz`)**:

- Extracted raw text from PDF  
- Cleaned text by:
  - Removing special characters  
  - Fixing broken lines  
  - Removing page numbers  
  - Normalizing whitespace  

---

## Chunking Strategy

- Chunk size: **500 characters**
- Overlap: **100 characters**

This ensures:
- Better context continuity  
- Improved retrieval performance  

---

## QA Pair Generation

- Created **20 Question-Answer pairs**
- Based strictly on Chapter 9 content  

Saved in:
```
outputs/task1/qa_pairs.json
outputs/task1/ground_truth.json
```

---

# Task 2: Naive RAG vs Contextual Retrieval

## 🔍 Models Used

### Retriever Model
- **SentenceTransformer**
- Model: `all-MiniLM-L6-v2`

### Generator Model (Evaluation)
- **Qwen 2.5 3B Instruct**
- Model: `Qwen/Qwen2.5-3B-Instruct`

---

## Naive RAG

Pipeline:
1. Split text into chunks  
2. Convert chunks into embeddings  
3. Retrieve top-k chunks using FAISS  
4. Generate answer from retrieved context  

---

## Contextual Retrieval

To improve retrieval quality, Contextual Retrieval was implemented by enriching each chunk with additional context generated using an LLM.

### Contextual Enrichment

For each chunk, a short 1–2 sentence explanation was generated describing how the chunk relates to the full document (Chapter 9).

### Prompt Strategy

The model was provided with:
- The document title (Chapter 9)
- A truncated portion of the full document
- The target chunk

It then generated a contextual prefix in the format:

```
This chunk from Chapter 9 discusses ...
```

### Example

**Before:**
```
Revenue grew 40% to $314M with improved margins.
```

**After:**
```
This chunk from Chapter 9 discusses financial performance and growth trends discussed in the text.

Revenue grew 40% to $314M with improved margins.
```

### Chunk Transformation

Each chunk was transformed into:

- Contextual prefix  
- Original chunk text  

### Re-Embedding and Indexing

The enriched chunks were:
- Re-embedded using the same embedding model  
- Stored in a FAISS index  

### Retrieval and Generation

The same retrieval and generation pipeline as Naive RAG was used, but applied on contextualized chunks instead.

This improves:
- Semantic understanding  
- Retrieval relevance  
- Answer quality  

## Evaluation Method

- Used **ROUGE metrics**:
  - ROUGE-1  
  - ROUGE-2  
  - ROUGE-L  

- Compared generated answers with ground truth  

---

## Evaluation Results

| Method | ROUGE-1 | ROUGE-2 | ROUGE-L |
|--------|--------|--------|--------|
| Naive RAG | 0.3541 | 0.1665 | 0.3065 |
| Contextual Retrieval | 0.4052 | 0.2049 | 0.3380 |

---

## Analysis

The results show that **Contextual Retrieval significantly outperforms Naive RAG** across all metrics.

- ROUGE-1 improved, indicating better word-level relevance  
- ROUGE-2 improved, showing stronger phrase-level coherence  
- ROUGE-L improved, indicating better sentence structure  

This demonstrates that contextual enrichment helps retrieve more relevant chunks and improves answer generation quality.

---

# Task 3: Chatbot Web Application

## Implementation

A web application was developed using **Streamlit**.

### Features:
- Ask questions about Chapter 9  
- Uses Contextual Retrieval backend  
- Displays:
  - Generated answer  
  - Retrieved source chunks  

---


## Project Structure

```
.
├── app/
│   └── app.py
├── outputs/
│   ├── task1/
│   └── task2/
├── answer/
│   └── response-st125999-chapter-9.json
├── README.md
├── requirements.txt
```

---



## JSON Format

```json
[
  {
    "question": "...",
    "ground_truth_answer": "...",
    "naive_rag_answer": "...",
    "contextual_retrieval_answer": "..."
  }
]
```

---

# Conclusion

This project demonstrates that **Contextual Retrieval improves RAG performance** by enhancing retrieval quality through contextual enrichment.

It leads to:
- Better chunk relevance  
- More accurate answers  
- Higher ROUGE scores  

---
