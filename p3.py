#importing modules
import streamlit as st
from main import ComputerVision

#setting up title and instructions
st.title("Object Detection For 1P13")
st.header("How it works:")
st.write("Simply enter a photo, and we will identify the objects for you")

#taking image from client's phone as input
image = st.file_uploader("Enter a photo here", type = ["jpg", "png", "jpeg"])

#processing photo

detector = ComputerVision()

if image is not None:
    processed_image = detector.get_objects_jpeg(image)
    st.image(processed_image)
