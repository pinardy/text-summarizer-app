from flask import render_template, request, flash
from app import app
from main import summarize_text

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def submit_text():
    if request.method == 'POST':
        data = request.form['rawtext']

        if data:
            summary = summarize_text(data)
            flash(summary)
        return render_template('index.html')
        

if __name__ == "__main__":
    app.run()
