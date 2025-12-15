import cv2
import os
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

faces = []
labels = []

for file in os.listdir("faces"):
    if file.endswith(".jpg"):
        path = os.path.join("faces", file)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        label = int(file.split("_")[0])

        detected_faces = face_cascade.detectMultiScale(img)
        for (x, y, w, h) in detected_faces:
            faces.append(img[y:y+h, x:x+w])
            labels.append(label)

recognizer.train(faces, np.array(labels))
recognizer.save("face_trainer.yml")

print("Face training completed")
