import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

# --- পেজ কনফিগারেশন ---
st.set_page_config(page_title="নির্বাচনী পোস্টার মেকার", page_icon="🌾", layout="centered")

# --- কাস্টম সিএসএস (ফেসবুক থিম লুক) ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; color: #1c1e21; } /* Facebook Light Gray Background */
    .main-title { 
        text-align: center; 
        color: #006a4e; 
        font-size: 32px; 
        font-weight: bold; 
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1877f2; /* Facebook Blue */
        color: white;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #166fe5;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'>🗳️ নির্বাচনী পোস্টার ও থিম মেকার</div>", unsafe_allow_html=True)

# --- ইনপুট সেকশন ---
with st.container():
    st.write("### 📸 আপনার তথ্য দিন")
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("আপনার ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])
        user_name = st.text_input("আপনার নাম লিখুন", placeholder="উদা: মিশকাতুল ইসলাম")
    
    with col2:
        slogan_options = [
            "১২ তারিখ সারাদিন ধানের শীষে ভোট দিন 🌾🌾",
            "পাপ্পা ভাইয়ের সালাম নিন, ধানের শীষে ভোট দিন",
            "তরুণ প্রবীণ মিলেমিশে, ভোট দেব ধানের শীষে",
            "তারুণ্যের প্রথম ভোট, ধানের শীষের জন্য হোক",
            "বাঁশখালীবাসীর মার্কা, ধানের শীষ মার্কা"
        ]
        selected_slogan = st.selectbox("একটি স্লোগান বেছে নিন", slogan_options)
        use_custom_bg = st.checkbox("লিডারের ব্যাকগ্রাউন্ড থিম ব্যবহার করুন", value=True)

if uploaded_file is not None:
    # ইউজারের ছবি লোড করা
    user_img = Image.open(uploaded_file).convert("RGBA")
    canvas_size = 1080
    
    # ব্যাকগ্রাউন্ড সিলেকশন
    if use_custom_bg:
        try:
            # এখানে আপনার দেওয়া ছবিটির সরাসরি লিঙ্ক দিন
            bg_url = "https://i.ibb.co/LzNfW8f/your-uploaded-image.jpg" 
            response = requests.get(bg_url)
            bg_img = Image.open(io.BytesIO(response.content)).convert("RGBA")
            frame = bg_img.resize((canvas_size, canvas_size))
        except:
            frame = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255)) # Default Green
    else:
        frame = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255))

    # ইউজারের ছবি মাঝখানে বসানো
    img_width, img_height = user_img.size
    aspect_ratio = img_width / img_height
    new_height = 680
    new_width = int(new_height * aspect_ratio)
    user_img = user_img.resize((new_width, new_height))
    
    x_offset = (canvas_size - new_width) // 2
    y_offset = 70
    frame.paste(user_img, (x_offset, y_offset), user_img if user_img.mode == 'RGBA' else None)
    
    # টেক্সট ও ব্যানার ডিজাইন (ফেসবুক স্টাইল)
    draw = ImageDraw.Draw(frame)
    
    # নিচের লাল ডাবল লেয়ার ব্যানার
    draw.rectangle([0, 780, canvas_size, canvas_size], fill=(244, 42, 65, 255)) # Red
    draw.rectangle([0, 770, canvas_size, 780], fill=(255, 215, 0, 255)) # Gold Line

    # ফন্ট লোড করা
    try:
        font_main = ImageFont.truetype("arial.ttf", 60)
        font_sub = ImageFont.truetype("arial.ttf", 45)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # বাংলা টেক্সট বসানো
    if user_name:
        draw.text((canvas_size//2, 840), f"শুভেচ্ছান্তে: {user_name}", fill="yellow", font=font_main, anchor="mm")
        draw.text((canvas_size//2, 940), selected_slogan, fill="white", font=font_sub, anchor="mm")
    else:
        draw.text((canvas_size//2, 890), selected_slogan, fill="white", font=font_main, anchor="mm")

    # আউটপুট দেখানো
    st.markdown("---")
    st.image(frame, caption="আপনার ফেসবুক প্রোফাইল থিম তৈরি!", use_container_width=True)
    
    # ডাউনলোড বাটন
    buf = io.BytesIO()
    frame.save(buf, format="PNG")
    st.download_button(
        label="📥 থিমটি ডাউনলোড করুন",
        data=buf.getvalue(),
        file_name="facebook_election_theme.png",
        mime="image/png"
    )

st.divider()
st.markdown("<p style='text-align: center; color: gray;'>১২ তারিখ সারাদিন ধানের শীষে ভোট দিন 🌾</p>", unsafe_allow_html=True)
