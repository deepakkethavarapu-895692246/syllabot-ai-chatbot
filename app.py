from flask import Flask, request, render_template, redirect, url_for, session
import os
import json
import fitz
import uuid
from llm import talkToLLM
from apikey import FLASK_SECRET_KEY

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

UPLOAD_FOLDER = 'syllabi'
INDEX_FILE = 'syllabus_index.json'
USERS_FILE = 'users.json'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_index():
    if not os.path.exists(INDEX_FILE):
        return {}
    with open(INDEX_FILE, 'r') as f:
        return json.load(f)

def save_index(data):
    with open(INDEX_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    return "\n".join(page.get_text() for page in doc)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if users.get(username) == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('upload'))
        else:
            return "Invalid credentials.<br><a href='/login'>⬅️ Back to Login</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return "Username already exists.<br><a href='/create_account'>⬅️ Back</a>"
        users[username] = password
        save_users(users)
        return "Account created successfully. <a href='/login'>Login here</a>"
    return render_template('create_account.html')

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    index = load_index()
    question = None
    answer = None
    selected_dept = None
    selected_course = None
    if request.method == 'POST':
        dept = request.form['department']
        course_number = request.form['course_number']
        question = request.form['question']
        selected_dept = dept
        selected_course = course_number

        matched_key = None
        for key, data in index.items():
            if data['department'] == dept and data['course_number'] == course_number:
                matched_key = key
                break

        if not matched_key:
            return "Course not found.<br><a href='/ask'>⬅️ Back</a>"

        syllabus_file = os.path.join(UPLOAD_FOLDER, index[matched_key]['filename'])
        syllabus_text = extract_text_from_pdf(syllabus_file)
        context = f"Syllabus:\n{syllabus_text}\n\nQuestion: {question}"
        answer = talkToLLM(context)

    return render_template(
        'ask_ui_final.html',
        index=index,
        question=question,
        answer=answer,
        selected_dept=selected_dept,
        selected_course=selected_course
    )

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        dept = request.form['department']
        course_number = request.form['course_number']
        course_name = request.form['course_name']
        filename = f"{dept}_{course_number}_{course_name.replace(' ', '_')}.pdf"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        index = load_index()
        unique_id = str(uuid.uuid4())[:8]
        key = f"{dept}_{course_number}_{unique_id}"
        
        index[key] = {
            "filename": filename,
            "department": dept,
            "course_number": course_number,
            "course_name": course_name
        }
        save_index(index)
        return redirect(url_for('upload'))
    return render_template('upload_ui_final.html', index=load_index())

@app.route('/download/<key>')
def download(key):
    index = load_index()
    if key in index:
        return redirect('/' + os.path.join(UPLOAD_FOLDER, index[key]['filename']))
    return "File not found", 404

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    index = load_index()
    if request.method == 'POST':
        key = request.form['key']
        action = request.form['action']
        if key in index:
            filename = os.path.join(UPLOAD_FOLDER, index[key]['filename'])
            if action == 'delete':
                if os.path.exists(filename):
                    os.remove(filename)
                del index[key]
                save_index(index)
            elif action == 'update_name':
                new_name = request.form['new_name']
                index[key]['course_name'] = new_name
                save_index(index)
    return render_template('manage.html', index=index)

@app.route('/manage_accounts', methods=['GET', 'POST'])
def manage_accounts():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    users = load_users()
    current_user = session.get('username')
    if request.method == 'POST':
        user_to_delete = request.form['user_to_delete']
        if user_to_delete != current_user and user_to_delete in users:
            del users[user_to_delete]
            save_users(users)
    users = load_users()
    return render_template('manage_accounts.html', users=users, current_user=current_user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5081, debug=True)
