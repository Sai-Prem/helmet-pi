from flask import Flask, Response
import cv2

app = Flask(__name__)
video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier()
face_cascade.load(cv2.samples.findFile("static/haarcascade_frontalface_alt.xml"))


def gen(video):
    while True:
        _, image = video.read()
        frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
            image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        _, jpeg = cv2.imencode(".jpg", image)
        frame = jpeg.tobytes()
        yield (b"--frame\r\n" + b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\\n")


@app.route("/")
def video_feed():
    return Response(gen(video), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2204, threaded=True)
