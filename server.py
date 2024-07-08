from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from csv_editor import webctrl_csv, metasys_csv, lutron_csv
from waitress import serve
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SAVED_FOLDER'] = 'saved'
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    files = [f for f in os.listdir(app.config['SAVED_FOLDER']) if f.endswith('.html')]
    return render_template('view.html', files=files)

@app.route('/view/<filename>')
def view_file(filename):
    return send_from_directory(app.config['SAVED_FOLDER'], filename)

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        if 'webctrl_file' in request.files:
            file = request.files['webctrl_file']
            if file and file.filename.endswith('.csv'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                webctrl_csv(filepath)

        if 'metasys_file' in request.files:
            file = request.files['metasys_file']
            if file and file.filename.endswith('.csv'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                metasys_csv(filepath)

        if 'lutron_file' in request.files:
            file = request.files['lutron_file']
            if file and file.filename.endswith('.csv'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                lutron_csv(filepath)

        flash('Files successfully processed')
        return redirect(url_for('view'))

    return render_template('generate.html')

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['SAVED_FOLDER'], exist_ok=True)
    serve(app, host="0.0.0.0", port=8000)
