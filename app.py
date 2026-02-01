import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# --- Page Config ---
st.set_page_config(page_title="Election Poster Maker", page_icon="🌾", layout="centered")

# --- Custom Styling (BD Flag Theme) ---
st.markdown("""
    <style>
    .stApp { background-color: #006a4e; color: white; }
    .main-title { text-align: center; color: #ffd700; font-size: 35px; font-weight: bold; border-bottom: 2px solid #f42a41; padding-bottom: 10px; }
    .instruction { text-align: center; color: #e0e0e0; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🇧🇩 নির্বাচনী পোস্টার মেকার 🇧🇩</h1>", unsafe_allow_html=True)
st.markdown("<p class='instruction'>আপনার ছবি ও পছন্দের স্লোগান দিয়ে পোস্টার তৈরি করুন</p>", unsafe_allow_html=True)

# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📸 আপনার ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])
    user_name = st.text_input("✍️ আপনার নাম (ঐচ্ছিক)", placeholder="উদা: আপনার নাম")

with col2:
    # Slogan Selection List
    slogan_options = [
        "১২ তারিখ সারাদিন ধানের শীষে ভোট দিন 🌾🌾",
        "পাপ্পা ভাইয়ের সালাম নিন, ধানের শীষে ভোট দিন",
        "তরুণ প্রবীণ মিলেমিশে, ভোট দেব ধানের শীষে",
        "তারুণ্যের প্রথম ভোট, ধানের শীষের জন্য হোক",
        "বাঁশখালীবাসীর মার্কা, ধানের শীষ মার্কা"
    ]
    selected_slogan = st.selectbox("📣 একটি স্লোগান নির্বাচন করুন", slogan_options)

if uploaded_file is not None:
    # Load user image
    user_img = Image.open(uploaded_file).convert("RGBA")
    
    # Create Canvas
    canvas_size = 1080
    frame = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255)) 
    
    # Resize user image
    img_width, img_height = user_img.size
    aspect_ratio = img_width / img_height
    new_height = 700
    new_width = int(new_height * aspect_ratio)
    user_img = user_img.resize((new_width, new_height))
    
    # Center paste
    x_offset = (canvas_size - new_width) // 2
    frame.paste(user_img, (x_offset, 50), user_img if user_img.mode == 'RGBA' else None)
    
    # Draw Banner
    draw = ImageDraw.Draw(frame)
    draw.rectangle([0, 750, canvas_size, canvas_size], fill=(244, 42, 65, 255)) # Red Banner
    draw.rectangle([0, 745, canvas_size, 755], fill=(255, 215, 0, 255)) # Gold Border

    # Font logic
    try:
        font_main = ImageFont.truetype("arial.ttf", 55)
        font_sub = ImageFont.truetype("arial.ttf", 45)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Draw Text
    if user_name:
        draw.text((canvas_size//2, 810), f"শুভেচ্ছান্তে: {user_name}", fill="yellow", font=font_main, anchor="mm")
        draw.text((canvas_size//2, 910), selected_slogan, fill="white", font=font_sub, anchor="mm")
    else:
        # If no name, make slogan bigger and centered
        draw.text((canvas_size//2, 870), selected_slogan, fill="white", font=font_main, anchor="mm")

    # Final Display
    st.image(frame, caption="আপনার কাস্টম নির্বাচনী পোস্টার", use_container_width=True)
    
    # Download Link
    buf = io.BytesIO()
    frame.save(buf, format="PNG")
    st.download_button(
        label="📥 পোস্টারটি ডাউনলোড করুন",
        data=buf.getvalue(),
        file_name="election_poster.png",
        mime="image/png"
    )

st.divider()
st.info("বাঁশখালী ও চট্টগ্রামের সকল ভাইদের জন্য এই ডিজিটাল প্রচারণার সুবিধা।")
