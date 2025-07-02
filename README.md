# Instagram Caption Assistant 

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
- [Contributing](#contributing-)
- [Authors](#authors)
- [License](#license)

---

## 🚀 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/<your-username>/instagram-caption-generator.git
cd instagram-caption-generator
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
instagram-caption-generator/
├── app.py                 # Main Streamlit application
├── model_utils.py         # BLIP model loader & image describer
├── caption_generator.py   # LLM integration & prompt chain code
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .streamlit/
    └── secrets.toml       # API keys (e.g., HUGGINGFACEHUB_API_TOKEN)
```

---

## 📦 Requirements

- **Python** ≥ 3.10  
- `torch`, `transformers`, `streamlit`, `Pillow`  
- `langchain`, `langchain-community`, `google-generativeai`  

### API Keys Needed

- `HUGGINGFACEHUB_API_TOKEN` (for models like Falcon or Llama)
- `GEMINI_API_KEY` (optional, for Gemini Pro)

### Add them to `.streamlit/secrets.toml`

```toml
HUGGINGFACEHUB_API_TOKEN = "hf_xxx"
GEMINI_API_KEY = "ya29_xxx"
```

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

- **Your Name** – Initial work – [your GitHub](https://github.com/your-username)

Thanks to all contributors!

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

