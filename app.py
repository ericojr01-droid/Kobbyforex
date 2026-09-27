import os
from flask import Flask
from modules import register_all

app = Flask(__name__)
app.secret_key = "kobbyforex_modular_2026"

register_all(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
