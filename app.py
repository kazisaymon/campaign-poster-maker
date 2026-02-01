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
    .main-title { text-align: center; color: #ffd700; font-size: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🇧🇩 নির্বাচনী পোস্টার মেকার 🇧🇩</h1>", unsafe_allow_html=True)

# --- Font Downloader (বাংলা টেক্সট ফিক্স করার জন্য) ---
@st.cache_resource
def get_bengali_font():
    # আদশলিপি বা কোনো ফ্রি বাংলা ফন্ট ডাউনলোড
    font_url = "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-Bold.ttf"
    r = requests.get(font_url)
    return io.BytesIO(r.content)

font_file = get_bengali_font()

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
    # ১. ক্যানভাস ও বর্ডার ডিজাইন (BD Flag Theme)
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255)) # সবুজ ব্যাকগ্রাউন্ড
    draw = ImageDraw.Draw(poster)
    
    # ২. পতাকার বর্ডার (লাল বর্ডার)
    border_width = 30
    draw.rectangle([0, 0, canvas_size, canvas_size], outline=(244, 42, 65, 255), width=border_width)

    # ৩. ইউজার ইমেজ প্রসেসিং
    user_img = Image.open(uploaded_file).convert("RGBA")
    user_img = user_img.resize((600, 600))
    
    # গোলাকার মাস্ক
    mask = Image.new('L', (600, 600), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 600, 600), fill=255)
    
    # ছবি বসানো
    poster.paste(user_img, (240, 100), mask)

    # ৪. ব্যানার (নিচের লাল অংশ)
    draw.rectangle([border_width, 750, canvas_size-border_width, 1050], fill=(244, 42, 65, 255))

    # ৫. বাংলা টেক্সট রেন্ডারিং (ফন্ট ফিক্সড)
    try:
        font_name = ImageFont.truetype(font_file, 65)
        font_slogan = ImageFont.truetype(font_file, 45)
    except:
        font_name = ImageFont.load_default()
        font_slogan = ImageFont.load_default()

    # নাম ও স্লোগান
    name_to_print = f"শুভেচ্ছান্তে: {user_name}" if user_name else "মিশকাতুল ইসলাম চৌধুরী পাপ্পা"
    draw.text((canvas_size//2, 830), name_to_print, fill="white", font=font_name, anchor="mm")
    draw.text((canvas_size//2, 930), selected_slogan, fill="yellow", font=font_slogan, anchor="mm")
    draw.text((canvas_size//2, 1000), "চট্টগ্রাম ১৬ - বাঁশখালী", fill="white", font=font_slogan, anchor="mm")

    # ৬. ফাইনাল ডিসপ্লে
    st.image(poster, caption="আপনার পোস্টার তৈরি হয়েছে", use_container_width=True)
    
    # ডাউনলোড
    buf = io.BytesIO()
    poster.save(buf, format="PNG")
    st.download_button(label="📥 পোস্টার ডাউনলোড করুন", data=buf.getvalue(), file_name="poster_bd.png", mime="image/png")

st.divider()
st.info("সঠিকভাবে বাংলা টেক্সট না আসলে পেজটি একবার রিফ্রেশ করুন।")
