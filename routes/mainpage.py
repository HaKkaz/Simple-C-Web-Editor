from flask import render_template
from __main__ import app

@app.route('/')
def mainpage():
    return render_template('editor.html')  # Ensure the template is located in the 'templates' directory