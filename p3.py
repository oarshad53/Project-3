#This just takes an image and spits it back out, still needs to run detection

import streamlit as st
from PIL import Image

st.title("Object Detection For 1P13")

st.header("How it works:")
st.write("Simply enter a photo, and we will identify it for you")

file = st.file_uploader("Enter a photo here", type = ["jpg", "png", "jpeg"])

if file is not None:
    image = Image.open(file)

    st.image(image)
