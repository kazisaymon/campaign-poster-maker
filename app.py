import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

# --- Page Config ---
st.set_page_config(page_title="Election Poster Maker", page_icon="🌾", layout="centered")

# --- Bengali Font & Asset Loader ---
@st.cache_resource
def load_assets():
    # Hind Siliguri Bold font download for Bengali support
    font_url = "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-Bold.ttf"
    font_bytes = requests.get(font_url).content
    
    # Paddy Logo (Paddy sheaf)
    logo_url = "https://raw.githubusercontent.com/arshadsamrat/files/main/paddy_logo_fixed.png" 
    try:
        logo_img = Image.open(io.BytesIO(requests.get(logo_url).content)).convert("RGBA")
    except:
        logo_img = None
    return font_bytes, logo_img

font_data, paddy_logo = load_assets()

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #006a4e; color: white; }
    .main-title { text-align: center; color: #ffd700; font-size: 30px; font-weight: bold; border-bottom: 3px solid #f42a41; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🇧🇩 নির্বাচনী পোস্টার মেকার ২০২৬ 🇧🇩</h1>", unsafe_allow_html=True)

# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📸 নিজের ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])
    user_name = st.text_input("✍️ আপনার নাম", value="মিশকাতুল ইসলাম চৌধুরী পাপ্পা")

with col2:
    slogan_options = [
        "import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

# --- Page Config ---
st.set_page_config(page_title="Election Poster Maker", page_icon="🌾", layout="centered")

# --- Bengali Font & Asset Loader ---
@st.cache_resource
def load_assets():
    # Hind Siliguri Bold font download for Bengali support
    font_url = "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-Bold.ttf"
    font_bytes = requests.get(font_url).content
    
    # Paddy Logo (Paddy sheaf)
    logo_url = "https://raw.githubusercontent.com/arshadsamrat/files/main/paddy_logo_fixed.png" 
    try:
        logo_img = Image.open(io.BytesIO(requests.get(logo_url).content)).convert("RGBA")
    except:
        logo_img = None
    return font_bytes, logo_img

font_data, paddy_logo = load_assets()

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #006a4e; color: white; }
    .main-title { text-align: center; color: #ffd700; font-size: 30px; font-weight: bold; border-bottom: 3px solid #f42a41; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🇧🇩 নির্বাচনী পোস্টার মেকার ২০২৬ 🇧🇩</h1>", unsafe_allow_html=True)

# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📸 নিজের ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])
    user_name = st.text_input("✍️ আপনার নাম", value="মিশকাতুল ইসলাম চৌধুরী পাপ্পা")

with col2:
    slogan_options = [
        "১২ তারিখ সারাদিন ধানের শীষে ভোট দিন 🌾🌾",
        "তরুণ প্রবীণ মিলেমিশে, ভোট দেব ধানের শীষে",
        "তারুণ্যের প্রথম ভোট, ধানের শীষের জন্য হোক",
        "বাঁশখালীবাসীর মার্কা, ধানের শীষ মার্কা",
        "পাপ্পা ভাইয়ের সালাম নিন, ধানের শীষে ভোট দিন"
    ]
    selected_slogan = st.selectbox("📣 স্লোগান নির্বাচন করুন", slogan_options)

# --- Poster Generation Logic ---
if uploaded_file:
    # Canvas (1080x1080)
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255))
    draw = ImageDraw.Draw(poster)
    
    # Red Border (Flag theme)
    b_width = 25
    draw.rectangle([0, 0, canvas_size, canvas_size], outline=(244, 42, 65, 255), width=b_width)

    # User Image Processing
    user_img = Image.open(uploaded_file).convert("RGBA")
    img_size = (620, 620)
    user_img = user_img.resize(img_size)
    
    mask = Image.new('L', img_size, 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.ellipse((0, 0, 620, 620), fill=255)
    
    # White circle behind photo
    draw.ellipse((230-15, 80-15, 850+15, 700+15), fill="white")
    poster.paste(user_img, (230, 80), mask)

    # Paddy Logo Placement
    if paddy_logo:
        l_res = paddy_logo.resize((180, 180))
        poster.paste(l_res, (60, 60), l_res)
        poster.paste(l_res, (840, 60), l_res)

    # Bottom Banner and Golden Line
    draw.rectangle([b_width, 740, canvas_size-b_width, 1060], fill=(244, 42, 65, 255))
    draw.rectangle([b_width, 735, canvas_size-b_width, 745], fill=(255, 215, 0, 255))

    # Font Setup
    try:
        font_lg = ImageFont.truetype(io.BytesIO(font_data), 70)
        font_md = ImageFont.truetype(io.BytesIO(font_data), 45)
        font_sm = ImageFont.truetype(io.BytesIO(font_data), 35)
    except:
        font_lg = font_md = font_sm = ImageFont.load_default()

    # Drawing Bengali Text
    draw.text((540, 810), user_name, fill="#ffd700", font=font_lg, anchor="mm")
    draw.text((540, 910), selected_slogan, fill="white", font=font_md, anchor="mm")
    draw.text((540, 980), "পাপ্পা ভাইয়ের সালাম নিন, ধানের শীষে ভোট দিন", fill="white", font=font_md, anchor="mm")
    
    # District Box
    draw.rounded_rectangle([380, 1015, 700, 1065], radius=20, fill="#006a4e")
    draw.text((540, 1038), "চট্টগ্রাম ১৬ - বাঁশখালী", fill="white", font=font_sm, anchor="mm")

    # Final Display
    st.image(poster, use_container_width=True)
    
    # Download Button
    final_buf = io.BytesIO()
    poster.save(final_buf, format="PNG")
    st.download_button("📥 পোস্টার ডাউনলোড করুন", final_buf.getvalue(), "election_poster.png", "image/png")

st.divider()
# Saved Info Implementation
st.caption("Developed for 2026. গুপ্তধন শুধু আপনার জন্য।")"
    ]
    selected_slogan = st.selectbox("📣 স্লোগান নির্বাচন করুন", slogan_options)

# --- Poster Generation Logic ---
if uploaded_file:
    # Canvas (1080x1080)
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255))
    draw = ImageDraw.Draw(poster)
    
    # Red Border (Flag theme)
    b_width = 25
    draw.rectangle([0, 0, canvas_size, canvas_size], outline=(244, 42, 65, 255), width=b_width)

    # User Image Processing
    user_img = Image.open(uploaded_file).convert("RGBA")
    img_size = (620, 620)
    user_img = user_img.resize(img_size)
    
    mask = Image.new('L', img_size, 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.ellipse((0, 0, 620, 620), fill=255)
    
    # White circle behind photo
    draw.ellipse((230-15, 80-15, 850+15, 700+15), fill="white")
    poster.paste(user_img, (230, 80), mask)

    # Paddy Logo Placement
    if paddy_logo:
        l_res = paddy_logo.resize((180, 180))
        poster.paste(l_res, (60, 60), l_res)
        poster.paste(l_res, (840, 60), l_res)

    # Bottom Banner and Golden Line
    draw.rectangle([b_width, 740, canvas_size-b_width, 1060], fill=(244, 42, 65, 255))
    draw.rectangle([b_width, 735, canvas_size-b_width, 745], fill=(255, 215, 0, 255))

    # Font Setup
    try:
        font_lg = ImageFont.truetype(io.BytesIO(font_data), 70)
        font_md = ImageFont.truetype(io.BytesIO(font_data), 45)
        font_sm = ImageFont.truetype(io.BytesIO(font_data), 35)
    except:
        font_lg = font_md = font_sm = ImageFont.load_default()

    # Drawing Bengali Text
    draw.text((540, 810), user_name, fill="#ffd700", font=font_lg, anchor="mm")
    draw.text((540, 910), selected_slogan, fill="white", font=font_md, anchor="mm")
    draw.text((540, 980), "পাপ্পা ভাইয়ের সালাম নিন, ধানের শীষে ভোট দিন", fill="white", font=font_md, anchor="mm")
    
    # District Box
    draw.rounded_rectangle([380, 1015, 700, 1065], radius=20, fill="#006a4e")
    draw.text((540, 1038), "চট্টগ্রাম ১৬ - বাঁশখালী", fill="white", font=font_sm, anchor="mm")

    # Final Display
    st.image(poster, use_container_width=True)
    
    # Download Button
    final_buf = io.BytesIO()
    poster.save(final_buf, format="PNG")
    st.download_button("📥 পোস্টার ডাউনলোড করুন", final_buf.getvalue(), "election_poster.png", "image/png")

st.divider()
# Saved Info Implementation
st.caption("Developed for 2026. গুপ্তধন শুধু আপনার জন্য।")
