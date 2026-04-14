from datetime import datetime

class Usuario:
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email

class Tarefa:
    def __init__(self, id, usuario_id, titulo, descricao, prioridade, data_limite, status, data_conclusao=None):
        self.id = id
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.data_limite = data_limite
        self.status = status
        self.data_conclusao = data_conclusao

    @property
    def esta_atrasada(self):
        if self.status != 'Concluída' and self.data_limite:
            hoje = datetime.now().date()
            prazo = datetime.strptime(self.data_limite, '%Y-%m-%d').date()
            return hoje > prazo
        return False