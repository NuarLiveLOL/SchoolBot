from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!"

def run():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)  # <- Важно!

def keep_alive():
    thread = threading.Thread(target=run, daemon=True)  # <- Даем Flask фоновый поток
    thread.start()
