import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import base64

# --- ১. কোডের ভেতরেই ফন্ট ও লোগো ডাটা (Base64) ---
# এটি ইন্টারনেটের ওপর নির্ভরতা কমাবে
st.set_page_config(page_title="Offline Poster Maker", page_icon="🌾", layout="wide")

# --- ২. সাইডবার এডিটর ---
st.sidebar.header("🛠️ Poster Editor")
uploaded_file = st.sidebar.file_uploader("📸 Upload Photo", type=["jpg", "png", "jpeg"])
user_name = st.sidebar.text_input("✍️ Candidate Name", "MISHKATUL ISLAM PAPPU")

st.sidebar.subheader("📏 Text & Size")
name_size = st.sidebar.slider("Name Size", 50, 150, 100) # সাইজ ৫০+ বোল্ড
name_y = st.sidebar.slider("Move Name (Up-Down)", 600, 1000, 780)
slogan_y = st.sidebar.slider("Move Slogan (Up-Down)", 600, 1000, 880)

# --- ৩. মেইন ফাংশন ---
def create_poster(img_file, name, n_size, n_y, s_y):
    canvas_size = 1080
    # রেড বর্ডার ফ্রেম
    poster = Image.new('RGBA', (canvas_size, canvas_size), (244, 42, 65, 255)) 
    draw = ImageDraw.Draw(poster)
    
    # গ্রিন ব্যাকগ্রাউন্ড
    inner_bg = Image.new('RGBA', (canvas_size-60, canvas_size-60), (0, 106, 78, 255))
    poster.paste(inner_bg, (30, 30))

    # ৩.১. ফন্ট হ্যান্ডলিং (লিঙ্ক ছাড়া ডিফল্ট বোল্ড করার চেষ্টা)
    try:
        # যদি আপনার সিস্টেমে কোনো ফন্ট না থাকে তবে এটি ডিফল্ট ব্যবহার করবে
        font_bold = ImageFont.load_default()
        # বড় সাইজ করার জন্য ট্রাই (যদি লিনাক্সে থাকে)
        font_name = ImageFont.truetype("DejaVuSans-Bold.ttf", n_size)
        font_slogan = ImageFont.truetype("DejaVuSans-Bold.ttf", 65)
    except:
        font_name = font_bold
        font_slogan = font_bold

    # ৩.২. গোল্ডেন হেডার ক্যাপসুল
    draw.rounded_rectangle([150, 20, 930, 100], radius=40, fill="#ffd700")
    draw.text((540, 60), "VOTE FOR PADDY SHEAF 🌾", fill="black", font=font_slogan, anchor="mm")

    # ৩.৩. ইউজার ফটো প্রসেসিং
    user_img = Image.open(img_file).convert("RGBA")
    user_img = ImageOps.fit(user_img, (600, 600), centering=(0.5, 0.5))
    
    mask = Image.new('L', (600, 600), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.ellipse((0, 0, 600, 600), fill=255)
    
    # ফটোর বর্ডার
    draw.ellipse((230, 100, 850, 720), outline="white", width=20)
    poster.paste(user_img, (240, 110), mask)

    # ৩.৪. ধানের শীষ প্রতীক (ইমোজি স্টাইল যা সবখানে সাপোর্ট করে)
    # যেহেতু লিঙ্ক ব্যবহার করা যাবে না, আমরা বড় ইমোজিকে লোগো হিসেবে ব্যবহার করছি
    draw.text((120, 150), "🌾", fill="#ffd700", font=font_name, anchor="mm")
    draw.text((960, 150), "🌾", fill="#ffd700", font=font_name, anchor="mm")

    # ৩.৫. টেক্সট বসানো (Bold & Large)
    # নাম
    draw.text((540, n_y), name.upper(), fill="#ffd700", font=font_name, anchor="mm")
    # স্লোগান
    draw.text((540, s_y), "VOTE FOR PADDY SHEAF 🌾🌾", fill="white", font=font_slogan, anchor="mm")

    # ৩.৬. নিচের এলাকা বক্স
    draw.rounded_rectangle([250, 980, 830, 1060], radius=40, fill="#004d2c")
    draw.text((540, 1020), "CHATTOGRAM 16 - BANSHKHALI", fill="white", font=font_slogan, anchor="mm")

    return poster

# --- ৪. ডিসপ্লে ---
if uploaded_file:
    final_poster = create_poster(uploaded_file, user_name, name_size, name_y, slogan_y)
    st.image(final_poster, use_container_width=True)
    
    # ডাউনলোড বাটন
    buf = io.BytesIO()
    final_poster.save(buf, format="PNG")
    st.download_button("📥 Download Poster", buf.getvalue(), "poster.png")
else:
    st.info("👈 বাম পাশের মেনু থেকে আপনার ছবি আপলোড করুন।")

st.divider()
st.write("গুপ্তধন শুধু আপনার জন্য।")
