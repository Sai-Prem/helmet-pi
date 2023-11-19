import time

from flask import Flask, Response, request, render_template, redirect
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import RPi.GPIO as IO

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text


Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    email = Column("email", String)
    password = Column("password", String)

    def __init__(self, ssn, firstname, lastname, email, password):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        
    def __repr__(self):
        return f"({self.ssn} {self.firstname} {self.lastname} {self.email}, {self.password})"


IO.setwarnings(False)
IO.setmode(IO.BCM)

app = Flask(__name__)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60
raw_capture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

face_cascade = cv2.CascadeClassifier()
face_cascade.load(cv2.samples.findFile("static/haarcascade_frontalface_alt.xml"))


def ir_sensor(IO, pin) -> bool:
    return IO.input(pin)

def gen(camera):
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        # sensor_output = ir_sensor(IO=IO, pin=14)

        # frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # frame_gray = cv2.equalizeHist(frame_gray)
        # faces = face_cascade.detectMultiScale(frame_gray)
        # for (x, y, w, h) in faces:
        #     center = (x + w//2, y + h//2)
        #     cv2.putText(
        #         image, 
        #         f"X: {center[0]} Y: {center[1]}",
        #         (50, 50),
        #         cv2.FONT_HERSHEY_SIMPLEX,
        #         1,
        #         (255, 0, 0),
        #         3
        #     )
        #     image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        _, jpeg = cv2.imencode(".jpg", image)
        frame = jpeg.tobytes()
        raw_capture.truncate(0)
        yield (b"--frame\r\n" + b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\\n")

@app.route("/signup", methods=["GET", "POST"])
def home():
    # with engine.connect() as con:
    #     statement = text("""SELECT * FROM persons""")
    #     rs = con.execute(statement)
    #     t = []
    #     for n in rs:
    #         print(n)
    #         t.append(n)
    #         print(t)

    if request.method == 'POST':
        if request.form['submit_button'] == 'Submit':
            if request.form.get("firstname") == "":
                print("Idiot")
                return render_template("index.html")
            elif request.form.get("lastname") == "":
                print("Idiot")
                return render_template("index.html")
            elif request.form.get("email") == "":
                print("Idiot")
                return render_template("index.html")
            elif request.form.get("password") == "":
                print("Idiot")
                return render_template("index.html")
            elif request.form.get("ssn") == "":
                print("Idiot")
                return render_template("index.html")
            
            else:
                engine = create_engine("sqlite:///mydb.db", echo=True)
                Base.metadata.create_all(bind=engine)

                Session = sessionmaker(bind=engine)
                session = Session()


                firstname = request.form.get("firstname")
                lastname = request.form.get("lastname")
                email = request.form.get("email")
                password = request.form.get("password")
                ssn = request.form.get("ssn") 

                
                p1 = Person(ssn, firstname, lastname, email, password)
                session.add(p1)
                session.commit()
            
                with engine.connect() as con:
                    statement = text("""SELECT * FROM persons""")
                    rs = con.execute(statement)
                    t = []
                    for n in rs:
                        t.append(n)
                    print(t)
                
                return redirect('/camera')
        else:
            print("Hiiiii")
            print(request.form['submit_button'], "HIIII")
    elif request.method == 'GET':
        # return render_template('index.html', form=form) 
        print("all well")
        return render_template("index.html")
            
    return render_template("index.html")

@app.route("/", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Submit':
            if request.form.get("firstname") == "":
                print("Idiot")
                return render_template("index.html")
            elif request.form.get("lastname") == "":
                print("Idiot")
                return render_template("index.html")
            elif request.form.get("email") == "":
                print("Idiot")
                return render_template("index.html")
            elif request.form.get("password") == "":
                print("Idiot")
                return render_template("index.html")
            elif request.form.get("ssn") == "":
                print("Idiot")
                return render_template("index.html")
            else:
                engine = create_engine("sqlite:///mydb.db", echo=True)
                Base.metadata.create_all(bind=engine)
                Session = sessionmaker(bind=engine)
                session = Session()
                firstname = request.form.get("firstname")
                lastname = request.form.get("lastname")
                email = request.form.get("email")
                password = request.form.get("password")
                ssn = request.form.get("ssn")
                print(ssn)

                check = session.query(Person).filter(Person.ssn == ssn).all()
                if not check:
                    print("bake!")
                    return render_template("index.html")
                else:
                    return redirect('/camera')
            
    return render_template("index.html")

@app.route("/camera")
def video_feed():
    return Response(gen(camera), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2204, threaded=True) 