from flask import Flask, render_template, request
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:SQL123@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://uqkqhuhzugjowm:a9478ca895645f3edf940c8a8a48943f7532f336232d735e0acfe6b16e952748@ec2-34-193-232-231.compute-1.amazonaws.com:5432/d129j98o8qfkks?sslmode=require'
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    ht=db.Column(db.Integer)

    def __init__(self, email_, ht):
        self.email_=email_
        self.ht=ht


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height_name"]
        print(email, height)
        if db.session.query(Data).filter(Data.email_ == email).count()== 0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.ht)).scalar()
            average_height=round(average_height, 1)
            count = db.session.query(Data.ht).count()
            send_email(email, height, average_height, count)
            print(average_height)
            return render_template("success.html")
    return render_template('index.html', text="Same email entry already exists!")

       

if __name__ == '__main__':
    app.debug=True
    app.run()