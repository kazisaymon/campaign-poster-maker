import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import requests
import math

# --- Page Config ---
st.set_page_config(page_title="Election Poster Maker", page_icon="🇧🇩", layout="centered")

# --- Asset Loader ---
@st.cache_resource
def load_assets():
    # Roboto Condensed for clear English text
    font_url = "https://github.com/google/fonts/raw/main/ofl/robotocondensed/RobotoCondensed-Bold.ttf"
    font_bytes = requests.get(font_url).content
    
    # Party Logo ( ধান ও চাকা)
    logo_url = "https://raw.githubusercontent.com/arshadsamrat/files/main/paddy_logo_fixed.png" 
    try:
        logo_img = Image.open(io.BytesIO(requests.get(logo_url).content)).convert("RGBA")
    except:
        logo_img = None
    return font_bytes, logo_img

font_data, party_logo = load_assets()

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; color: #333; }
    .main-title { text-align: center; color: #006a4e; font-size: 28px; font-weight: bold; border-bottom: 3px solid #f42a41; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🇧🇩 Election Poster Maker 🇧🇩</h1>", unsafe_allow_html=True)

# --- Input ---
uploaded_file = st.file_uploader("📸 Upload Your High Quality Photo", type=["jpg", "png", "jpeg"])
user_name = st.text_input("✍️ Enter Your Name", value="MISHKATUL ISLAM CHOWDHURY PAPPA")
selected_slogan = st.selectbox("📣 Select Slogan", ["Your Vote, Your Voice!", "For a Better Banshkhali", "Development & Peace"])

if uploaded_file:
    # ১. ক্যানভাস এবং ব্যাকগ্রাউন্ড
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (244, 42, 65, 255)) # লাল বাইরের ফ্রেম
    draw = ImageDraw.Draw(poster)
    
    # ভেতরের সবুজ ব্যাকগ্রাউন্ড (গ্রেডিয়েন্ট লুকের জন্য)
    inner_bg = Image.new('RGBA', (canvas_size-60, canvas_size-60), (0, 106, 78, 255))
    poster.paste(inner_bg, (30, 30))

    # ২. উপরের টাইটেল বার (গোল্ডেন)
    draw.rounded_rectangle([150, 10, 930, 80], radius=35, fill="#ffd700")
    try:
        font_title = ImageFont.truetype(io.BytesIO(font_data), 50)
        draw.text((540, 45), "Election Poster Maker 2026", fill="black", font=font_title, anchor="mm")
    except: pass

    # ৩. ইউজারের ছবি (বৃত্তাকার এবং গ্লো ইফেক্ট)
    user_img = Image.open(uploaded_file).convert("RGBA")
    img_size = (600, 600)
    user_img = ImageOps.fit(user_img, img_size, centering=(0.5, 0.5))
    
    mask = Image.new('L', img_size, 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.ellipse((0, 0, 600, 600), fill=255)
    
    # ছবির বর্ডার
    draw.ellipse((230, 110, 850, 730), outline="white", width=15)
    poster.paste(user_img, (240, 120), mask)

    # ৪. লোগো বসানো (টপ কর্নার)
    if party_logo:
        l_res = party_logo.resize((160, 160))
        poster.paste(l_res, (80, 100), l_res)
        poster.paste(l_res, (840, 100), l_res)

    # ৫. নিচের টেক্সট প্যানেল
    # নামের লেখা (বড় এবং গোল্ডেন)
    font_name = ImageFont.truetype(io.BytesIO(font_data), 80)
    draw.text((540, 780), user_name.upper(), fill="#ffd700", font=font_name, anchor="mm")
    
    # স্লোগান এবং ধানের শীষ লেখা
    font_slogan = ImageFont.truetype(io.BytesIO(font_data), 55)
    draw.text((540, 860), selected_slogan, fill="white", font=font_slogan, anchor="mm")
    draw.text((540, 930), "VOTE FOR PADDY SHEAF 🌾", fill="white", font=font_slogan, anchor="mm")

    # ৬. একদম নিচের ক্যাপসুল বক্স (সবুজ)
    draw.rounded_rectangle([280, 980, 800, 1050], radius=35, fill="#004d39")
    font_sm = ImageFont.truetype(io.BytesIO(font_data), 45)
    draw.text((540, 1015), "CHATTOGRAM 16 - BANSHKHALI", fill="white", font=font_sm, anchor="mm")

    # ৭. প্রদর্শন
    st.image(poster, use_container_width=True)
    
    # ডাউনলোড
    final_buf = io.BytesIO()
    poster.save(final_buf, format="PNG")
    st.download_button("📥 Download This Poster", final_buf.getvalue(), "pappu_poster_2026.png", "image/png")

st.divider()
st.info("আপনার স্যাম্পল ফটোর মতো লাল বর্ডার, গোল্ডেন টাইটেল এবং প্রফেশনাল অ্যালাইনমেন্ট সেট করা হয়েছে।")
st.write("গুপ্তধন শুধু আপনার জন্য।")
