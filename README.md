# 🩺 Blood Work Health Analyzer

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-orange?logo=google-gemini)](https://ai.google.dev/)
[![uv Package Manager](https://img.shields.io/badge/Managed%20with-uv-black?logo=python)](https://github.com/astral-sh/uv)

An AI-powered agentic application built with **Streamlit** and **LangChain** that parses plain-text blood work reports. Using **Gemini 2.5 Flash**, it extracts and classifies medical test results and generates a hyper-localized **Pakistani Diet Plan** tailored to the patient's condition.

---

## 🌟 Features

* **Stage 1: Automated Medical Extraction** Extracts all medical parameters and instantly classifies them as **HIGH**, **LOW**, or **NORMAL** based on the laboratory reference ranges.
* **Stage 2: Clinical Nutritionist (Pakistani Diet)** Generates a concise 2-line clinical health summary and creates a targeted dietary plan split strictly into:
  1. *Foods to avoid*
  2. *Foods to eat more of*
  *(Tailored specifically to common Pakistani meals and dietary habits).*
* **Flexible Inputs** Allows uploading a `.txt` report, pasting raw text directly, or testing with the built-in sample report.

---

## 📂 Project Structure

```text
├── app.py                  # Main Streamlit Application
├── blood_work.txt         # Pre-saved sample blood report
└── .env                   # (You have to make this file on your local machine by yourself)
