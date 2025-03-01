from ultralytics import YOLO
import requests
import cv2
import numpy as np

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
            return None # should stop execution if we get an exception?

    def get_objects(self, url, showimage=True) -> list:  #should return a list
        
        results = self.model.predict(source=self.get_image_from_url(url), conf=0.25, save=False, stream=False) # adjut conf value

        annotated_image = results[0].plot()

        if showimage == True:
            cv2.imshow("Detection Image", annotated_image)
            cv2.waitKey(0) # wait until key press to close iagmae
            cv2.destroyAllWindows()

        object_arr = [] #make an array to contain detected objects for testing purposes

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0]) # mapping x1,y1 x2,y2 coord pairs of box for each object
            class_id = int(box.cls[0]) # get the class_id so we can say what the object is from an already defined list of detectable objects
            confidence = box.conf[0].item() # confidence score of each box. .item() is used to PyTorch tensor value to a normal int

        # now we make a dictionary to readily have key data points available to us
            detection = {
                "class": results[0].names[class_id],
                "bbox": (x1, x2, y1, y2),  # tuple
                "confidence": confidence
            }

            #print(f"Detected: {results[0].names[class_id]}, BBox: ({x1}, {y1}, {x2}, {y2})")
            object_arr.append(results[0].names[class_id])

        return object_arr, annotated_image

if __name__ == "__main__":
    print("This class is meant to be imported.")

