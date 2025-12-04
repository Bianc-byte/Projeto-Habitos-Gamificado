import sqlite3
import os


def criar_tabelas():
    caminho = os.path.join(os.path.dirname(__file__), "database", "habitos.db")
    conn = sqlite3.connect(caminho)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habitos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        titulo TEXT NOT NULL,
        descricao TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progresso_diario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        habito_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        UNIQUE(usuario_id, habito_id, data),
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY(habito_id) REFERENCES habitos(id)
    );
    """)

    conn.commit()
    conn.close()
    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    criar_tabelas()
