import streamlit as st
import os
import requests

from PIL import Image
#from dotenv import load_dotenv
import os
import json

# Set page tab display
st.set_page_config(
   page_title="Simple Image Uploader",
   page_icon= '🖼️',
   layout="wide",
   initial_sidebar_state="expanded",
)

# Example local Docker container URL
# url = 'http://api:8000'
# Example localhost development URL
url = 'http://localhost:8000/upload_image'
#load_dotenv()
#url = "127.0.0.1:8000"

#"SERVICE_URL = os.environ.get("SERVICE_URL")

#url = "https://taxifare-174146437405.europe-west1.run.app/upload_image"


# App title and description
st.header('Inspiart 📸')
st.markdown('''
            > Test website for Inspiart.

            ''')

st.markdown("---")

### Create a native Streamlit file upload input
st.markdown("### INSPIART - Let's find you some paintings! 👇")
img_file_buffer = st.file_uploader('Upload an image')

if img_file_buffer is not None:

    col1, col2 = st.columns(2)

    with col1:
    ### Display the image user uploaded
        st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded ☝️")




    with col2:
        with st.spinner("Wait for it..."):
      ### Get bytes from the file buffer
      #img_bytes = img_file_buffer.getvalue()

      ### Make request to  API (stream=True to stream response as bytes)
            res = requests.post(url, files={'img': img_file_buffer.getvalue()})
            res_dict = json.loads(res.json())

            if res.status_code == 200:
        ### Display the image returned by the API
                for image in res_dict:
                    st.image(res_dict[image], caption="Image returned from API ☝️")

            else:
                st.markdown(f"**Oops**, something went wrong 😓 Please try again.{res.status_code}, {res.content}, {res}")
                print(res.status_code, res.content)
