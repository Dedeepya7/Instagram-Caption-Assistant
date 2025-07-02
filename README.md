# Instagram Caption Generator 📸

**Generate creative, multilingual Instagram captions effortlessly.**  
Upload an image or describe your post, customize style, length, emojis, hashtags, and get captions powered by AI (BLIP + LLM).

---

## 🌟 Highlights

- **Image & text input**: Caption generator works with uploaded images (via BLIP) or user description.
- **Customization**: Choose tone (formal/informal/humorous/inspirational/poetic), length, include emojis & hashtags.
- **Multilingual**: Output in English, Hindi, Telugu, Tamil, and more.
- **Downloadable captions**: Save results as a `.txt` file.
- **Privacy-first**: All processing is done locally; no data is stored.

---

## 🧭 Table of Contents

1. [Overview](#overview)  
2. [Installation](#installation)  
3. [Usage](#usage)  
4. [Project Structure](#project-structure)  
5. [Requirements](#requirements)  
6. [Contributing](#contributing)  
7. [Authors](#authors)  
8. [License](#license)

---

## Overview

This Streamlit app helps users create engaging Instagram captions automatically. It uses:

- **BLIP** for image captioning
- **LLM (e.g., GPT‑4 / Falcon‑7B)** to generate caption variations
- Supports multiple languages and other preferences

Ideal for social media creators, marketers, or anyone looking to level up their Insta game!

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/instagram-caption-generator.git
cd instagram-caption-generator
### 2. Create a virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows PowerShell
### 3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
Usage
Launch the app:

bash
Copy
Edit
streamlit run app.py
Open http://localhost:8501 in your browser.

Upload image(s) or enter a post description.

Select number, style, length, emojis, hashtags, and language.

Click Generate Captions.

View captions and download as .txt.

Project Structure
graphql
Copy
Edit
├── app.py                 # Main Streamlit application
├── model_utils.py         # BLIP model loader & image describer
├── caption_generator.py   # LLM integration & prompt chain code
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .streamlit/
    └── secrets.toml       # API keys (e.g., HUGGINGFACEHUB_API_TOKEN)
Requirements
Python ≥ 3.10

torch, transformers, streamlit, Pillow

langchain, langchain-community, google-generativeai (for Gemini)

API keys:

HUGGINGFACEHUB_API_TOKEN for Falcon / Llama

GEMINI_API_KEY (optional) for Gemini Pro

Add your keys to .streamlit/secrets.toml:

toml
Copy
Edit
HUGGINGFACEHUB_API_TOKEN = "hf_xxx"
GEMINI_API_KEY = "ya29_xxx"
Contributing 🤝
Contributions are welcome! To propose enhancements or fix bugs:

Fork the repo

Create a feature branch: git checkout -b feature-xyz

Commit changes: git commit -m "Add xyz feature"

Push branch: git push origin feature-xyz

Open a Pull Request

Please follow PEP 8, include docstrings, and keep architecture modular.

Authors
Your Name – Initial work – your GitHub

Contributors – Thanks to everyone who contributed

License
Licensed under the MIT License – see the LICENSE file for details.
