from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/convert', methods=['POST'])
def convert():
    # Placeholder for conversion logic
    return redirect('/upload')

if __name__ == '__main__':
    app.run(debug=True)
