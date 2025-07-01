import os
import torch
import streamlit as st
from PIL import Image, UnidentifiedImageError
from transformers import BlipProcessor, BlipForConditionalGeneration
import google.generativeai as genai
from datetime import datetime

# Page config
st.set_page_config(page_title="Instagram Caption Assistant", layout="centered")

# Custom CSS for pastel Instagram-like background and improved readability
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(120deg, #fbe7b3 0%, #f7b0b7 50%, #b8a7f7 100%) !important;
        }
        /* Header */
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
            color: #202025;
            letter-spacing: 0.7px;
            text-shadow: 0 2px 8px #fff7;
        }
        /* Subtitle */
        .subtitle {
            font-size: 1.18rem;
            color: #222;
            font-weight: 500;
            margin-bottom: 0.2rem;
            text-shadow: 0 1px 10px #fff8;
        }
        .privacy {
            font-size: 1rem;
            color: #2b2b2b;
            margin-bottom: 1.5rem;
            text-shadow: 0 1px 10px #fff3;
        }
        /* Inputs and Buttons */
        .stButton button {
            background: #fd1d1d;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 0.85rem 2.2rem;
            font-size: 1.15rem;
            transition: background 0.2s;
        }
        .stButton button:hover {
            background: #833ab4;
            color: #fff;
        }
        .stFileUploader {
            border-radius: 12px;
            border: 2px dashed #fd1d1d;
            background: #fcf8ff;
        }
        .stCheckbox > label {
            color: #833ab4 !important;
            font-weight: 500;
        }
        .stSelectbox > div {
            border-radius: 8px;
        }
        .stAlert {
            border-radius: 8px;
        }
        /* Captions block */
        .caption-block {
            font-size: 1.23rem !important;
            color: #232323 !important;
            font-weight: 500 !important;
            background: rgba(255,255,255,0.92);
            border-radius: 14px;
            padding: 1.2rem 1.3rem;
            margin: 1.3rem 0;
            box-shadow: 0 2px 12px #0001;
        }
        .stMarkdown ol, .stMarkdown ul {
            color: #363636 !important;
        }
        /* Misc */
        .stApp > header, .stApp > footer { background: transparent !important; }
    </style>
""", unsafe_allow_html=True)

# HEADER (Option 1: Logo + light bold title, larger font)
st.markdown("""
<div class="main-header">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png"
         style="width:54px; height:54px; border-radius:50%; box-shadow:0 4px 12px #0002;">
    <span class="main-header-text">
        Instagram Caption Assistant
    </span>
</div>
""", unsafe_allow_html=True)

# Description/instructions
st.markdown('<div class="subtitle">Upload an image or describe your post to get smart captions in any language!</div>', unsafe_allow_html=True)
st.markdown('<div class="privacy">No data stored. Fully private. ✨</div>', unsafe_allow_html=True)

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

def build_prompt(desc, n, style, length, emojis, hashtags, language):
    return f"""
    Generate {n} {style.lower()} Instagram captions for the post:
    "{desc}"
    Captions should be {length.lower()}.
    {'Include emojis.' if emojis else 'No emojis.'}
    {'Include hashtags.' if hashtags else 'No hashtags.'}
    Translate the captions to {language}.
    Format the captions as a numbered list.
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

n_captions = st.selectbox("Number of Captions", [1, 2, 5, 10])
caption_style = st.selectbox("Caption Style", ["Formal", "Informal", "Humorous", "Inspirational", "Poetic"])
caption_length = st.selectbox("Caption Length", ["Short", "Medium", "Long"])
emojis = st.checkbox("Include Emojis 😊", value=True)
hashtags = st.checkbox("Include Hashtags #️⃣", value=True)
language = st.selectbox("Output Language", ["English", "Hindi", "Telugu", "Tamil", "Kannada", "French"])

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
