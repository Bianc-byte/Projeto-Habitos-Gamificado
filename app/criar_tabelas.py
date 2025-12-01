import sqlite3
import os


def criar_tabelas():
    caminho = os.path.join(os.path.dirname(__file__), "database", "habitos.db")
    conn = sqlite3.connect(caminho)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habitos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        titulo TEXT NOT NULL,
        descricao TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """)

    conn.commit()
    conn.close()
    print("Tabela 'habitos' criada com sucesso!")


if __name__ == "__main__":
    criar_tabelas()
