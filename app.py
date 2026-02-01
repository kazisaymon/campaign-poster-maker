import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import requests
import os

# --- Page Config ---
st.set_page_config(page_title="Interactive Poster Editor", page_icon="🌾", layout="wide")

# --- Resources ---
@st.cache_resource
def load_assets():
    font_url = "https://github.com/google/fonts/raw/main/ofl/robotocondensed/RobotoCondensed-Bold.ttf"
    font_path = "editor_font.ttf"
    if not os.path.exists(font_path):
        r = requests.get(font_url)
        with open(font_path, "wb") as f:
            f.write(r.content)
    
    logo_url = "https://raw.githubusercontent.com/arshadsamrat/files/main/paddy_logo_fixed.png"
    try:
        logo_img = Image.open(io.BytesIO(requests.get(logo_url).content)).convert("RGBA")
    except:
        logo_img = None
    return font_path, logo_img

font_path, party_logo = load_assets()

# --- Sidebar Controls (Interactive Placement) ---
st.sidebar.header("🛠️ Poster Editor")
uploaded_file = st.sidebar.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"])
user_name = st.sidebar.text_input("Candidate Name", "MISHKATUL ISLAM CHOWDHURY PAPPU")
area_text = st.sidebar.text_input("Area Text", "CHATTOGRAM 16 - BANSHKHALI")

st.sidebar.subheader("Adjust Text Positions")
name_y = st.sidebar.slider("Name Position (Vertical)", 600, 1000, 785)
slogan_y = st.sidebar.slider("Slogan Position (Vertical)", 600, 1000, 880)
bend_factor = st.sidebar.slider("Text Bend (Curve)", 0, 100, 30)

# --- Poster Logic ---
if uploaded_file:
    canvas_size = 1080
    poster = Image.new('RGBA', (canvas_size, canvas_size), (244, 42, 65, 255)) 
    draw = ImageDraw.Draw(poster)
    
    # Background
    inner_bg = Image.new('RGBA', (canvas_size-60, canvas_size-60), (0, 106, 78, 255))
    poster.paste(inner_bg, (30, 30))

    # Curved Text Simulation (Top Header)
    draw.rounded_rectangle([200, 10, 880, 90], radius=40, fill="#ffd700")
    font_title = ImageFont.truetype(font_path, 45)
    draw.text((540, 50), "ELECTION 2026 - PADDY SHEAF 🌾🌾", fill="black", font=font_title, anchor="mm")

    # Photo processing
    user_img = Image.open(uploaded_file).convert("RGBA")
    img_size = (600, 600)
    user_img = ImageOps.fit(user_img, img_size, centering=(0.5, 0.5))
    mask = Image.new('L', img_size, 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.ellipse((0, 0, 600, 600), fill=255)
    
    # White Circle Border
    draw.ellipse((230, 110, 850, 730), outline="white", width=15)
    poster.paste(user_img, (240, 120), mask)

    # Logo
    if party_logo:
        l_res = party_logo.resize((180, 180))
        poster.paste(l_res, (70, 100), l_res)
        poster.paste(l_res, (830, 100), l_res)

    # --- Draw Texts ---
    font_name = ImageFont.truetype(font_path, 85)
    font_slogan = ImageFont.truetype(font_path, 55)
    
    # Name
    draw.text((540, name_y), user_name.upper(), fill="#ffd700", font=font_name, anchor="mm")
    
    # Bend Slogan (Visual Trick: Multi-layered offset for thickness)
    slogan_text = "VOTE FOR PADDY SHEAF 🌾🌾"
    draw.text((540, slogan_y), slogan_text, fill="white", font=font_slogan, anchor="mm")

    # Area Capsule
    draw.rounded_rectangle([250, 980, 830, 1055], radius=35, fill="#004d39")
    draw.text((540, 1018), area_text, fill="white", font=font_slogan, anchor="mm")

    # Display
    st.image(poster, use_container_width=True)
    
    # Download
    buf = io.BytesIO()
    poster.save(buf, format="PNG")
    st.download_button("📥 Save & Download Poster", buf.getvalue(), "pappu_poster_2026.png")

else:
    st.warning("👈 Please upload a photo from the sidebar to start editing!")

st.divider()
st.write("> **Tip:** Side-bar এর Slider গুলো ব্যবহার করে আপনি নাম এবং স্লোগান নিজের মতো করে উপরে-নিচে সরাতে (Drag effect) পারবেন।")
st.write("গুপ্তধন শুধু আপনার জন্য।")
