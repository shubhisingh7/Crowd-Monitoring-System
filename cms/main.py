import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import cv2
from ultralytics import YOLO
import winsound


app = FastAPI()

# Load YOLO model
model = YOLO("yolov8n.pt")
# Face recognition setup
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("face_trainer.yml")

names = {
    1: "Shubhi"
}


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# Crowd history for plotting
crowd_history = []
MAX_POINTS = 30   # last 30 seconds

# Open webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

crowd_count = 0
CROWD_LIMIT = 1  # 👈 change this number as needed
alert_active = False
alarm_playing = False


def generate_frames():
    global crowd_count, alert_active, alarm_playing

    while True:
        success, frame = cap.read()
        if not success:
            break

        # ---------------- YOLO PERSON DETECTION ----------------
        results = model(frame, stream=True)
        count = 0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if cls == 0:  # person
                    count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        crowd_count = count

        # ---------------- FACE RECOGNITION ----------------
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id_, confidence = face_recognizer.predict(gray[y:y+h, x:x+w])

            if confidence < 80:
                name = names.get(id_, "Unknown")
            else:
                name = "Unknown"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(
                frame,
                name,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

        # ---------------- ALERT LOGIC ----------------
        if crowd_count > CROWD_LIMIT:
            alert_active = True
        else:
            alert_active = False
            alarm_playing = False

        # ---------------- SOUND ----------------
        if alert_active and not alarm_playing:
            winsound.Beep(1000, 500)
            alarm_playing = True

        # ---------------- TEXT OVERLAY ----------------
        if alert_active:
            cv2.putText(
                frame,
                "ALERT: CROWD LIMIT EXCEEDED!",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

        cv2.putText(
            frame,
            f"Crowd Count: {crowd_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 255),
            3
        )

        # ---------------- STREAM FRAME ----------------
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )



@app.get("/")
def dashboard():
    with open("static/index.html") as f:
        return HTMLResponse(f.read())


@app.get("/video-feed")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/count")
def count():
    return {"crowd": crowd_count}

@app.get("/alert")
def alert_status():
    return {
        "alert": alert_active,
        "limit": CROWD_LIMIT,
        "current": crowd_count
    }

@app.get("/crowd-data")
def crowd_data():
    global crowd_history

    crowd_history.append(crowd_count)

    if len(crowd_history) > MAX_POINTS:
        crowd_history.pop(0)

    avg_crowd = sum(crowd_history) / len(crowd_history)
    peak_crowd = max(crowd_history)

    return {
        "history": crowd_history,
        "current": crowd_count,
        "average": round(avg_crowd, 2),
        "peak": peak_crowd,
        "limit": CROWD_LIMIT,
        "alert": alert_active
    }
