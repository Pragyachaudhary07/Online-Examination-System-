from flask import Flask, render_template, request, redirect, session, url_for
import json

app = Flask(_name_)
app.secret_key = 'exam_secret'

# Load questions
with open('questions.json') as f:
    questions = json.load(f)

users = {
    'admin': 'admin123',
    'student1': 'pass123'
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if users.get(username) == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Invalid credentials!"

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    if session['username'] == 'admin':
        return render_template('dashboard.html', admin=True)
    return render_template('dashboard.html', admin=False)

@app.route('/exam', methods=['GET', 'POST'])
def exam():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        score = 0
        for q in questions:
            selected = request.form.get(q['id'])
            if selected == q['answer']:
                score += 1
        return render_template('result.html', score=score, total=len(questions))
    return render_template('exam.html', questions=questions)

if _name_ == '_main_':
    app.run(debug=True)
