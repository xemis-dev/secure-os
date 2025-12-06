from flask import Flask, render_template, Response, jsonify, request, redirect, url_for, session
import cv2
import time
import os
import psutil
from datetime import datetime
from ultralytics import YOLO
import threading
import pygame

app = Flask(__name__)
app.secret_key = 'SUPER_SECRET_KEY_SECURE_OS'

USERS = {"begzat": "kidirbaev"}
START_TIME = datetime.now()
REC_FOLDER = 'recordings'
if not os.path.exists(REC_FOLDER): os.makedirs(REC_FOLDER)

pygame.mixer.init()
ALARM_FILE = "siren.mp3"
model = YOLO('yolov8n.pt')

camera_settings = {
    "motion_active": False,
    "ai_active": True,
    "recording": False,
    "alarm_active": False,
    "sensitivity": 40,
    "brightness": 0,
    "contrast": 1.0,
    "fps": 15
}

global_writer = None
last_motion_time = 0
alarm_playing = False

def play_alarm():
    global alarm_playing
    if not alarm_playing and camera_settings["alarm_active"]:
        alarm_playing = True
        try:
            if os.path.exists(ALARM_FILE):
                pygame.mixer.music.load(ALARM_FILE)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(1)
        except: pass
        alarm_playing = False

def get_stats():
    disk = psutil.disk_usage('/')
    uptime = str(datetime.now() - START_TIME).split('.')[0]
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk_text": f"{round(disk.free / (1024**3), 1)}GB FREE",
        "uptime": uptime
    }

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        global global_writer, last_motion_time
        success, frame = self.video.read()
        if not success: return None
        
        frame = cv2.resize(frame, (640, 480))
        if camera_settings["brightness"] != 0 or camera_settings["contrast"] != 1.0:
            frame = cv2.convertScaleAbs(frame, alpha=camera_settings["contrast"], beta=camera_settings["brightness"])
        
        original = frame.copy()
        person_detected = False

        if camera_settings["ai_active"]:
            results = model(frame, verbose=False, conf=0.5)
            for r in results:
                for box in r.boxes:
                    if model.names[int(box.cls[0])] == 'person':
                        person_detected = True
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(frame, "INTRUDER DETECTED", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

        if person_detected:
            last_motion_time = time.time()
            if camera_settings["alarm_active"] and not alarm_playing:
                threading.Thread(target=play_alarm).start()
            if not camera_settings["recording"]:
                camera_settings["recording"] = True
                fn = os.path.join(REC_FOLDER, f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi")
                global_writer = cv2.VideoWriter(fn, cv2.VideoWriter_fourcc(*'XVID'), 10.0, (640, 480))

        if camera_settings["recording"]:
            if time.time() - last_motion_time > 5:
                camera_settings["recording"] = False
                if global_writer: global_writer.release()
            elif global_writer:
                global_writer.write(original)
                cv2.circle(frame, (30, 30), 5, (0, 0, 255), -1)

        cv2.putText(frame, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        ret, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        return jpeg.tobytes()

def gen(camera):
    while True:
        st = time.time()
        frame = camera.get_frame()
        if frame: yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        wait = (1.0 / camera_settings["fps"]) - (time.time() - st)
        if wait > 0: time.sleep(wait)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="ACCESS DENIED")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not session.get('logged_in'): return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    if not session.get('logged_in'): return "Access Denied"
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/data')
def api_data():
    if not session.get('logged_in'): return jsonify({})
    s = get_stats()
    s.update(camera_settings)
    return jsonify(s)

@app.route('/api/update', methods=['POST'])
def api_update():
    if not session.get('logged_in'): return jsonify({"status":"error"})
    data = request.json
    for k, v in data.items():
        if k in camera_settings:
            if k == 'contrast': camera_settings[k] = float(v)
            elif k in ['brightness', 'sensitivity', 'fps']: camera_settings[k] = int(v)
            else: camera_settings[k] = v
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)