# Crowd Monitoring System

## 📌 Overview

The **Crowd Monitoring System** is a computer vision–based application designed to monitor and analyze crowd density in real time using a camera feed. The system helps in identifying overcrowded areas and can generate alerts when the crowd exceeds a predefined threshold. This project is useful for **public safety**, **event management**, **smart surveillance**, and **campus monitoring**.

---

## 🎯 Objectives

* Monitor live video feed from a camera
* Detect and estimate crowd density
* Visualize crowd data using graphs
* Trigger alerts when crowd exceeds safe limits
* Provide a simple web-based dashboard

---

## 🛠️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript
* Chart.js (for data visualization)

### Backend

* Python
* FastAPI / Flask
* OpenCV (for video processing)

### Other Tools

* Git & GitHub
* Webcam / CCTV feed

---

## ⚙️ Features

* 📹 Live camera feed
* 👥 Crowd count estimation
* 📊 Real-time graphical analysis
* 🚨 Alert system for high crowd density
* 🌙 Optional Dark Mode UI

---

## 📂 Project Structure

```
Crowd-Monitoring-System/
│── static/
│   ├── index.html
│── main.py
│── requirements.txt
│── faces
     │── 1_shubhi.jpg
│── face_trainer.yml
│── train_face.py
│── yolo8n.pt
│── README.md

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/crowd-monitoring-system.git
cd crowd-monitoring-system
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python main.py
```

### 5️⃣ Open in Browser

```
http://127.0.0.1:8000
```

(or the port shown in the terminal)

---

## 📊 Output

* Live video stream from the camera
* Crowd count displayed dynamically
* Graph showing crowd variations over time
* Alert message when crowd limit is exceeded

## 🔮 Future Enhancements

* AI-based person detection using YOLO
* Heatmap visualization
* Multiple camera support
* SMS / Email alert system
* Cloud deployment

## 🎓 Use Cases

* Public gatherings & events
* Railway stations & airports
* Shopping malls
* College campuses
* Smart city surveillance

---

## 🤝 Contribution

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

---

## 📜 License

This project is for **educational purposes**.

## 👤 Author

Shubhi Singh
B.Tech Student | Crowd Monitoring System Project

⭐ If you like this project, don’t forget to **star the repository**!
