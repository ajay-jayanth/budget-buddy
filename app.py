from flask import Flask, render_template
from flask_cors import CORS

name = 'Budget Buddy'
app = Flask(name) 
CORS(app)

app.config.update( 
    SECRET_KEY='dev'
)

@app.route('/')
def index_function(): 
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000, threaded=True)
