import sqlalchemy
from flask import Flask, redirect, url_for, render_template, request
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text

engine = create_engine('sqlite:///mydb.db')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    with engine.connect() as con:
        statement = text("""SELECT * FROM persons""")
        rs = con.execute(statement)
        t = []
        for n in rs:
            print(n)
            t.append(n)
            print(t)

    if request.method == 'POST':
        if request.form['submit_button'] == 'Submit':
            if request.form["submit_button"].firstname === "":
                print("Idiot")
                return render_template("index.html", content=t)
            if request.form["submit_button"].lastname === "":
                print("Idiot")
                return render_template("index.html", content=t)
            if request.form["submit_button"].email === "":
                print("Idiot")
                return render_template("index.html", content=t)
            if request.form["submit_button"].password === "":
                print("Idiot")
                return render_template("index.html", content=t)
            if request.form["submit_button"].ssn === "":
                print("Idiot")
                return render_template("index.html", content=t)
        else:
            print("Hiiiii")
            print(request.form['submit_button'], "HIIII")
    elif request.method == 'GET':
        # return render_template('index.html', form=form) 
        return render_template("index.html", content=t)
            
    return render_template("index.html", content=t)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2204, threaded=True)
