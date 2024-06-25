from flask import Flask

app = Flask(__name__)

from routes.mainpage import mainpage
from routes.compile import compile_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8787, debug=True)