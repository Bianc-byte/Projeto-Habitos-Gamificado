import sqlite3
import os

caminho = os.path.join(os.path.dirname(__file__), "habitos.db")
conn = sqlite3.connect(caminho)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS progresso_habitos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    habito_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    status INTEGER DEFAULT 0,
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (habito_id) REFERENCES habitos(id)
)
""")

conn.commit()
conn.close()

print("Tabela progresso_habitos criada com sucdesso!")
