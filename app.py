import os
import torch
import streamlit as st
from PIL import Image, UnidentifiedImageError
from transformers import BlipProcessor, BlipForConditionalGeneration
import google.generativeai as genai
from datetime import datetime

# Page config
st.set_page_config(page_title="Instagram Caption Assistant", layout="centered")

# ---- CSS: dreamy script for subtitle/privacy, NO cursor tracking ----
st.markdown("""
    <style>
        body, .stApp {
            background: linear-gradient(120deg, #f7971e 0%, #fd5c63 40%, #a445b2 100%) !important;
        }
        .main-header {
            display: flex;
            align-items: center;
            gap: 18px;
            margin-bottom: 1.3rem;
            margin-top: 1.3rem;
        }
        .main-header-text {
            font-family: 'Poppins', 'Inter', sans-serif;
            font-size: 2.7rem;
            font-weight: 700;
            color: #fff;
            letter-spacing: 0.7px;
            text-shadow: 0 2px 8px #a445b288, 0 1px 0 #fd5c6388;
        }
        /* Dreamy script font for subtitle/privacy lines */
        @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
        .dreamy-script {
            font-family: 'Pacifico', cursive;
            font-size: 2.1rem;
            color: #fff;
            display: block;
            background: none;
            border-radius: 0;
            margin-bottom: 0.15rem;
            margin-top: 1.1rem;
            box-shadow: none;
            border: none;
            outline: none;
            letter-spacing: 0.8px;
            filter: brightness(1.09);
            font-style: normal;
        }
        .dreamy-script-privacy {
            font-family: 'Pacifico', cursive;
            font-size: 1.35rem;
            color: #fff;
            display: block;
            background: none;
            border-radius: 0;
            margin-bottom: 1.13rem;
            box-shadow: none;
            border: none;
            outline: none;
            letter-spacing: 0.7px;
            filter: brightness(1.08);
            font-style: normal;
        }
        .stButton button {
            background: #fd5c63;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 0.85rem 2.2rem;
            font-size: 1.15rem;
            transition: background 0.2s;
        }
        .stButton button:hover {
            background: #a445b2;
            color: #fff;
        }
        .stFileUploader {
            border-radius: 12px;
            border: 2px dashed #fd5c63;
            background: #fff9fb;
        }
        .stCheckbox > label {
            color: #a445b2 !important;
            font-weight: 500;
        }
        .stSelectbox > div {
            border-radius: 8px;
        }
        .stAlert {
            border-radius: 8px;
        }
        .caption-block {
            font-size: 1.23rem !important;
            color: #232323 !important;
            font-weight: 500 !important;
            background: rgba(255,255,255,0.97);
            border-radius: 14px;
            padding: 1.2rem 1.3rem;
            margin: 1.3rem 0;
            box-shadow: 0 2px 12px #0001;
        }
        .stMarkdown ol, .stMarkdown ul {
            color: #363636 !important;
        }
    </style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="main-header">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png"
         style="width:54px; height:54px; border-radius:50%; box-shadow:0 4px 12px #0002;">
    <span class="main-header-text">
        Instagram Caption Assistant
    </span>
</div>
""", unsafe_allow_html=True)

# Dreamy script, no outline subtitle/privacy lines
st.markdown("""
    <div class="dreamy-script">
        Upload an image or describe your post to get smart captions in any language!
    </div>
    <div class="dreamy-script-privacy">
        No data stored. Fully private. ✨
    </div>
""", unsafe_allow_html=True)

# === 🔐 Gemini API Key ===
if "GEMINI_API_KEY" not in st.secrets:
    st.warning("Please add your Gemini API key to .streamlit/secrets.toml as GEMINI_API_KEY.")
    st.stop()
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# === 🖼️ Load BLIP for Image Captioning ===
@st.cache_resource
def load_blip_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

def get_image_description(images, processor, model):
    descriptions = []
    for idx, img in enumerate(images):
        try:
            inputs = processor(images=img, return_tensors="pt")
            with torch.no_grad():
                outputs = model.generate(**inputs)
            desc = processor.decode(outputs[0], skip_special_tokens=True)
            descriptions.append(desc)
        except Exception as e:
            descriptions.append(f"Could not process image {idx+1}: {e}")
    return " ".join(descriptions)

# --- Language search box list ---
language_list = [
    "English", "Spanish", "French", "German", "Hindi", "Mandarin Chinese", "Arabic", "Bengali",
    "Russian", "Portuguese", "Indonesian", "Japanese", "Punjabi", "Marathi", "Telugu", "Turkish",
    "Tamil", "Vietnamese", "Korean", "Italian", "Gujarati", "Persian", "Polish", "Ukrainian",
    "Dutch", "Romanian", "Greek", "Malayalam", "Kannada", "Czech", "Hungarian", "Thai", "Hebrew",
    "Swedish", "Finnish", "Danish", "Norwegian", "Slovak", "Bulgarian", "Serbian", "Croatian", "Sinhala",
    "Filipino", "Malay", "Swahili", "Afrikaans", "Irish", "Scottish Gaelic", "Catalan", "Basque", "Galician",
    "Estonian", "Latvian", "Lithuanian", "Slovenian", "Icelandic", "Albanian", "Macedonian", "Belarusian",
    "Armenian", "Georgian", "Azerbaijani", "Uzbek", "Kazakh",
]
language_list = sorted(language_list)

# --- PROMPT LOGIC ---
def build_prompt(desc, n, style, length, emojis, hashtags, language):
    if language.lower() == "english":
        return f"""
        Generate {n} unique Instagram captions in English ONLY for the following post:
        "{desc}"
        Captions should be {length.lower()} and in a {style.lower()} style.
        {'Include emojis.' if emojis else 'No emojis.'}
        {'Include hashtags.' if hashtags else 'No hashtags.'}
        Do NOT provide translations or captions in any other language.
        List the captions as a numbered list, with no extra explanations or formatting.
        """
    else:
        return f"""
        Generate {n} unique Instagram captions for the following post:
        "{desc}"
        Captions should be {length.lower()} and in a {style.lower()} style.
        {'Include emojis.' if emojis else 'No emojis.'}
        {'Include hashtags.' if hashtags else 'No hashtags.'}
        The captions should be in {language}.
        For each caption, also provide a translation in English, formatted as:
        [Caption in {language}]
        English: [English translation]
        List the captions as a numbered list, with no extra explanations or formatting.
        """

def generate_captions(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text.strip()

# --- UI ---

uploaded_files = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Robust image loading with error handling and preview
images = []
if uploaded_files:
    for f in uploaded_files:
        try:
            images.append(Image.open(f))
        except UnidentifiedImageError:
            st.error(f"File {f.name} is not a valid image and was skipped.")

for img in images:
    st.image(img, width=120)

text_input = st.text_area("Or describe your post", "")

# Number input for number of captions: up/down arrows, between 1 and 10
n_captions = st.number_input("Number of Captions", min_value=1, max_value=10, value=3, step=1)

caption_style = st.selectbox("Caption Style", ["Formal", "Informal", "Humorous", "Inspirational", "Poetic"])
caption_length = st.selectbox("Caption Length", ["Short", "Medium", "Long"])
emojis = st.checkbox("Include Emojis 😊", value=True)
hashtags = st.checkbox("Include Hashtags #️⃣", value=True)
language = st.selectbox("Search or select your output language", language_list, index=language_list.index("English"))

if (images or text_input.strip()) and st.button("Generate Captions"):
    with st.spinner("Generating captions..."):
        processor, model = load_blip_model()
        description = get_image_description(images, processor, model) if images else text_input.strip()
        prompt = build_prompt(description, n_captions, caption_style, caption_length, emojis, hashtags, language)
        try:
            captions = generate_captions(prompt)
            st.success("🎉 Captions generated!")
            st.markdown(f'<div class="caption-block">{captions}</div>', unsafe_allow_html=True)
            st.download_button("📥 Download Captions", captions, file_name=f"captions_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("Upload an image or enter a description to begin.")
