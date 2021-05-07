from flask import Flask,request,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

def encrypt(text):
    output = ""
    s = 4
    for i in range(len(text)):
        stng = text[i]
        if (stng.isupper()):
            output += chr((ord(stng) + s - 65) % 26 + 65)
        else:
            output += chr((ord(stng) + s - 97) % 26 + 97)
    return output

class cipher(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.String(300),nullable=False)
    encod = db.Column(db.String)
    time = db.Column(db.DateTime)
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/',methods=['POST','GET'])
def Home():
    if request.method=='POST':
        text = request.form['text']
        encod = encrypt(text)
        data1 = cipher(text=text,encod=encod)
        try:
            db.session.add(data1)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem'
    else:
        task = cipher.query.order_by(cipher.id).all()
        return render_template('base.html',task=task)

if __name__ == '__main__':
    app.run(port=80, debug=True)
