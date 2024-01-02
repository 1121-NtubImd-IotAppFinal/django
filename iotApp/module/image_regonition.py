import os
import cv2
import numpy as np

def detect_face(uploaded_file):
    image_np = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    if image_np is None:
        print("Error: Unable to read the image.")
        return False
    current_directory = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_directory, 'ai_model/haarcascade_frontalface_default.xml')

    face_detector = cv2.CascadeClassifier(model_path)
    faces = face_detector.detectMultiScale(image_np)

    for (x, y, w, h) in faces:
        cv2.rectangle(image_np, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return len(faces) > 0

