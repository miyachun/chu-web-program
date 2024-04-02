from flask import Flask, redirect, url_for, render_template, request, session
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"
boostrap = Bootstrap(app=app)
img=''
upload_folder = os.path.join('static', 'photo')
app.config['UPLOAD'] = upload_folder
@app.route('/')  
def index():  
    return render_template('index.html')    
  
@app.route("/write", methods=["POST","GET"])
def write():
    global img
    if request.method == "POST":
        paper = request.form["nm"]
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)                      
        session["paper"] = paper
        session["photo"] = filename
        return redirect(url_for("paper"))
    else:
        return render_template("write.html")  


@app.route("/paper")
def paper():
    if "paper" or "photo" in session:
        paper = session["paper"]
        photo = session["photo"]
        img = os.path.join(app.config['UPLOAD'], photo)        
        return render_template("paper.html",paper=paper, photo=img)
    else:
        return redirect(url_for("write"))



if __name__ == '__main__':
    app.run()