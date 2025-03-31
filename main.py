from ultralytics import YOLO
import requests
import cv2
import numpy as np
from paddleocr import PaddleOCR

class ComputerVision:

    def __init__(self, model="yolo11n.pt"):
        self.model = YOLO(model) # yolo model, defaults to yolo11n.pt, which is the one being used in this project

    def get_image_from_url(self, url):

        try:
            response = requests.get(url)
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8) # numpy image byte array
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            return image

        except Exception as e:
            print(e.args[0])
            return None 
        
    def get_text(self, url): 

        ocr = PaddleOCR(use_angle_cls=True, lang="en") 

        image = self.get_image_from_url(url)  

        result = ocr.ocr(image, cls=True)
        
        text_clean = [] 
        if result != [None]:
            for line in result:
                for word in line:
                    text_clean.append(word[1][0])  

        return " ".join(text_clean) if text_clean else "No recognised text."
            

    def get_objects(self, url, showimage=False) -> list:
        
        results = self.model.predict(source=self.get_image_from_url(url), conf=0.60, save=False, stream=False)

        annotated_image = results[0].plot()

        if showimage == True:
            cv2.imshow("Detection Image", annotated_image)
            cv2.waitKey(0) # key press to close image
            cv2.destroyAllWindows()

        object_arr = []

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0]) 
            class_id = int(box.cls[0]) 
            confidence = box.conf[0].item() 

            object_arr.append(results[0].names[class_id])

        return object_arr, annotated_image

if __name__ == "__main__":
    print("This class is meant to be imported.")
