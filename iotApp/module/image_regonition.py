import cv2
import numpy as np
import face_recognition

def detect_face(uploaded_file):
    image_np = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    if image_np is None:
        print("Error: Unable to read the image.")
        return False

    # Convert BGR image to RGB (face_recognition uses RGB)
    rgb_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

    # Use face_recognition to find faces in the image
    face_locations = face_recognition.face_locations(rgb_image)

    # Draw bounding boxes on faces
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(image_np, (left, top), (right, bottom), (0, 255, 0), 2)

    return len(face_locations) > 0