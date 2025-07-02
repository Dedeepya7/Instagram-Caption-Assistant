import os
import torch
import streamlit as st
from PIL import Image, UnidentifiedImageError
from transformers import BlipProcessor, BlipForConditionalGeneration
import google.generativeai as genai
from datetime import datetime
import streamlit.components.v1 as components

# Page config
st.set_page_config(page_title="Instagram Caption Assistant", layout="centered")

# ---- DREAMY CSS for Instagram gradient and floating logos ----
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Quicksand:wght@400;700&display=swap');
        .stApp {
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
        .dreamy-subtitle {
            font-family: 'Pacifico', cursive, 'Quicksand', sans-serif;
            font-size: 1.4rem;
            color: #fff;
            font-weight: 500;
            margin-bottom: 0.3rem;
            text-shadow: 0 4px 20px #a445b266, 0 1px 0 #fff6, 0 0px 12px #fff2;
            letter-spacing: 1.2px;
        }
        .dreamy-privacy {
            font-family: 'Quicksand', 'Poppins', sans-serif;
            font-size: 1.1rem;
            color: #fff;
            margin-bottom: 1.5rem;
            text-shadow: 0 1px 8px #fd5c6344, 0 1px 0 #fff9;
            letter-spacing: 0.7px;
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
        # .caption-block {
        #     font-size: 1.23rem !important;
        #     color: #232323 !important;
        #     font-weight: 500 !important;
        #     background: rgba(255,255,255,0.97);
        #     border-radius: 14px;
        #     padding: 1.2rem 1.3rem;
        #     margin: 1.3rem 0;
        #     box-shadow: 0 2px 12px #0001;
        # }
        .caption-block {
             font-size: 1.23rem !important;
             color: #232323 !important;
             font-weight: 500 !important;
             background: #fff !important;
             border-radius: 14px;
             padding: 1.2rem 1.3rem;
             margin: 1.3rem 0;
             box-shadow: 0 2px 12px #0001;
             border: 1.5px solid #e0e0e0;    
        }
        .stMarkdown ol, .stMarkdown ul {
            color: #363636 !important;
        }
        /* ---- Floating Instagram logos ---- */
        .bg-ig-float {
            position: fixed;
            z-index: 0;
            pointer-events: none;
            top: 0; left: 0; width: 100vw; height: 100vh;
            overflow: hidden;
        }
        .ig-float-img {
            position: absolute;
            opacity: 0.13;
            filter: drop-shadow(0 4px 14px #0004);
            animation: floatIG 19s linear infinite;
        }
        .ig-float-img:nth-child(1) { left: 5vw; top: 82vh; width: 64px; animation-duration: 17s; }
        .ig-float-img:nth-child(2) { left: 22vw; top: 66vh; width: 44px; animation-duration: 23s; }
        .ig-float-img:nth-child(3) { left: 70vw; top: 29vh; width: 40px; animation-duration: 19s; }
        .ig-float-img:nth-child(4) { left: 54vw; top: 75vh; width: 55px; animation-duration: 28s; }
        .ig-float-img:nth-child(5) { left: 85vw; top: 10vh; width: 50px; animation-duration: 20s; }
        @keyframes floatIG {
            0%   { transform: translateY(0) scale(1) rotate(0deg);}
            100% { transform: translateY(-105vh) scale(1.15) rotate(33deg);}
        }
        .stApp > header, .stApp > footer { background: transparent !important; }
    </style>
    <div class="bg-ig-float">
      <img class="ig-float-img" src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png">
      <img class="ig-float-img" src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png">
      <img class="ig-float-img" src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png">
      <img class="ig-float-img" src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png">
      <img class="ig-float-img" src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png">
    </div>
""", unsafe_allow_html=True)

# # --- Instagram-logo tracking cursor (optional, enabled by default) ---
# components.html("""
# <div id="ig-cursor" style="position:fixed;left:0;top:0;width:44px;height:44px;pointer-events:none;z-index:99;transition:transform 0.08s;">
#   <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" style="width:44px;height:44px;opacity:0.23;">
# </div>
# <script>
# const cursor = document.getElementById('ig-cursor');
# document.addEventListener('mousemove', (e) => {
#   cursor.style.transform = `translate(${e.clientX-22}px, ${e.clientY-22}px)`;
# });
# </script>
# """, height=60)

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

# Dreamy subtitle and privacy lines
st.markdown('<div class="dreamy-subtitle">Upload an image or describe your post to get smart captions in any language!</div>', unsafe_allow_html=True)
st.markdown('<div class="dreamy-subtitle">No data stored. Fully private. ✨</div>', unsafe_allow_html=True)

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

# --- PROMPT LOGIC: Improved language & translation handling ---
def build_prompt(desc, n, style, length, emojis, hashtags, language):
    if language.lower() == "english":
        return f"""
        Generate {n} unique Instagram captions in English ONLY for the following post:
        "{desc}"
        Each caption should be approximately the same length and level of detail. 
        Ensure all captions are similar in length (differ by no more than 1 sentence).
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
        Each caption should be approximately the same length and level of detail. 
        Ensure all captions are similar in length (differ by no more than 1 sentence).
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

n_captions = st.selectbox("Number of Captions", [1, 2, 5, 10])
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
            #st.markdown(f'<div class="caption-block">{captions}</div>', unsafe_allow_html=True)
            caption_lines = [line.strip() for line in captions.split('\n') if line.strip()]

            block_html = '<div class="caption-block"><ol style="margin:0;padding-left:1.3em;">'
            for line in caption_lines:
               # Remove "1. ", "2. ", etc. if present at the start
               if len(line) > 2 and line[1:3] == '. ' and line[0].isdigit():
                  text = line[3:]
               else:
                  text = line
               block_html += f'<li>{text}</li>'
            block_html += '</ol></div>'

            st.markdown(block_html, unsafe_allow_html=True)
            st.download_button("📥 Download Captions", captions, file_name=f"captions_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("Upload an image or enter a description to begin.")
