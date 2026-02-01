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
    .main-title { text-align: center; color: #ffd700; font-size: 32px; font-weight: bold; border-bottom: 3px solid #f42a41; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🇧🇩 নির্বাচনী পোস্টার মেকার 🇧🇩</h1>", unsafe_allow_html=True)

# --- Bengali Font & Logo Downloader ---
@st.cache_resource
def load_resources():
    # বাংলা ফন্ট ফিক্স করার জন্য Hind Siliguri Bold
    font_url = "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-Bold.ttf"
    font_data = io.BytesIO(requests.get(font_url).content)
    
    # ধানের শীষের লোগো (ট্রান্সপারেন্ট PNG)
    logo_url = "https://i.ibb.co/6yXm7vR/paddy-logo.png" 
    try:
        logo_img = Image.open(io.BytesIO(requests.get(logo_url).content)).convert("RGBA")
    except:
        logo_img = None
        
    return font_data, logo_img

font_data, paddy_logo = load_resources()

# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📸 নিজের ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])
    user_name = st.text_input("✍️ আপনার নাম", placeholder="উদা: মিশকাতুল ইসলাম")

with col2:
    slogan_options = [
        "১২ তারিখ সারাদিন ধানের শীষে ভোট দিন 🌾🌾",
        "পাপ্পা ভাইয়ের সালাম নিন, ধানের শীষে ভোট দিন",
        "তরুণ প্রবীণ মিলেমিশে, ভোট দেব ধানের শীষে",
        "তারুণ্যের প্রথম ভোট, ধানের শীষের জন্য হোক",
        "বাঁশখালীবাসীর মার্কা, ধানের শীষ মার্কা"
    ]
    selected_slogan = st.selectbox("📣 স্লোগান নির্বাচন করুন", slogan_options)

if uploaded_file is not None:
    # ১. ক্যানভাস তৈরি (১০৮০x১০৮০)
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255)) 
    draw = ImageDraw.Draw(poster)
    
    # ২. চারদিকের লাল বর্ডার (পতাকার থিম)
    border_width = 20
    draw.rectangle([0, 0, canvas_size, canvas_size], outline=(244, 42, 65, 255), width=border_width)

    # ৩. ইউজারের ছবি প্রসেসিং (Circular Frame with White Border)
    user_img = Image.open(uploaded_file).convert("RGBA")
    img_size = (620, 620)
    user_img = user_img.resize(img_size)
    
    # মাস্ক ও সাদা বর্ডার
    mask = Image.new('L', img_size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 620, 620), fill=255)
    
    # ছবির চারপাশে সাদা বৃত্তাকার বর্ডার
    draw.ellipse((230-15, 80-15, 850+15, 700+15), fill="white")
    poster.paste(user_img, (230, 80), mask)

    # ৪. ধানের শীষ লোগো (উপরে দুই পাশে)
    if paddy_logo:
        logo_res = paddy_logo.resize((160, 160))
        poster.paste(logo_res, (60, 60), logo_res) # বামে
        poster.paste(logo_res, (860, 60), logo_res) # ডানে

    # ৫. নিচের লাল ব্যানার ও সোনালী বর্ডার
    draw.rectangle([border_width, 740, canvas_size-border_width, 1060], fill=(244, 42, 65, 255))
    draw.rectangle([border_width, 735, canvas_size-border_width, 745], fill=(255, 215, 0, 255)) # Golden Line

    # ৬. বাংলা টেক্সট রেন্ডারিং (ফন্ট ফিক্সড)
    try:
        font_name = ImageFont.truetype(font_data, 65)
        font_slogan = ImageFont.truetype(font_data, 45)
        font_area = ImageFont.truetype(font_data, 35)
    except:
        font_name = ImageFont.load_default()
        font_slogan = ImageFont.load_default()
        font_area = ImageFont.load_default()

    # নাম (হলুদ রঙে বড় করে)
    display_name = f"শুভেচ্ছান্তে: {user_name}" if user_name else "মিশকাতুল ইসলাম চৌধুরী পাপ্পা"
    draw.text((canvas_size//2, 810), display_name, fill="#ffd700", font=font_name, anchor="mm")
    
    # স্লোগান (সাদা রঙে)
    draw.text((canvas_size//2, 910), selected_slogan, fill="white", font=font_slogan, anchor="mm")
    
    # দ্বিতীয় লাইন (পাপ্পা ভাইয়ের সালাম নিন)
    draw.text((canvas_size//2, 980), "পাপ্পা ভাইয়ের সালাম নিন, ধানের শীষে ভোট দিন", fill="white", font=font_slogan, anchor="mm")

    # এলাকার নাম (সবুজ ক্যাপসুলে)
    draw.rounded_rectangle([380, 1020, 700, 1065], radius=20, fill="#006a4e")
    draw.text((canvas_size//2, 1042), "চট্টগ্রাম ১৬ - বাঁশখালী", fill="white", font=font_area, anchor="mm")

    # ৭. ফাইনাল আউটপুট
    st.image(poster, caption="আপনার কাস্টম নির্বাচনী পোস্টার", use_container_width=True)
    
    # ডাউনলোড বাটন
    buf = io.BytesIO()
    poster.save(buf, format="PNG")
    st.download_button(label="📥 পোস্টার ডাউনলোড করুন", data=buf.getvalue(), file_name="election_poster_bd.png", mime="image/png")

st.divider()
st.caption("বাঁশখালীর ডিজিটাল প্রচারণা সহায়তায় - ২০২৬")
