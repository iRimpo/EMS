from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from csv_editor import webctrl_csv, metasys_csv, lutron_csv
from waitress import serve
import os
import subprocess

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

def process_files(files):
    file_status = {
        'webctrl_file': webctrl_csv,
        'metasys_file': metasys_csv,
        'lutron_file': lutron_csv,
        'wattstopper_file': lutron_csv,
        'encelium_file': lutron_csv,
        'imonnit_file': lutron_csv,
    }
    errors = []
    for file_key, process_func in file_status.items():
        if file_key in files:
            file = files[file_key]
            if file and file.filename.endswith('.csv'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                try:
                    process_func(filepath)
                except Exception as e:
                    errors.append(f"{file_key.replace('_file', '').capitalize()} section: incorrect format or processing error.")
                    print(f"Error processing {file_key}: {e}")
    return errors

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    files_processed = False
    if request.method == 'POST':
        errors = process_files(request.files)
        if not errors:
            flash('Files successfully processed', 'success')
            # Call the diagram generation
            subprocess.run(['python', 'generate.py'], check=True)
            return redirect(url_for('show_diagram', filename='Diagram.html'))
        else:
            for error in errors:
                flash(error, 'error')
        return render_template('generate.html', files_processed=False)
    return render_template('generate.html', files_processed=False)

@app.route('/show_diagram/<filename>')
def show_diagram(filename):
    return render_template('show_diagram.html', filename=filename)


@app.route('/generate_diagram', methods=['POST'])
def generate_diagram():
    try:
        subprocess.run(['python', 'generate.py'], check=True)
        flash('Diagram successfully generated')
    except subprocess.CalledProcessError as e:
        flash(f'Error generating diagram: {e}')
    return redirect(url_for('view'))

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['SAVED_FOLDER'], exist_ok=True)
    serve(app, host="0.0.0.0", port=8000)
