
from flask import Flask, render_template, request
import os
import sqlite3


app = Flask(__name__)


def conectar_banco():
    caminho = os.path.join(os.path.dirname(__file__), "database", "habitos.db")
    return sqlite3.connect(caminho, timeout=10, check_same_thread=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM usuarios WHERE email = ? AND senha = ?
            """, (email, senha))

        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return render_template("login.html", mensagem="Login realizado com sucesso!")
        else:
            return render_template("login.html", mensagem="Email ou senha incorretos!")
    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO usuarios (nome, email, senha)
                VALUES (?, ?, ?)
            """, (nome, email, senha))

            conn.commit()
            mensagem = "Conta criada com sucesso!"

        except sqlite3.IntegrityError:
            mensagem = "Email já está cadastrado!"

        finally:
            conn.close()

        return render_template("cadastro.html", mensagem=mensagem)

    return render_template("cadastro.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
