import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import requests
import os

# --- Page Config ---
st.set_page_config(page_title="Interactive Poster Editor", page_icon="🌾", layout="wide")

# --- Resources Handling ---
@st.cache_resource
def get_font(size):
    font_url = "https://github.com/google/fonts/raw/main/ofl/robotocondensed/RobotoCondensed-Bold.ttf"
    font_path = "font_style.ttf"
    
    # ফন্ট ফাইল না থাকলে ডাউনলোড করবে
    if not os.path.exists(font_path):
        try:
            r = requests.get(font_url, timeout=10)
            with open(font_path, "wb") as f:
                f.write(r.content)
        except:
            pass
            
    # ফাইল থেকে লোড করার চেষ্টা করবে, না পারলে ডিফল্ট ফন্ট দিবে
    try:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
        else:
            return ImageFont.load_default()
    except:
        return ImageFont.load_default()

@st.cache_resource
def load_logo():
    logo_url = "https://raw.githubusercontent.com/arshadsamrat/files/main/paddy_logo_fixed.png"
    try:
        return Image.open(io.BytesIO(requests.get(logo_url).content)).convert("RGBA")
    except:
        return None

party_logo = load_logo()

# --- Sidebar Controls ---
st.sidebar.header("🛠️ Poster Editor")
uploaded_file = st.sidebar.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"])
user_name = st.sidebar.text_input("Candidate Name", "MISHKATUL ISLAM CHOWDHURY PAPPU")
area_text = st.sidebar.text_input("Area Text", "CHATTOGRAM 16 - BANSHKHALI")

st.sidebar.subheader("Adjust Positions")
name_y = st.sidebar.slider("Name (Up-Down)", 600, 1000, 785)
slogan_y = st.sidebar.slider("Slogan (Up-Down)", 600, 1000, 880)

# --- Poster Logic ---
if uploaded_file:
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (244, 42, 65, 255)) 
    draw = ImageDraw.Draw(poster)
    
    # Background
    inner_bg = Image.new('RGBA', (canvas_size-60, canvas_size-60), (0, 106, 78, 255))
    poster.paste(inner_bg, (30, 30))

    # Header Capsule
    draw.rounded_rectangle([200, 15, 880, 95], radius=40, fill="#ffd700")
    draw.text((540, 55), "ELECTION 2026 - PADDY SHEAF 🌾🌾", fill="black", font=get_font(45), anchor="mm")

    # Photo Processing
    user_img = Image.open(uploaded_file).convert("RGBA")
    img_size = (600, 600)
    user_img = ImageOps.fit(user_img, img_size, centering=(0.5, 0.5))
    mask = Image.new('L', img_size, 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.ellipse((0, 0, 600, 600), fill=255)
    
    # White Border
    draw.ellipse((230, 110, 850, 730), outline="white", width=15)
    poster.paste(user_img, (240, 120), mask)

    # Logos
    if party_logo:
        l_res = party_logo.resize((180, 180))
        poster.paste(l_res, (70, 100), l_res)
        poster.paste(l_res, (830, 100), l_res)

    # Texts
    draw.text((540, name_y), user_name.upper(), fill="#ffd700", font=get_font(80), anchor="mm")
    draw.text((540, slogan_y), "VOTE FOR PADDY SHEAF 🌾🌾", fill="white", font=get_font(55), anchor="mm")

    # Bottom Box
    draw.rounded_rectangle([250, 980, 830, 1055], radius=35, fill="#004d39")
    draw.text((540, 1018), area_text.upper(), fill="white", font=get_font(45), anchor="mm")

    # Show Output
    st.image(poster, use_container_width=True)
    
    # Download
    buf = io.BytesIO()
    poster.save(buf, format="PNG")
    st.download_button("📥 Download Poster", buf.getvalue(), "poster_2026.png")
else:
    st.info("👈 Please upload your photo to start editing!")

st.divider()
st.caption("Developed for 2026. গুপ্তধন শুধু আপনার জন্য।")
