from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает и не отключается!"

def run():
    app.run(host="0.0.0.0", port=5000)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()
