import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import requests
import os

# --- Page Config ---
st.set_page_config(page_title="Election Poster Maker", page_icon="🇧🇩", layout="centered")

# --- Asset Loader (Fixed OSError) ---
@st.cache_resource
def load_assets():
    # ফন্ট ডাউনলোড করে লোকাল ফাইল হিসেবে সেভ করা হচ্ছে এরর এড়াতে
    font_path = "temp_font.ttf"
    font_url = "https://github.com/google/fonts/raw/main/ofl/robotocondensed/RobotoCondensed-Bold.ttf"
    
    if not os.path.exists(font_path):
        r = requests.get(font_url)
        with open(font_path, "wb") as f:
            f.write(r.content)
    
    # Party Logo
    logo_url = "https://raw.githubusercontent.com/arshadsamrat/files/main/paddy_logo_fixed.png" 
    try:
        logo_img = Image.open(io.BytesIO(requests.get(logo_url).content)).convert("RGBA")
    except:
        logo_img = None
    
    return font_path, logo_img

font_path, party_logo = load_assets()

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; color: #333; }
    .main-title { text-align: center; color: #006a4e; font-size: 28px; font-weight: bold; border-bottom: 3px solid #f42a41; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🇧🇩 Election Poster Maker 🇧🇩</h1>", unsafe_allow_html=True)

# --- Input ---
uploaded_file = st.file_uploader("📸 Upload Your Photo", type=["jpg", "png", "jpeg"])
user_name = st.text_input("✍️ Enter Your Name", value="MISHKATUL ISLAM CHOWDHURY PAPPA")
selected_slogan = st.selectbox("📣 Select Slogan", ["Your Vote, Your Voice!", "For a Better Banshkhali", "Development & Peace"])

if uploaded_file:
    # ১. ক্যানভাস এবং ব্যাকগ্রাউন্ড
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (244, 42, 65, 255)) 
    draw = ImageDraw.Draw(poster)
    
    # ভেতরের সবুজ ব্যাকগ্রাউন্ড
    inner_bg = Image.new('RGBA', (canvas_size-60, canvas_size-60), (0, 106, 78, 255))
    poster.paste(inner_bg, (30, 30))

    # ২. উপরের গোল্ডেন বার
    draw.rounded_rectangle([150, 10, 930, 80], radius=35, fill="#ffd700")
    try:
        font_title = ImageFont.truetype(font_path, 45)
        draw.text((540, 45), "Election Poster Maker 2026", fill="black", font=font_title, anchor="mm")
    except: pass

    # ৩. ইউজারের ছবি (Circular Frame)
    user_img = Image.open(uploaded_file).convert("RGBA")
    img_size = (620, 620)
    user_img = ImageOps.fit(user_img, img_size, centering=(0.5, 0.5))
    
    mask = Image.new('L', img_size, 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.ellipse((0, 0, 620, 620), fill=255)
    
    draw.ellipse((220, 100, 860, 740), outline="white", width=15)
    poster.paste(user_img, (230, 110), mask)

    # ৪. লোগো বসানো
    if party_logo:
        l_res = party_logo.resize((170, 170))
        poster.paste(l_res, (75, 100), l_res)
        poster.paste(l_res, (835, 100), l_res)

    # ৫. নিচের টেক্সট ডিজাইন
    try:
        font_name = ImageFont.truetype(font_path, 80)
        font_slogan = ImageFont.truetype(font_path, 55)
        font_sm = ImageFont.truetype(font_path, 45)
    except:
        font_name = font_slogan = font_sm = ImageFont.load_default()

    draw.text((540, 785), user_name.upper(), fill="#ffd700", font=font_name, anchor="mm")
    draw.text((540, 865), selected_slogan, fill="white", font=font_slogan, anchor="mm")
    draw.text((540, 935), "VOTE FOR PADDY SHEAF 🌾", fill="white", font=font_slogan, anchor="mm")

    # ৬. একদম নিচের এরিয়া বক্স
    draw.rounded_rectangle([270, 985, 810, 1055], radius=35, fill="#004d39")
    draw.text((540, 1020), "CHATTOGRAM 16 - BANSHKHALI", fill="white", font=font_sm, anchor="mm")

    # ৭. প্রদর্শন ও ডাউনলোড
    st.image(poster, use_container_width=True)
    
    final_buf = io.BytesIO()
    poster.save(final_buf, format="PNG")
    st.download_button("📥 Download This Poster", final_buf.getvalue(), "pappu_poster_2026.png", "image/png")

st.divider()
st.write("গুপ্তধন শুধু আপনার জন্য।")
