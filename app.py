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

# --- Resources Loader ---
@st.cache_resource
def load_assets():
    # বাংলা ফন্ট (Hind Siliguri) ডাউনলোড
    font_url = "https://github.com/google/fonts/raw/main/ofl/hindsiliguri/HindSiliguri-Bold.ttf"
    font_res = requests.get(font_url).content
    
    # ধানের শীষ লোগো (আপনার দেয়া ছবির সাথে মিল রেখে)
    logo_url = "https://raw.githubusercontent.com/arshadsamrat/files/main/paddy_logo_fixed.png" 
    try:
        logo_res = Image.open(io.BytesIO(requests.get(logo_url).content)).convert("RGBA")
    except:
        logo_res = None
    return font_res, logo_res

font_bytes, paddy_logo = load_assets()

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📸 নিজের ছবি আপলোড করুন", type=["jpg", "png", "jpeg"])
    user_name = st.text_input("✍️ আপনার নাম", value="মিশকাতুল ইসলাম চৌধুরী পাপ্পা")

with col2:
    slogan_options = [
        "১২ তারিখ সারাদিন ধানের শীষে ভোট দিন 🌾🌾",
        "তরুণ প্রবীণ মিলেমিশে, ভোট দেব ধানের শীষে",
        "তারুণ্যের প্রথম ভোট, ধানের শীষের জন্য হোক",
        "বাঁশখালীবাসীর মার্কা, ধানের শীষ মার্কা"
    ]
    selected_slogan = st.selectbox("📣 স্লোগান নির্বাচন করুন", slogan_options)

if uploaded_file:
    # ১. পোস্টার ক্যানভাস (সবুজ ব্যাকগ্রাউন্ড)
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (0, 106, 78, 255))
    draw = ImageDraw.Draw(poster)
    
    # ২. লাল বর্ডার
    b_width = 25
    draw.rectangle([0, 0, canvas_size, canvas_size], outline=(244, 42, 65, 255), width=b_width)

    # ৩. ইউজার ইমেজ (গোলাকার সাদা ফ্রেম সহ)
    user_img = Image.open(uploaded_file).convert("RGBA")
    img_size = (600, 600)
    user_img = user_img.resize(img_size)
    
    mask = Image.new('L', img_size, 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.ellipse((0, 0, 600, 600), fill=255)
    
    # সাদা বর্ডার সার্কেল
    draw.ellipse((240-15, 80-15, 840+15, 680+15), fill="white")
    poster.paste(user_img, (240, 80), mask)

    # ৪. লোগো বসানো (উপরে দুই কোণায়)
    if paddy_logo:
        l_size = (180, 180)
        paddy_res = paddy_logo.resize(l_size)
        poster.paste(paddy_res, (60, 60), paddy_res) # Left
        poster.paste(paddy_res, (840, 60), paddy_res) # Right

    # ৫. নিচের লাল প্যানেল ও গোল্ডেন লাইন
    draw.rectangle([b_width, 740, canvas_size-b_width, 1055], fill=(244, 42, 65, 255))
    draw.rectangle([b_width, 735, canvas_size-b_width, 745], fill=(255, 215, 0, 255))

    # ৬. বাংলা টেক্সট রেন্ডারিং
    try:
        font_lg = ImageFont.truetype(io.BytesIO(font_bytes), 70)
        font_md = ImageFont.truetype(io.BytesIO(font_bytes), 45)
    except:
        font_lg = ImageFont.load_default()
        font_md = ImageFont.load_default()

    # নাম এবং স্লোগান লেখা
    draw.text((540, 815), user_name, fill="#ffd700", font=font_lg, anchor="mm")
    draw.text((540, 915), selected_slogan, fill="white", font=font_md, anchor="mm")
    draw.text((540, 985), "পাপ্পা ভাইয়ের সালাম নিন, ধানের শীষে ভোট দিন", fill="white", font=font_md, anchor="mm")
    
    # চট্টগ্রাম ১৬ বক্স
    draw.rounded_rectangle([380, 1015, 700, 1065], radius=20, fill="#006a4e")
    draw.text((540, 1038), "চট্টগ্রাম ১৬ - বাঁশখালী", fill="white", font=font_md, anchor="mm")

    # ৭. প্রদর্শন ও ডাউনলোড
    st.image(poster, use_container_width=True)
    
    final_buf = io.BytesIO()
    poster.save(final_buf, format="PNG")
    st.download_button("📥 পোস্টার ডাউনলোড করুন", final_buf.getvalue(), "election_poster.png", "image/png")

st.divider()
st.write("গুপ্তধন শুধু আপনার জন্য।") # আপনার নির্দেশানুযায়ী সংরক্ষিত তথ্য

### **কিভাবে এটি কাজ করবে?**
1.  **বাংলা ফন্ট:** আমি `Hind Siliguri` ফন্টটি সরাসরি কোডের মাধ্যমে ডাউনলোড করার ব্যবস্থা করেছি, তাই আপনার ছবিতে এখন বাংলা লেখাগুলো একদম পরিষ্কার আসবে।
2.  **লোগো সাপোর্ট:** উপরে দুই কোণায় **ধানের শীষ** লোগোটি সুন্দরভাবে সেট করা হয়েছে।
3.  **সাদা ফ্রেম:** আপনার ছবির চারপাশে একটি সাদা বৃত্তাকার বর্ডার দেওয়া হয়েছে যা আপনার দেওয়া স্যাম্পল ছবির মতো দেখাবে।
4.  **চট্টগ্রাম ১৬:** এটি নিচের অংশে একটি সবুজ ক্যাপসুলের ভেতরে সেট করা হয়েছে।

এই কোডটি আপনার `app.py` ফাইলে সেভ করে রান করুন। এটি এখন সম্পূর্ণ প্রফেশনাল নির্বাচনী পোস্টার তৈরি করতে সক্ষম।

আমি কি এখন আপনার গিটহাবের জন্য একটি **`requirements.txt`** ফাইল তৈরি করে দেব যাতে সার্ভারে কোনো সমস্যা না হয়?
