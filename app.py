import os
import torch
import streamlit as st
from PIL import Image, UnidentifiedImageError
from transformers import BlipProcessor, BlipForConditionalGeneration
import google.generativeai as genai
from datetime import datetime

st.set_page_config(page_title="Instagram Caption Assistant", layout="centered")

st.markdown("""
    <style>
        body {
            background: linear-gradient(120deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Poppins', 'Inter', sans-serif;
        }
        .main-card {
            background: #fff;
            border-radius: 20px;
            box-shadow: 0 6px 24px 0 rgba(0,0,0,0.07);
            padding: 2.5rem;
            margin-top: 2rem;
        }
        .stButton button {
            background: #6c63ff;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 0.75rem 2rem;
            transition: background 0.2s;
        }
        .stButton button:hover {
            background: #5947c4;
            color: #fff;
        }
        .stFileUploader {
            border-radius: 12px;
            border: 2px dashed #6c63ff;
            background: #f3f4f6;
        }
        .stCheckbox > label {
            color: #6c63ff !important;
            font-weight: 500;
        }
        .stSelectbox > div {
            border-radius: 8px;
        }
        .stAlert {
            border-radius: 8px;
        }
    </style>
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



st.title("📸 Instagram Caption Assistant")
st.markdown("<p style='color: #91c9f7;'>Upload an image or describe your post to get smart captions in any language!</p>", unsafe_allow_html=True)
st.markdown("<p style='color: #5ef78e;'>No data stored. Fully private. ✨</p>", unsafe_allow_html=True)  
# st.markdown("Upload image(s) or describe your post to generate smart captions!")

uploaded_files = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Robust image loading with error handling
images = []
if uploaded_files:
    for f in uploaded_files:
        try:
            images.append(Image.open(f))
        except UnidentifiedImageError:
            st.error(f"File {f.name} is not a valid image and was skipped.")

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
            st.write(captions)
            st.download_button("📥 Download Captions", captions, file_name=f"captions_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("Upload an image or enter a description to begin.")
