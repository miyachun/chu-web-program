from flask import Flask, render_template, request, url_for, flash, redirect, abort
import sqlite3
import datetime
from werkzeug.utils import secure_filename

import os
app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
upload_folder = os.path.join('static', 'uploads') 
app.config['UPLOAD'] = upload_folder
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

Mnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM COMPANY ORDER BY time DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        content = request.form['content']   
        image = request.files['image']
        filename = secure_filename(image.filename) 

        if not id:
            flash('id無填')
        elif not name :
            flash('name無填')
        elif not content :
            flash('content無填')
        elif not filename:
            nopic='no.jpg'
            conn = get_db_connection()
            conn.execute('INSERT INTO COMPANY (id, name, content, image, time ) VALUES (?, ?, ?, ?, ?)',
                         (id, name, content, nopic, Mnow ))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        else:
            image.save(os.path.join(app.config['UPLOAD'], filename))
            conn = get_db_connection()
            conn.execute('INSERT INTO COMPANY (id, name, content, image, time ) VALUES (?, ?, ?, ?, ?)',
                         (id, name, content, filename, Mnow ))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM COMPANY WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    
    post = get_post(id)

    if request.method == 'POST':        
        name = request.form['name']
        content = request.form['content']        
        image = request.files['image']
        filename = secure_filename(image.filename)
        
        print(filename)
        if not filename:
            conn = get_db_connection()
            conn.execute('UPDATE COMPANY SET name = ?, content = ?'
                         ' WHERE id = ?',
                         ( name, content, id))

            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
        else:
            image.save(os.path.join(app.config['UPLOAD'], filename))
            conn = get_db_connection()
            conn.execute('UPDATE COMPANY SET name = ?, content = ?, image = ?'
                         ' WHERE id = ?',
                         ( name, content, filename, id))

            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM COMPANY WHERE id = ?', (id,))
    conn.commit()
    conn.close()    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
