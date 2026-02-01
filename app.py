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
    .main-title { text-align: center; color: #ffd700; font-size: 35px; font-weight: bold; border-bottom: 2px solid #f42a41; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🇧🇩 নির্বাচনী পোস্টার মেকার 🇧🇩</h1>", unsafe_allow_html=True)

# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📸 আপনার ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])
    user_name = st.text_input("✍️ আপনার নাম (ঐচ্ছিক)", placeholder="উদা: আপনার নাম")
    use_custom_bg = st.checkbox("🖼️ লিডারের ব্যাকগ্রাউন্ড ব্যবহার করুন", value=True)

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
    # ১. ইউজার ইমেজ প্রসেসিং
    user_img = Image.open(uploaded_file).convert("RGBA")
    canvas_size = 1080
    
    # ২. ব্যাকগ্রাউন্ড তৈরি বা লোড
    if use_custom_bg:
        try:
            # আপনার দেওয়া ছবিটির সরাসরি লিঙ্ক (GitHub বা Image Hosting লিঙ্ক এখানে দিন)
            bg_url = "https://i.ibb.co/LzNfW8f/your-uploaded-image.jpg" 
            response = requests.get(bg_url)
            bg_img = Image.open(io.BytesIO(response.content)).convert("RGBA")
            frame = bg_img.resize((canvas_size, canvas_size))
        except:
            # লিঙ্ক কাজ না করলে ডিফল্ট সবুজ ব্যাকগ্রাউন্ড
            frame = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255))
    else:
        frame = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255))

    # ৩. ইউজারের ছবি রিসাইজ ও পজিশনিং
    img_width, img_height = user_img.size
    aspect_ratio = img_width / img_height
    new_height = 650
    new_width = int(new_height * aspect_ratio)
    user_img = user_img.resize((new_width, new_height))
    
    # ব্যাকগ্রাউন্ডের ওপর ইউজারের ছবি বসানো (মাঝখানে)
    x_offset = (canvas_size - new_width) // 2
    y_offset = 80
    frame.paste(user_img, (x_offset, y_offset), user_img if user_img.mode == 'RGBA' else None)
    
    # ৪. ব্যানার ও টেক্সট ড্রয়িং
    draw = ImageDraw.Draw(frame)
    # নিচে লাল ব্যানার
    draw.rectangle([0, 780, canvas_size, canvas_size], fill=(244, 42, 65, 255)) 
    draw.rectangle([0, 775, canvas_size, 785], fill=(255, 215, 0, 255)) # গোল্ডেন বর্ডার

    try:
        font_main = ImageFont.truetype("arial.ttf", 55)
        font_sub = ImageFont.truetype("arial.ttf", 42)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # নাম ও স্লোগান বসানো
    if user_name:
        draw.text((canvas_size//2, 840), f"শুভেচ্ছান্তে: {user_name}", fill="yellow", font=font_main, anchor="mm")
        draw.text((canvas_size//2, 940), selected_slogan, fill="white", font=font_sub, anchor="mm")
    else:
        draw.text((canvas_size//2, 890), selected_slogan, fill="white", font=font_main, anchor="mm")

    # ৫. রেজাল্ট দেখানো
    st.image(frame, caption="আপনার কাস্টম পোস্টার তৈরি হয়ে গেছে!", use_container_width=True)
    
    # ডাউনলোড বাটন
    buf = io.BytesIO()
    frame.save(buf, format="PNG")
    st.download_button(label="📥 পোস্টার ডাউনলোড করুন", data=buf.getvalue(), file_name=f"poster_{user_name}.png", mime="image/png")

st.info("দ্রষ্টব্য: আপনি 'লিডারের ব্যাকগ্রাউন্ড' অপশনটি টিক দিয়ে সেই কাস্টম ইমেজটি ব্যবহার করতে পারেন।")
