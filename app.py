import streamlit as st
import os
import requests

from PIL import Image
#from dotenv import load_dotenv
import os
import json
import base64

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

#image buffer

st.markdown("---")

### Create a native Streamlit file upload input
img = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

## uploading image
if img:
    st.image(img, caption="Here's the image you uploaded ☝️", use_container_width=True)

 # Button to fetch artwork info
    if st.button("Get Artwork Info"):
        res = requests.post(url, files={'img': img.getvalue()})
        res_dict = json.loads(res.json())


        if res.ok:
            data = res.json()
            st.subheader("Artwork Information")
            st.write(f"**Author:** {data.get('author', 'Unknown')}")
            st.write(f"**Year:** {data.get('year', 'Unknown')}")
            st.write(f"**Style:** {data.get('style', 'Unknown')}")
        else:
            st.error("I'm sorry, the art work information is not on our database, please try another art work.")
st.markdown("---")

# Button to find similar artworks
relation_type = st.selectbox("Select relatedness type", ["Style", "Content", "Content but another style"])
show_related = st.button("Show 5 Related Images")

if show_related:
     # End points

    if relation_type == "Style":
        pass
    elif relation_type == "Content":
        url = "https://taxifare-174146437405.europe-west1.run.app/upload_image"

    elif relation_type == "Content but another style":
        pass
      
    payload = {"relation_type": relation_type.lower()}
    res = requests.post(url, files={'img': img.getvalue()}, data=payload)
    res_dict = json.loads(res.json())

# 5 images output
    if res.ok:

        related_data = res.json()
        st.subheader("Related Artworks")
        cols = st.columns(5)

        for i, sim_img in enumerate(res_dict.values()):
            # sim_img = Image.open(image_paths[indices[0][i]])
##            sim_img = res_dict.values()[i]  # placeholder
            cols[i].image(sim_img, use_container_width=True)
else:
    st.error("I'm sorry, please try again.")
