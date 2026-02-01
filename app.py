import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# --- Page Config ---
st.set_page_config(page_title="Election Poster Maker", page_icon="🌾", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #006a4e; color: white; }
    .main-title { text-align: center; color: #ffd700; font-size: 30px; font-weight: bold; border-bottom: 2px solid #f42a41; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🇧🇩 নির্বাচনী পোস্টার মেকার 🇧🇩</h1>", unsafe_allow_html=True)

# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📸 আপনার ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])
    user_name = st.text_input("✍️ আপনার নাম (ঐচ্ছিক)", placeholder="উদা: আপনার নাম")

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
    # ১. ক্যানভাস এবং ব্যাকগ্রাউন্ড সেটআপ
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255)) # গভীর সবুজ ব্যাকগ্রাউন্ড
    draw = ImageDraw.Draw(poster)

    # ২. ব্যাকগ্রাউন্ড ডিজাইন (আপনার দেওয়া ছবির মতো গ্রেডিয়েন্ট লুক)
    for i in range(canvas_size):
        alpha = int(255 * (i / canvas_size))
        draw.line([(0, i), (canvas_size, i)], fill=(0, 120, 80, alpha))

    # ৩. ইউজার ইমেজ প্রসেসিং (Circular Frame)
    user_img = Image.open(uploaded_file).convert("RGBA")
    size = (600, 600)
    user_img = user_img.resize(size)
    
    # মাস্ক তৈরি (গোলাকার করার জন্য)
    mask = Image.new('L', size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0) + size, fill=255)
    
    # বর্ডারসহ ছবি বসানো
    border_size = 15
    draw.ellipse((240-border_size, 100-border_size, 840+border_size, 700+border_size), fill="white")
    poster.paste(user_img, (240, 100), mask)

    # ৪. ব্যানার ডিজাইন (আপনার ছবির মতো লাল-সবুজ ওয়েভ)
    # লাল অংশ
    draw.rectangle([0, 750, canvas_size, 900], fill=(244, 42, 65, 255)) 
    # সবুজ অংশ
    draw.rectangle([0, 900, canvas_size, 1080], fill=(0, 106, 78, 255)) 
    # গোল্ডেন বর্ডার লাইন
    draw.rectangle([0, 745, canvas_size, 755], fill=(255, 215, 0, 255))

    # ৫. টেক্সট রাইটিং
    try:
        # ফন্ট পাথ (আপনার পিসিতে বা সার্ভারে এই ফন্ট থাকা লাগবে, নাহলে ডিফল্ট কাজ করবে)
        font_name = ImageFont.truetype("arial.ttf", 60)
        font_slogan = ImageFont.truetype("arial.ttf", 45)
    except:
        font_name = ImageFont.load_default()
        font_slogan = ImageFont.load_default()

    # নাম এবং ঠিকানা
    name_text = user_name if user_name else "মিশকাতুল ইসলাম চৌধুরী পাপ্পা"
    draw.text((canvas_size//2, 825), name_text, fill="white", font=font_name, anchor="mm")
    
    # স্লোগান
    draw.text((canvas_size//2, 980), selected_slogan, fill="yellow", font=font_slogan, anchor="mm")
    
    # এলাকা
    draw.text((canvas_size//2, 1040), "চট্টগ্রাম ১৬", fill="white", font=font_slogan, anchor="mm")

    # ৬. ফাইনাল ডিসপ্লে
    st.image(poster, caption="আপনার তৈরি করা পোস্টার", use_container_width=True)
    
    # ডাউনলোড বাটন
    buf = io.BytesIO()
    poster.save(buf, format="PNG")
    st.download_button(label="📥 পোস্টার ডাউনলোড করুন", data=buf.getvalue(), file_name="election_poster.png", mime="image/png")

st.divider()
st.info("আপনার ছবি আপলোড করলে সেটি স্বয়ংক্রিয়ভাবে গোলাকার ফ্রেমে বসে যাবে।")
