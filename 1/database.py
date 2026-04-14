import sqlite3

def get_connection():
    return sqlite3.connect("gerenciador_tarefas.db")

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    
    # Tabela de Tarefas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo TEXT NOT NULL,
            descricao TEXT,
            prioridade TEXT CHECK(prioridade IN ('Baixa', 'Média', 'Alta')),
            data_limite DATE,
            status TEXT CHECK(status IN ('Pendente', 'Em Andamento', 'Concluída')),
            data_conclusao DATE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    conn.commit()
    conn.close()