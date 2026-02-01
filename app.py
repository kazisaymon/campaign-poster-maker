import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

# --- ১. রিসোর্স লোডার (Unicode Bengali Font) ---
@st.cache_resource
def load_bengali_font():
    # এই ফন্টটি বিজয় ৫২ বা যে কোনো কিবোর্ড দিয়ে লেখা ইউনিকোড টেক্সট সাপোর্ট করবে
    font_url = "https://github.com/google/fonts/raw/main/ofl/notosansbengali/NotoSansBengali-Bold.ttf"
    try:
        font_data = requests.get(font_url).content
        return io.BytesIO(font_data)
    except:
        return None

font_file = load_bengali_font()

# --- ২. অ্যাপ ডিজাইন ---
st.set_page_config(page_title="Poster Maker 2026", page_icon="🌾")

st.markdown("""
    <style>
    .stApp { background-color: #006a4e; color: white; }
    .main-title { text-align: center; color: #ffd700; font-size: 32px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🇧🇩 নির্বাচনী পোস্টার মেকার 🇧🇩</h1>", unsafe_allow_html=True)

# --- ৩. ইনপুট ---
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📸 নিজের ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])
    user_name = st.text_input("✍️ আপনার নাম", value="মিশকাতুল ইসলাম চৌধুরী পাপ্পা")

with col2:
    slogan = st.selectbox("📣 স্লোগান নির্বাচন করুন", [
        "১২ তারিখ সারাদিন ধানের শীষে ভোট দিন 🌾🌾",
        "তরুণ প্রবীণ মিলেমিশে, ভোট দেব ধানের শীষে",
        "পাপ্পা ভাইয়ের সালাম নিন, ধানের শীষে ভোট দিন"
    ])

# --- ৪. পোস্টার প্রসেসিং ---
if uploaded_file and font_file:
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255))
    draw = ImageDraw.Draw(poster)
    
    # বর্ডার
    draw.rectangle([0, 0, canvas_size, canvas_size], outline=(244, 42, 65, 255), width=25)

    # ইউজার ইমেজ
    user_img = Image.open(uploaded_file).convert("RGBA")
    user_img = user_img.resize((620, 620))
    mask = Image.new('L', (620, 620), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 620, 620), fill=255)
    
    draw.ellipse((220, 70, 860, 710), fill="white")
    poster.paste(user_img, (230, 80), mask)

    # নিচের লাল প্যানেল
    draw.rectangle([25, 750, 1055, 1055], fill=(244, 42, 65, 255))

    # টেক্সট রেন্ডারিং (বিজয় ৫২ কিবোর্ড সাপোর্ট)
    try:
        font_lg = ImageFont.truetype(font_file, 75)
        font_sm = ImageFont.truetype(font_file, 45)
    except:
        font_lg = font_sm = ImageFont.load_default()

    # টেক্সট গুলো বসানো
    draw.text((540, 830), user_name, fill="#ffd700", font=font_lg, anchor="mm")
    draw.text((540, 930), slogan, fill="white", font=font_sm, anchor="mm")
    draw.text((540, 1010), "চট্টগ্রাম ১৬ - বাঁশখালী", fill="white", font=font_sm, anchor="mm")

    # আউটপুট
    st.image(poster, use_container_width=True)
    
    # ডাউনলোড
    buf = io.BytesIO()
    poster.save(buf, format="PNG")
    st.download_button("📥 পোস্টার ডাউনলোড করুন", buf.getvalue(), "poster.png", "image/png")

st.divider()
st.caption("Developed for 2026. গুপ্তধন শুধু আপনার জন্য।")
