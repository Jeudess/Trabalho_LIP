# 📝 Sistema de Gerenciamento de Tarefas (Questão 1)

## 📌 Descrição

Aplicação desktop para gerenciamento de tarefas pessoais, desenvolvida para a disciplina de Linguagens de Programação.
Permite organizar atividades, definir prioridades, acompanhar progresso e gerar relatórios.

---

## ⚙️ Funcionalidades

* Cadastro de tarefas (título, descrição, prioridade, data)
* Listagem por status (Pendente, Em andamento, Concluída)
* Atualização de status
* Remoção de tarefas
* Cadastro e login de usuários (com senha criptografada)
* Relatórios de produtividade
* Exportação de relatório em PDF

---

## 🔑 Conta para Teste

Para facilitar a avaliação do sistema, já existe uma conta de administrador cadastrada:

* **Login:** adm
* **Senha:** adm

---

## 🧠 POO Aplicada

* **Abstração:** classes `Usuario` e `Tarefa`
* **Encapsulamento:** regras dentro das classes (ex: tarefa atrasada)
* **Separação de responsabilidades:** divisão entre interface, modelo e dados

---

## 💾 Persistência

* Banco de dados SQLite
* Dados organizados por usuário

---

## 🚀 Como Executar

```bash
pip install -r requirements.txt
python app.py
```

---

## 📦 Dependências

* charset-normalizer==3.4.7
* customtkinter==5.2.2
* darkdetect==0.8.0
* packaging==26.0
* pillow==12.2.0
* reportlab==4.4.10

---

## ✔ Conclusão

A Questão 1 atende aos requisitos do trabalho, incluindo POO, persistência, interface gráfica, regras de negócio e geração de relatórios.
