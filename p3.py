#importing modules
import streamlit as st
from main import ComputerVision
from PIL import Image
import io

model = ComputerVision()

#setting up title and instructions
st.title("Object Detection For 1P13")
st.header("How it works:")
st.write("Simply enter a photo, and we will identify the objects for you")

#taking image from client's phone as input
file = st.file_uploader("Enter a photo here", type = ["jpg", "png", "jpeg"]) #Stored as BYTEIO, need it as an image

#processing photo
if file is not None:
    #creating image object
    image = Image.open(file)
    processed_image = model.get_objects_jpeg(image) #needed as BYTEIO, not as an image
    image_byte_array = io.BYTESIO() #created empty array of bytes
    image_byte_array = image_byte_array.getvalue()
    st.image(image_byte_array)
    
    
