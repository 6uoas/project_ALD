from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "알라딘 최저가 탐색 프로그램"

if __name__ == "__main__":
    app.run()