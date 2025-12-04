
from flask import Flask, render_template, request, session, redirect
import os
import sqlite3
from datetime import date


app = Flask(__name__)

app.secret_key = "linkin_park_secret_key"


def conectar_banco():
    caminho = os.path.join(os.path.dirname(__file__), "database", "habitos.db")
    return sqlite3.connect(caminho, timeout=10, check_same_thread=False)


def calcular_streak(usuario_id, habito_id):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT data_conclusao
        FROM progresso_diario
        WHERE usuario_id = ? AND habito_id = ?
        ORDER BY data_conclusao DESC
    """, (usuario_id, habito_id))

    datas = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not datas:
        return 0

    streak = 1
    hoje = date.today()

    for data_str in datas[1:]:
        dia = date.fromisoformat(data_str)
        anterior = hoje.fromordinal(hoje.toordinal() - streak)

        if dia == anterior:
            streak += 1
        else:
            break

    return streak


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

    cursor.execute("""
        SELECT id, titulo, descricao
        FROM habitos
        WHERE usuario_id = ?
        ORDER BY id DESC
        LIMIT 5
    """, (session["usuario_id"],))
    habitos_recentes = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) FROM habitos WHERE usuario_id = ?
    """, (session["usuario_id"],))
    total_habitos = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        nome=session["usuario_nome"],
        habitos=habitos_recentes,
        total_habitos=total_habitos
    )


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

        return redirect("/habitos")
    return render_template("criar_habito.html")


@app.route("/habitos")
def habitos():
    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, titulo, descricao
        FROM habitos
        WHERE usuario_id = ?
    """, (session["usuario_id"],))

    lista = cursor.fetchall()
    conn.close()

    habitos_completos = []
    for h in lista:
        streak = calcular_streak(session["usuario_id"], h[0])
        habitos_completos.append((h[0], h[1], h[2], streak))

    return render_template("habitos.html", habitos=lista)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_habito(id):
    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar_banco()
    cursor = conn.cursor()

    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]

        cursor.execute("""
            UPDATE habitos
            SET titulo = ?, descricao = ?
            WHERE id = ? AND usuario_id = ?
        """, (titulo, descricao, id, session["usuario_id"]))

        conn.commit()
        conn.close()

        return redirect("/habitos")

    # GET — pegar hábito existente
    cursor.execute("""
        SELECT id, titulo, descricao
        FROM habitos
        WHERE id = ? AND usuario_id = ?
    """, (id, session["usuario_id"]))

    habito = cursor.fetchone()
    conn.close()

    return render_template("editar_habito.html", habito=habito)


@app.route("/deletar_habito/<int:id>")
def deletar_habito(id):
    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM habitos
        WHERE id = ? AND usuario_id = ?
    """, (id, session["usuario_id"]))

    conn.commit()
    conn.close()

    return redirect("/habitos")


@app.route("/marcar/<int:habito_id>")
def marcar_habito(habito_id):
    if "usuario_id" not in session:
        return redirect("/login")

    usuario_id = session["usuario_id"]
    hoje = date.today().isoformat()

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM progresso_diario
        WHERE usuario_id = ? AND habito_id = ? AND data = ?
    """, (usuario_id, habito_id, hoje))

    registro = cursor.fetchone()

    if registro:
        conn.close()
        return redirect("/habitos")

    cursor.execute("""
        INSERT INTO progresso_diario (usuario_id, habito_id, data)
        VALUES (?, ?, ?)
    """, (usuario_id, habito_id, hoje))

    conn.commit()
    conn.close()

    return redirect("/habitos")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
