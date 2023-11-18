


import time

from flask import Flask, Response
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2

app = Flask(__name__)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60
raw_capture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

face_cascade = cv2.CascadeClassifier()
face_cascade.load(cv2.samples.findFile("static/haarcascade_frontalface_alt.xml"))

def gen(camera):
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array

        '''frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)
        faces = face_cascade.detectMultiScale(frame_gray)
        for (x, y, w, h) in faces:
            center = (x + w//2, y + h//2)
            cv2.putText(
                image,
                f"X: {center[0]} Y: {center[1]}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                3
            )


            image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)'''
        

        _, jpeg = cv2.imencode(".jpg", image)
        frame = jpeg.tobytes()
        raw_capture.truncate(0)
        yield (b"--frame\r\n" + b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\\n")


@app.route("/")
def video_feed():
    return Response(gen(camera), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2204, threaded=True)
