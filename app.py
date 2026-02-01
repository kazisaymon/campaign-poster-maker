import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import requests
import os

# --- Page Config ---
st.set_page_config(page_title="Paddy Sheaf Poster Maker", page_icon="🌾", layout="wide")

# --- Resource Handling (Bold Font & Logo) ---
@st.cache_resource
def get_assets():
    # Bold Font (Roboto Bold)
    font_url = "https://github.com/google/fonts/raw/main/ofl/robotocondensed/RobotoCondensed-Bold.ttf"
    font_path = "bold_font.ttf"
    if not os.path.exists(font_path):
        try:
            r = requests.get(font_url, timeout=10)
            with open(font_path, "wb") as f:
                f.write(r.content)
        except: pass
    
    # Paddy Sheaf Logo ( ধান ও চাকা)
    logo_url = "https://raw.githubusercontent.com/arshadsamrat/files/main/paddy_logo_fixed.png"
    logo_img = None
    try:
        logo_img = Image.open(io.BytesIO(requests.get(logo_url).content)).convert("RGBA")
    except:
        logo_img = None # লোগো না পেলে ইমোজি ব্যবহার হবে
        
    return font_path, logo_img

font_path, party_logo = get_assets()

# --- Helper function for dynamic font size ---
def get_custom_font(size):
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

# --- Sidebar Editor ---
st.sidebar.header("🛠️ Poster Editor")
uploaded_file = st.sidebar.file_uploader("📸 Upload Photo", type=["jpg", "png", "jpeg"])
user_name = st.sidebar.text_input("✍️ Candidate Name", "MISHKATUL ISLAM CHOWDHURY PAPPU")

st.sidebar.subheader("📏 Text Adjustments")
name_size = st.sidebar.slider("Name Font Size", 50, 120, 90)
name_y = st.sidebar.slider("Name Position (Up-Down)", 600, 1000, 780)
slogan_y = st.sidebar.slider("Slogan Position (Up-Down)", 600, 1000, 880)

# --- Poster Logic ---
if uploaded_file:
    canvas_size = 1080
    # লাল ফ্রেম
    poster = Image.new('RGBA', (canvas_size, canvas_size), (244, 42, 65, 255)) 
    draw = ImageDraw.Draw(poster)
    
    # গাঢ় সবুজ ব্যাকগ্রাউন্ড
    inner_bg = Image.new('RGBA', (canvas_size-60, canvas_size-60), (0, 106, 78, 255))
    poster.paste(inner_bg, (30, 30))

    # ১. গোল্ডেন হেডার (ধানের শীষ প্রতীক সহ)
    draw.rounded_rectangle([150, 15, 930, 95], radius=45, fill="#ffd700")
    draw.text((540, 55), "VOTE FOR PADDY SHEAF 🌾🌾", fill="black", font=get_custom_font(55), anchor="mm")

    # ২. ইউজার ফটো (বৃত্তাকার)
    user_img = Image.open(uploaded_file).convert("RGBA")
    img_size = (620, 620)
    user_img = ImageOps.fit(user_img, img_size, centering=(0.5, 0.5))
    mask = Image.new('L', img_size, 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.ellipse((0, 0, 620, 620), fill=255)
    
    # ফটোর চারপাশে সাদা মোটা বর্ডার
    draw.ellipse((220, 100, 860, 740), outline="white", width=18)
    poster.paste(user_img, (230, 110), mask)

    # ৩. ধানের শীষ লোগো সেট করা (টপ কর্নারে)
    if party_logo:
        l_res = party_logo.resize((190, 190))
        poster.paste(l_res, (60, 90), l_res)
        poster.paste(l_res, (830, 90), l_res)
    else:
        # লোগো না পেলে বড় ইমোজি বসবে
        draw.text((120, 180), "🌾", font=get_custom_font(120), fill="white", anchor="mm")
        draw.text((960, 180), "🌾", font=get_custom_font(120), fill="white", anchor="mm")

    # ৪. ক্যান্ডিডেট নেম (Bold & Large)
    draw.text((540, name_y), user_name.upper(), fill="#ffd700", font=get_custom_font(name_size), anchor="mm")

    # ৫. মেইন স্লোগান
    draw.text((540, slogan_y), "VOTE FOR PADDY SHEAF 🌾🌾", fill="white", font=get_custom_font(65), anchor="mm")

    # ৬. এরিয়া বক্স (Capsule Design)
    draw.rounded_rectangle([250, 980, 830, 1060], radius=40, fill="#004d2c")
    draw.text((540, 1020), "CHATTOGRAM 16 - BANSHKHALI", fill="white", font=get_custom_font(45), anchor="mm")

    # আউটপুট দেখানো
    st.image(poster, use_container_width=True)
    
    # ডাউনলোড বাটন
    buf = io.BytesIO()
    poster.save(buf, format="PNG")
    st.download_button("📥 Download Final Poster", buf.getvalue(), "pappu_poster_final.png")

else:
    st.warning("👈 Please upload your photo from the left sidebar!")

st.divider()
st.info("স্লাইডার ব্যবহার করে টেক্সট সাইজ এবং পজিশন (টেনে বসানোর মতো) ঠিক করে নিন।")
st.write("গুপ্তধন শুধু আপনার জন্য।")
