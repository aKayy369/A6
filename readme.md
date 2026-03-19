# A6: Naive RAG vs Contextual Retrieval

## Submitted BY - 
- **Student ID:** st125999  
- **Assigned Chapter:** Chapter 9  

---

# Objective

The goal of this assignment is to build a **domain-specific Question Answering (QA) system** using Retrieval-Augmented Generation (RAG) techniques.

Two retrieval approaches are implemented and compared:

- **Naive RAG**
- **Contextual Retrieval**

Their performance is evaluated using **ROUGE metrics**.

---


---

# Task 1: Source Discovery & Data Preparation

## Chapter Selection
The assigned chapter is determined by the last digit of the student ID.

- Student ID: **st125999**
- Last digit: **9**
- Assigned chapter: **Chapter 9**

---

## Document Processing

The chapter PDF was processed using **PyMuPDF (`fitz`)**.

### Steps:
- Extract raw text from PDF
- Remove unwanted characters
- Fix broken words and lines
- Remove page numbers
- Normalize whitespace

---

## Chunking Strategy

The cleaned text was split into overlapping chunks:

- **Chunk size:** 500 characters  
- **Overlap:** 100 characters  

### Why overlap?
- Preserves context between chunks  
- Improves retrieval quality  

---

## QA Pair Generation

- Created **20 question-answer pairs**
- Based strictly on Chapter 9 content
- Covers key topics:
  - Instruction tuning
  - RLHF
  - Reward models
  - DPO
  - Chain-of-thought prompting

Saved in: 
---

# Task 1: Source Discovery & Data Preparation

## Chapter Selection
The assigned chapter is determined by the last digit of the student ID.

- Student ID: **st125999**
- Last digit: **9**
- Assigned chapter: **Chapter 9**

---

## Document Processing

The chapter PDF was processed using **PyMuPDF (`fitz`)**.

### Steps:
- Extract raw text from PDF
- Remove unwanted characters
- Fix broken words and lines
- Remove page numbers
- Normalize whitespace

---

## Chunking Strategy

The cleaned text was split into overlapping chunks:

- **Chunk size:** 500 characters  
- **Overlap:** 100 characters  

### Why overlap?
- Preserves context between chunks  
- Improves retrieval quality  

---

## QA Pair Generation

- Created **20 question-answer pairs**
- Based strictly on Chapter 9 content
- Covers key topics:
  - Instruction tuning
  - RLHF
  - Reward models
  - DPO
  - Chain-of-thought prompting

Saved in: outputs/task1/qa_pairs.json
outputs/task1/ground_truth.json


---

# Task 2: Naive RAG vs Contextual Retrieval

## Models Used

### Retriever Model
- **Model:** `sentence-transformers/all-MiniLM-L6-v2`  
- Used for embedding chunks and queries  

### Generator Model
- **Model:** `Qwen/Qwen2.5-3B-Instruct`  
- Used for answer generation  

---

# 2.1 Naive RAG

## Pipeline:

1. Split text into chunks  
2. Convert chunks into embeddings  
3. Store embeddings in FAISS index  
4. Retrieve top-k relevant chunks  
5. Generate answer using retrieved context  

### Key Characteristics:
- Uses **raw chunk text only**
- No additional context provided

---

# 2.2 Contextual Retrieval

## Idea:
Improve retrieval by **adding semantic context to each chunk**.

---

## Contextual Enrichment

Each chunk is enriched using an LLM to generate a short explanation.

### Input to LLM:
- Chapter title  
- Partial full document  
- Target chunk  

### Output:
A contextual prefix:


---

## Re-Embedding

- Enriched chunks are embedded again  
- Stored in a new FAISS index  

---

## Retrieval & Generation

- Same pipeline as Naive RAG  
- But uses **contextualized chunks**

---

## Why Contextual Retrieval Works Better

- Adds semantic meaning to chunks  
- Improves retrieval accuracy  
- Provides better input to generator  

---

# 2.3 Evaluation

## Metric Used:
- **ROUGE-1**
- **ROUGE-2**
- **ROUGE-L**

These measure overlap between:
- Generated answer  
- Ground truth answer  

---

# 2.4 Results

| Method | ROUGE-1 | ROUGE-2 | ROUGE-L |
|--------|--------|--------|--------|
| Naive RAG | 0.3541 | 0.1665 | 0.3065 |
| Contextual Retrieval | 0.4052 | 0.2049 | 0.3380 |

---

# Analysis

The results show that **Contextual Retrieval significantly outperforms Naive RAG**.

### Improvements:
- **ROUGE-1 ↑** → better word-level relevance  
- **ROUGE-2 ↑** → better phrase-level matching  
- **ROUGE-L ↑** → better sentence structure  

---

## Reason for Improvement

Naive RAG relies only on raw chunk text, which may lack sufficient context.

Contextual Retrieval improves performance because:

- Each chunk includes **additional semantic explanation**
- Retriever selects **more relevant chunks**
- Generator receives **clearer and richer context**

---

## Conclusion

Contextual Retrieval leads to:
- Better retrieval quality  
- More accurate answers  
- Higher evaluation scores  

---

# Task 3: Chatbot Web Application

## Implementation

A web application was built using **Streamlit**.

---

## Features

- Ask questions about Chapter 9  
- Uses **Contextual Retrieval backend**  
- Displays:
  - Generated answer  
  - Top retrieved chunks  
  - Source chunk content  

---


