# genai-systems-lab 🛡️🤖

This repository is a **hands-on learning and experimentation hub** for building **production-ready Generative AI systems** with a strong focus on **Responsible AI (RAI)**.

It covers **RAG pipelines, multi-agent systems, safety layers, monitoring, evaluation, and governance** — designed with **real-world deployment** in mind.

---

## 🎯 Goals of This Repository

- Build **end-to-end GenAI pipelines**
- Implement **Responsible AI by design**
- Experiment with **RAG & agentic architectures**
- Understand **pre-production evaluation** and **post-production monitoring**
- Apply **safety, ethics, and governance** to LLM systems

---

## 🧩 What This Repo Covers

### 📚 Retrieval-Augmented Generation (RAG)
- Basic and advanced RAG pipelines
- Chunking strategies & embeddings
- Vector databases (FAISS, Chroma)
- Query rewriting & hybrid search
- RAG evaluation techniques

---

### 🧠 Multi-Agent Systems
- CrewAI
- AutoGen
- LangGraph
- Agent planning & coordination
- Tool-using agents
- Agent safety boundaries

---

### 🛡️ Responsible AI (RAI) Layer

The RAI layer ensures model outputs are:
- Safe
- Ethical
- Explainable
- Auditable
- Policy-aligned

#### Responsibilities
- Harmful content detection & blocking
- Sensitive topic handling (politics, religion, hate, violence, self-harm, adult content)
- Prompt injection & jailbreak prevention
- Output validation & policy enforcement
- Audit logs & explainability

---

### 🚦 API Gateway & Safety Controls
- Authentication & Authorization
- Rate limiting
- Input validation
- PII masking
- Request & response logging

---

### 🧪 Pre-Production Evaluation
- Manual red-teaming (weekly batches)
- Adversarial prompt testing
- Safety & policy checks
- Bias and fairness evaluation
- Explainability analysis

**Tools Used**
- Microsoft Responsible AI Toolbox
- Custom evaluation scripts

---

### 📊 Post-Production Monitoring
- Continuous safety monitoring
- Dashboard-based insights
- Policy violation tracking
- Model drift detection
- User feedback analysis

**Human-in-the-loop**
- Manual review of flagged outputs
- Prompt and policy tuning
- Model or agent behavior adjustments

---

## 🧰 Microsoft Responsible AI Toolbox – Role

Primarily used for:
- Model evaluation
- Fairness checks
- Explainability & debugging

**Best suited for**
- Pre-production testing
- Batch evaluation
- Offline analysis

Also supports **post-production investigations** using logged data.

---

## 🗂️ Repository Structure

```bash
genai-responsible-systems/
│
├── rag/
│   ├── basic/
│   ├── advanced/
│   └── evaluation/
│
├── agents/
│   ├── crewai/
│   ├── autogen/
│   └── langgraph/
│
├── rai/
│   ├── safety_checks/
│   ├── policy_rules/
│   ├── explainability/
│   └── audit_logs/
│
├── gateway/
│   ├── auth/
│   ├── rate_limit/
│   └── masking/
│
├── monitoring/
│   ├── dashboards/
│   └── alerts/
│
├── caching/
│   ├── response_cache/
│   └── embedding_cache/
│
├── experiments/
│
├── requirements.txt
├── .env.example
└── README.md

