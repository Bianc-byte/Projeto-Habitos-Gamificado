
from flask import Flask, render_template, request
import os
import sqlite3


app = Flask(__name__)


def conectar_banco():
    caminho = os.path.join(os.path.dirname(__file), "database", "habitos.db")
    return sqlite3.connect(caminho)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
