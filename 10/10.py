from flask import Flask, redirect, url_for, render_template, request, session
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"
boostrap = Bootstrap(app=app)

@app.route('/')  
def index():  
    return render_template('index.html')    
  
@app.route("/write", methods=["POST","GET"])
def write():
    if request.method == "POST":
        paper = request.form["nm"]
        session["paper"] = paper
        return redirect(url_for("paper"))
    else:
        return render_template("write.html")  


@app.route("/paper")
def paper():
    if "paper" in session:
        paper = session["paper"]
        return render_template("paper.html",paper=paper)
    else:
        return redirect(url_for("write"))
  

if __name__ == '__main__':
    app.run()