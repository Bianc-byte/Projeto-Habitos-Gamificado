
from flask import Flask, render_template, request, session, redirect
import os
import sqlite3


app = Flask(__name__)

app.secret_key = "linkin_park_secret_key"


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
            session["usuario_id"] = usuario[0]
            session["usuario_nome"] = usuario[1]
            return redirect("/dashboard")
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
    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM usuarios WHERE id = ?",
                   (session["usuario_id"],))
    habitos = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html", nome=session["usuario_nome"], habitos=habitos)


@app.route("/criar_habito", methods=["GET", "POST"])
def criar_habito():
    if "usuario_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        usuario_id = session["usuario_id"]

        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO habitos (usuario_id, titulo, descricao)
            VALUES (?, ?, ?)
        """, (usuario_id, titulo, descricao))

        conn.commit()
        conn.close()

        return render_template("criar_habito.html", mensagem="Hábito criado com sucesso!")

    return render_template("criar_habito.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
