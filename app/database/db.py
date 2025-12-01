import sqlite3
import os
db_path = os.path.join(os.path.dirname(__file__), "habitos.db")


def criar_tabela_usuarios():
    conexao = sqlite3.connect(db_path)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            xp INTEGER DEFAULT 0,
            nivel INTEGER DEFAULT 1
        );
    """)
