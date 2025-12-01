from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import cv2
from ultralytics import YOLO
import threading

app = FastAPI()

# Load YOLOv8
model = YOLO("yolov8n.pt")

# Attach static HTML folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Shared variable
crowd_count = 0

# Video capture
cap = cv2.VideoCapture(0)

def generate_frames():
    global crowd_count

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, stream=True)
        count = 0

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                if cls == 0:
                    count += 1
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, f"Person {conf:.2f}",
                                (x1, y1 - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                (0,255,0), 2)

        crowd_count = count

        cv2.putText(frame, f"Crowd Count: {crowd_count}",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0,0,255), 3)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get("/")
def dashboard():
    """Serve Dashboard HTML"""
    with open("static/index.html") as f:
        return HTMLResponse(f.read())


@app.get("/video-feed")
def video_feed():
    """Live camera stream"""
    return StreamingResponse(generate_frames(),
                             media_type="multipart/x-mixed-replace; boundary=frame")


@app.get("/crowd-count")
def get_crowd_count():
    """Return live crowd count"""
    return {"count": crowd_count}
