import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

# --- Page Config ---
st.set_page_config(page_title="Election Poster Maker", page_icon="🌾", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #006a4e; color: white; }
    .main-title { text-align: center; color: #ffd700; font-size: 32px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🇧🇩 নির্বাচনী পোস্টার মেকার 🇧🇩</h1>", unsafe_allow_html=True)

# --- Bengali Font Downloader (বাংলা ফন্ট ফিক্স) ---
@st.cache_resource
def get_bengali_font():
    # Hind Siliguri Bold ফন্ট ডাউনলোড
    font_url = "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-Bold.ttf"
    r = requests.get(font_url)
    return io.BytesIO(r.content)

# --- ধান গাছ (Logo) Downloader ---
@st.cache_resource
def get_paddy_logo():
    # ধানের শীষের একটি ট্রান্সপারেন্ট পিএনজি লিঙ্ক (উদাহরণ হিসেবে)
    logo_url = "https://i.ibb.co/6yXm7vR/paddy-logo.png" 
    try:
        r = requests.get(logo_url)
        return Image.open(io.BytesIO(r.content)).convert("RGBA")
    except:
        return None

font_file = get_bengali_font()
paddy_logo = get_paddy_logo()

# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📸 আপনার ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])
    user_name = st.text_input("✍️ আপনার নাম", placeholder="উদা: মিশকাতুল ইসলাম")

with col2:
    slogan_options = [
        "১২ তারিখ সারাদিন ধানের শীষে ভোট দিন 🌾🌾",
        "পাপ্পা ভাইয়ের সালাম নিন, ধানের শীষে ভোট দিন",
        "তরুণ প্রবীণ মিলেমিশে, ভোট দেব ধানের শীষে",
        "তারুণ্যের প্রথম ভোট, ধানের শীষের জন্য হোক",
        "বাঁশখালীবাসীর মার্কা, ধানের শীষ মার্কা"
    ]
    selected_slogan = st.selectbox("📣 একটি স্লোগান নির্বাচন করুন", slogan_options)

if uploaded_file is not None:
    # ১. ক্যানভাস তৈরি
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255)) 
    draw = ImageDraw.Draw(poster)
    
    # ২. বাংলাদেশের পতাকার বর্ডার (লাল)
    border_width = 25
    draw.rectangle([0, 0, canvas_size, canvas_size], outline=(244, 42, 65, 255), width=border_width)

    # ৩. ইউজারের ছবি (গোলাকার)
    user_img = Image.open(uploaded_file).convert("RGBA")
    img_size = (620, 620)
    user_img = user_img.resize(img_size)
    
    mask = Image.new('L', img_size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 620, 620), fill=255)
    
    # সাদা সার্কেল বর্ডার ছবির পিছনে
    draw.ellipse((230-10, 80-10, 850+10, 700+10), fill="white")
    poster.paste(user_img, (230, 80), mask)

    # ৪. ধানের শীষ লোগো (উপরে দুই কোণায়)
    if paddy_logo:
        logo_res = paddy_logo.resize((150, 150))
        poster.paste(logo_res, (50, 50), logo_res) # বাম কোণায়
        poster.paste(logo_res, (880, 50), logo_res) # ডান কোণায়

    # ৫. নিচের ব্যানার (লাল)
    draw.rectangle([border_width, 760, canvas_size-border_width, 1050], fill=(244, 42, 65, 255))

    # ৬. বাংলা টেক্সট রেন্ডারিং
    try:
        font_name = ImageFont.truetype(font_file, 65)
        font_slogan = ImageFont.truetype(font_file, 45)
    except:
        font_name = ImageFont.load_default()
        font_slogan = ImageFont.load_default()

    name_to_print = user_name if user_name else "মিশকাতুল ইসলাম চৌধুরী পাপ্পা"
    draw.text((canvas_size//2, 830), name_to_print, fill="white", font=font_name, anchor="mm")
    draw.text((canvas_size//2, 930), selected_slogan, fill="yellow", font=font_slogan, anchor="mm")
    draw.text((canvas_size//2, 1000), "চট্টগ্রাম ১৬ - বাঁশখালী", fill="white", font=font_slogan, anchor="mm")

    # ৭. আউটপুট দেখানো
    st.image(poster, caption="আপনার কাস্টম পোস্টার", use_container_width=True)
    
    # ডাউনলোড বাটন
    buf = io.BytesIO()
    poster.save(buf, format="PNG")
    st.download_button(label="📥 পোস্টারটি ডাউনলোড করুন", data=buf.getvalue(), file_name="poster_2026.png", mime="image/png")

st.divider()
st.markdown("<p style='text-align: center;'>সবার আগে বাংলাদেশ | সবার আগে বাঁশখালী</p>", unsafe_allow_html=True)
