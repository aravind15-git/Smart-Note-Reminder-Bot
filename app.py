from flask import Flask, render_template, request, redirect
import json
from datetime import datetime

app = Flask(__name__)

REMINDER_FILE = 'reminders.json'

# Load reminders from file
def load_reminders():
    try:
        with open(REMINDER_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save reminders to file
def save_reminders(reminders):
    with open(REMINDER_FILE, 'w') as file:
        json.dump(reminders, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def home():
    reminders = load_reminders()

    if request.method == 'POST':
        text = request.form['reminder']
        if text.strip():
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            reminders.append({'reminder': text.strip(), 'time': timestamp})
            save_reminders(reminders)
        return redirect('/')

    return render_template('index.html', reminders=reminders)

@app.route('/clear')
def clear():
    save_reminders([])
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
