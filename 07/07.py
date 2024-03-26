from flask import Flask, render_template
import os
 
app = Flask(__name__)
 
img = os.path.join('static', 'photo')
 
@app.route('/')
def home():
    file = os.path.join(img, 'a.jpg')
    return render_template('index.html', image=file)
 
if __name__ == '__main__':
    app.run()