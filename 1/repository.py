from database import get_connection
from auth import hash_senha
from models import Tarefa, Usuario
from datetime import datetime

class Repository:
    def __init__(self):
        self.conn = get_connection()

    # --- USUÁRIOS ---
    def cadastrar_usuario(self, nome, email, senha):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                           (nome, email, hash_senha(senha)))
            self.conn.commit()
            return True
        except: return False

    def login(self, email, senha):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        if user_data and hash_senha(senha) == user_data[3]:
            return Usuario(user_data[0], user_data[1], user_data[2])
        return None

    # --- TAREFAS ---
    def cadastrar_tarefa(self, usuario_id, titulo, desc, prio, data_limite):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO tarefas (usuario_id, titulo, descricao, prioridade, data_limite, status)
                          VALUES (?, ?, ?, ?, ?, 'Pendente')''',
                       (usuario_id, titulo, desc, prio, data_limite))
        self.conn.commit()

    def listar_tarefas(self, usuario_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tarefas WHERE usuario_id = ?", (usuario_id,))
        rows = cursor.fetchall()
        return [Tarefa(*row) for row in rows]

    def atualizar_status(self, tarefa_id, novo_status):
        data_conclusao = datetime.now().strftime('%Y-%m-%d') if novo_status == 'Concluída' else None
        cursor = self.conn.cursor()
        cursor.execute("UPDATE tarefas SET status = ?, data_conclusao = ? WHERE id = ?",
                       (novo_status, data_conclusao, tarefa_id))
        self.conn.commit()

    def remover_tarefa(self, tarefa_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        self.conn.commit()

    # --- RELATÓRIOS ---
    def get_relatorio(self, usuario_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM tarefas WHERE usuario_id = ? GROUP BY status", (usuario_id,))
        stats = dict(cursor.fetchall())
        
        cursor.execute('''SELECT data_conclusao, COUNT(*) FROM tarefas 
                          WHERE usuario_id = ? AND status = 'Concluída' 
                          GROUP BY data_conclusao''', (usuario_id,))
        por_dia = cursor.fetchall()
        
        return {"geral": stats, "produtividade_diaria": por_dia}

    def atualizar_tarefa_completa(self, tarefa_id, titulo, desc, prio, data):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE tarefas SET titulo=?, descricao=?, prioridade=?, data_limite=? 
                      WHERE id=?''', (titulo, desc, prio, data, tarefa_id))
        self.conn.commit()