# sleep-circadian-research-agent-ai

# 🧠 Sleep & Circadian Research Agent

An automated AI-powered research assistant that monitors PubMed for the latest scientific publications in sleep and circadian rhythm research and generates structured daily literature briefings.

---

## 📌 Overview

This project builds an automated pipeline for tracking neuroscience literature in real time.

It:

- Searches PubMed for sleep and circadian rhythm studies  
- Filters for relevant biomedical and clinical research  
- Retrieves recent peer-reviewed publications  
- Uses a large language model to summarize findings  
- Outputs a structured research briefing  

The goal is to reduce scientific information overload and make it easier to stay up to date with rapidly evolving sleep research.

---

## ⚙️ How It Works

### 1. Literature Retrieval
The system queries PubMed using a structured search across:
- Sleep physiology
- Circadian rhythm regulation
- Chronobiology
- Sleep disorders (insomnia, shift work, REM/NREM sleep)

It prioritizes recent publications from major biomedical journals.

---

### 2. Data Processing
Retrieved PubMed results are extracted and passed into the summarization pipeline.

---

### 3. AI Summarization
An LLM processes research data and generates structured summaries:

- Title  
- Journal and date  
- Key findings  
- Why it matters  
- Limitations  
- Clinical relevance  

---

### 4. Output
Final output is a daily research briefing that can be:
- Printed in terminal  
- Sent via email (optional SMTP setup)  

---

## 🧠 Motivation

Scientific literature in neuroscience is expanding rapidly, making manual tracking difficult.

This project explores how AI can assist in:

- Literature monitoring  
- Scientific summarization  
- Research prioritization  
- Knowledge workflow automation  

---

## ⚙️ Setup

### Install dependencies
```bash
pip install -r requirements.txt
