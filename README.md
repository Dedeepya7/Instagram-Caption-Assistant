# Instagram Caption Assistant

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/github/license/Dedeepya7/Instagram-Caption-Assistant)

Generate creative, multilingual Instagram captions from images or descriptions using BLIP and LLMs via Streamlit.

---

## 🌟 Features

- Generate captions from image or user description
- Choose number, style, length, emojis, hashtags, and language
- Supports English, Hindi, Telugu, Tamil, etc.
- Download captions as `.txt`
- Powered by HuggingFace & Gemini APIs

---

## 🧭 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [Authors](#authors)
- [License](#license)

---

## 🚀 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/Dedeepya7/Instagram-Caption-Assistant
cd Instagram-Caption-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# For Linux/macOS
source venv/bin/activate

# For Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Launch the app:

```bash
streamlit run app.py
```

Then:

1. Open `http://localhost:8501` in your browser  
2. Upload image(s) or enter a post description  
3. Select number, style, length, emojis, hashtags, and language  
4. Click **Generate Captions**  
5. View or download the captions as a `.txt` file  

---

## 🗂️ Project Structure

```
instagram-Caption-Assistant/
├── app.py                 # Main Streamlit application
├── model_utils.py         # BLIP model loader & image describer
├── caption_generator.py   # LLM integration & prompt chain code
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .streamlit/
    └── secrets.toml       # API keys (e.g., GEMINI_API_KEY)
```

---

## 📦 Requirements

- **Python** 3.10, 3.11, 3.12 
- `torch`, `transformers`, `streamlit`, `Pillow`
- `langchain`, `langchain-community`, `google-generativeai`  

### API Keys Needed

- `GEMINI_API_KEY` (for Gemini Pro)
-  [Gemini Studio](https://aistudio.google.com/) – Manage your Gemini API keys and projects.

### Add them to `.streamlit/secrets.toml`

```toml
GEMINI_API_KEY = "ya29_xxx"
```

---

## ⚠️ Security

**Never commit your `.streamlit/secrets.toml` or API keys to public repositories!**

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. **Fork** the repo  
2. Create a **feature branch**:  
   ```bash
   git checkout -b feature-xyz
   ```
3. **Commit changes**:  
   ```bash
   git commit -m "Add xyz feature"
   ```
4. **Push to your fork**:  
   ```bash
   git push origin feature-xyz
   ```
5. **Open a Pull Request**

🧑‍💻 Please follow **PEP 8**, use **docstrings**, and keep the code modular.

---

## 👩‍💻 Authors

- **Dedeepya Ramidi** – Initial work – https://github.com/Dedeepya7

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---
