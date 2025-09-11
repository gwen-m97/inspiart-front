import streamlit as st
import os
import requests

from PIL import Image
#from dotenv import load_dotenv
import os
import json
import base64

BASE_URL = "https://api-122517660338.europe-west1.run.app"

# Set page tab display
st.set_page_config(page_title="Inspiart")

#logo
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_path = os.path.abspath("sources/logo.png")
logo_base64 = get_base64_of_bin_file(logo_path)
# Centered logo and slogan together
st.markdown(
    f"""
    <div style='display: flex; flex-direction: column; align-items: center; margin-top: 20px;'>
        <img src="data:image/png;base64,{logo_base64}" width="200">
        <p style="text-align:center; font-size:20px; margin-top:10px;">
            Upload an image to know the style and find similar artworks.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Add background image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_path = os.path.abspath("sources/background1.jpg")
bg_base64 = get_base64_of_bin_file(bg_path)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

### file upload input
img = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

## uploading image, made it smaller
if img:
    st.markdown(
        """
        <style>
            [data-testid=stImage] img {
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 400px;
                height: auto;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.image(img, width=300, use_container_width=True)

 # Button to fetch artwork info
    if st.button("Get Artwork Info"):
        url = f"{BASE_URL}/samepainting_search"
        res = requests.post(url, files={'img': img.getvalue()})



        if res.ok:
            data = res.json()
            st.subheader("Artwork Information")
            st.write(f"**Artist:** {data.get('artist', 'Unknown')}")
            st.write(f"**Name:** {data.get('file_name', 'Unknown')}")


st.markdown("---")

# Button related artworks
relation_type = st.selectbox("Select relatedness type", ["Similar paintings from the same style", "Similar paintings from different styles", "Similar paintings on content only"])

#show related images button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    show_related = st.button("Show 5 Related Images")

##show_related = st.button("Show 5 Related Images")

if show_related:

     # End points

    if relation_type == "Similar paintings from the same style":
        url = f"{BASE_URL}/upload_same_style"
    elif relation_type == "Similar paintings from different styles":
        url = f"{BASE_URL}/upload_other_style"
    elif relation_type == "Similar paintings on content only":
        url = f"{BASE_URL}/upload_image"


    res = requests.post(url, files={'img': img.getvalue()})

# 5 images output
    if res.ok:
        related_data = res.json()
        st.subheader("Related Artworks")
        if relation_type != "Similar paintings on content only":

            st.markdown("---")
            st.markdown(f"**Predicted Style:** {related_data.get('style_predicted', 'Unknown')}")

        cols = st.columns(5)

        images = related_data.get("images", {})

    for i, (key, img_info) in enumerate(images.items()):
        with cols[i % 5]:
            st.markdown(
                f"""
                <div style='max-width:600px; margin:auto; text-align:center;'>
                    <img src="{img_info['img_url']}"
                         style='width:100%; height:auto; display:block; margin:auto; border-radius:8px;'/>
                    <p style="font-size:14px; margin-top:5px;">
                        <b>{img_info.get('artist', 'Unknown')}</b><br>
                        {img_info.get('style', 'Unknown')}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Footer ---
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.8);
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #333;
    }
    </style>
    <div class="footer">
        © 2025 Inspiart. Cedric Werkmann, Charles Lamb, Fabian, Giovanna Di Giacomo and Gwenaëlle Mustière

    </div>
    """,
    unsafe_allow_html=True
)
