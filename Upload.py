from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def upload():
    content = "Upload Page"
    return render_template('upload.html', content = content)

if __name__ == '__main__':
    app.run(debug=True)