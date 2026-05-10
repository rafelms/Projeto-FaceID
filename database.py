import sqlite3

def init_db():
    # Cria/conecta ao banco de dados local
    conn = sqlite3.connect('faceid.db')
    cursor = conn.cursor()

    # Tabela pessoas (Conforme exigido no PDF)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela imagens (Conforme exigido no PDF)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pessoa_id INTEGER,
            caminho_imagem TEXT NOT NULL,
            FOREIGN KEY (pessoa_id) REFERENCES pessoas (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados 'faceid.db' criado com sucesso!")

if __name__ == '__main__':
    init_db()