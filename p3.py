#next step, testing


#importing modules
import streamlit as st
from main import ComputerVision
from PIL import Image
import io

model = ComputerVision()

#Color is set to neon green, which the client is able to see
#setting up title and instructions, embedding html to meet client's vison needs
st.write("<h1 style ='color: #39FF14;'>Object Detection For 1P13</h1>", unsafe_allow_html = True)
st.write("<h2 style ='color: #39FF14;'>How it works:</h2>", unsafe_allow_html = True)
st.write("<h4 style = 'color: #39FF14;'>Simply enter a photo, and we will identify it for you</h4>", unsafe_allow_html = True)


#taking image from client's phone as input
file = st.file_uploader("Enter a photo here", type = ["jpg", "png", "jpeg"]) #Stored as BYTEIO, need it as an image

#processing photo
if file is not None:
    image = Image.open(file) #creates image object
    _, processed_image = model.get_objects_jpeg(image)#this is stored as an image, need it as bytes
    processed_image_bytes = io.BytesIO(processed_image) #Converted back to bytes, which can now be displayed
    st.image(processed_image_bytes) 
    

    
    
