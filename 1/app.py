import customtkinter as ctk
from repository import Repository
from tkinter import messagebox
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

# Configurações globais de tema
ctk.set_appearance_mode("light") 

# --- CLASSES DE INTERFACE (MODAIS) ---

class TarefaModal(ctk.CTkToplevel):
    def __init__(self, parent, usuario_id, repo, tarefa=None, callback_atualizar=None):
        super().__init__(parent)
        self.usuario_id = usuario_id
        self.repo = repo
        self.tarefa = tarefa
        self.callback_atualizar = callback_atualizar
        
        self.title("Atividade" if not tarefa else "Editar Atividade")
        self.geometry("500x650")
        self.configure(fg_color="white")
        
        # Garante foco no modal
        self.after(10, self.lift)
        self.grab_set() 

        self.setup_ui()

    def setup_ui(self):
        # Header baseado no Figma
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        ctk.CTkLabel(header_frame, text="Atividade LIP", font=("Arial", 22, "bold"), text_color="black").pack(anchor="w")
        ctk.CTkLabel(header_frame, text="Preencha os detalhes da sua tarefa", font=("Arial", 12), text_color="gray").pack(anchor="w")

        # Inputs
        ctk.CTkLabel(self, text="Nome da atividade", font=("Arial", 12, "bold"), text_color="black").pack(anchor="w", padx=30)
        self.entry_nome = ctk.CTkEntry(self, width=440, height=40)
        self.entry_nome.pack(padx=30, pady=(5, 15))

        ctk.CTkLabel(self, text="Data limite (AAAA-MM-DD)", font=("Arial", 12, "bold"), text_color="black").pack(anchor="w", padx=30)
        self.entry_data = ctk.CTkEntry(self, width=440, height=40)
        self.entry_data.pack(padx=30, pady=(5, 15))

        ctk.CTkLabel(self, text="Prioridade", font=("Arial", 12, "bold"), text_color="black").pack(anchor="w", padx=30)
        self.combo_prio = ctk.CTkComboBox(self, values=["Baixa", "Média", "Alta"], width=440, height=40)
        self.combo_prio.pack(padx=30, pady=(5, 15))

        ctk.CTkLabel(self, text="Descrição da tarefa", font=("Arial", 12, "bold"), text_color="black").pack(anchor="w", padx=30)
        self.txt_desc = ctk.CTkTextbox(self, width=440, height=100, border_width=2)
        self.txt_desc.pack(padx=30, pady=(5, 15))

        # Botão Salvar
        btn_texto = "Salvar atividade" if not self.tarefa else "Atualizar atividade"
        self.btn_salvar = ctk.CTkButton(self, text=btn_texto, fg_color="#0061A8", height=45, font=("Arial", 14, "bold"), command=self.salvar)
        self.btn_salvar.pack(fill="x", padx=30, pady=10)

        # Preenchimento automático (Edição)
        if self.tarefa:
            self.entry_nome.insert(0, self.tarefa.titulo)
            self.entry_data.insert(0, self.tarefa.data_limite)
            self.combo_prio.set(self.tarefa.prioridade)
            self.txt_desc.insert("1.0", self.tarefa.descricao)

    def salvar(self):
        nome = self.entry_nome.get()
        data = self.entry_data.get()
        prio = self.combo_prio.get()
        desc = self.txt_desc.get("1.0", "end-1c")

        if not nome or not data:
            messagebox.showwarning("Aviso", "Nome e Data são obrigatórios!")
            return

        if self.tarefa:
            self.repo.atualizar_tarefa_completa(self.tarefa.id, nome, desc, prio, data)
        else:
            self.repo.cadastrar_tarefa(self.usuario_id, nome, desc, prio, data)

        if self.callback_atualizar:
            self.callback_atualizar()
        self.destroy()

# --- TELAS PRINCIPAIS ---

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        self.logo_label = ctk.CTkLabel(self.main_container, text="✓", font=("Arial", 60, "bold"), width=120, height=120, fg_color="#4CAFFF", corner_radius=60, text_color="white")
        self.logo_label.pack(pady=(0, 40))

        self.entry_user = ctk.CTkEntry(
            self.main_container, 
            placeholder_text="USERNAME (EMAIL)", 
            width=300, 
            height=45, 
            border_color="white", 
            fg_color="transparent", 
            border_width=2,
            text_color="white",                
            placeholder_text_color="#CCCCCC"    
        )
        self.entry_user.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(
            self.main_container, 
            placeholder_text="PASSWORD", 
            show="*", 
            width=300, 
            height=45, 
            border_color="white", 
            fg_color="transparent", 
            border_width=2,
            text_color="white",                
            placeholder_text_color="#CCCCCC"    
        )
        self.entry_pass.pack(pady=10)

        self.btn_login = ctk.CTkButton(self.main_container, text="LOGIN", command=self.fazer_login, width=300, height=45, fg_color="white", text_color="#0095FF", font=("Arial", 14, "bold"))
        self.btn_login.pack(pady=25)

        self.btn_ir_cadastro = ctk.CTkButton(self, text="CRIAR CONTA", command=lambda: self.controller.exibir_tela("cadastro"), width=150, height=30, fg_color="white", text_color="#0095FF", corner_radius=20)
        self.btn_ir_cadastro.place(relx=0.5, rely=0.95, anchor="center")

    def fazer_login(self):
        email = self.entry_user.get()
        senha = self.entry_pass.get()
        usuario = self.controller.repo.login(email, senha)
        if usuario:
            self.controller.mudar_para_tarefas(usuario)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

class CadastroFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        self.logo_label = ctk.CTkLabel(self.main_container, text="✓", font=("Arial", 60, "bold"), width=120, height=120, fg_color="#4CAFFF", corner_radius=60, text_color="white")
        self.logo_label.pack(pady=(0, 40))

        self.entry_nome = ctk.CTkEntry(self.main_container, placeholder_text="USERNAME", width=300, height=45, border_color="white", fg_color="transparent", border_width=2,
            text_color="white",                
            placeholder_text_color="#CCCCCC" )
        self.entry_nome.pack(pady=10)

        self.entry_email = ctk.CTkEntry(self.main_container, placeholder_text="EMAIL", width=300, height=45, border_color="white", fg_color="transparent", border_width=2,
            text_color="white",                
            placeholder_text_color="#CCCCCC" )
        self.entry_email.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self.main_container, placeholder_text="PASSWORD", show="*", width=300, height=45, border_color="white", fg_color="transparent", border_width=2,
            text_color="white",                
            placeholder_text_color="#CCCCCC" )
        self.entry_pass.pack(pady=10)

        self.btn_registrar = ctk.CTkButton(self.main_container, text="CRIAR CONTA", command=self.registrar, width=300, height=45, fg_color="white", text_color="#0095FF", font=("Arial", 14, "bold"))
        self.btn_registrar.pack(pady=25)

        self.btn_ir_login = ctk.CTkButton(self, text="LOGIN", command=lambda: self.controller.exibir_tela("login"), width=150, height=30, fg_color="white", text_color="#0095FF", corner_radius=20)
        self.btn_ir_login.place(relx=0.5, rely=0.95, anchor="center")

    def registrar(self):
        nome = self.entry_nome.get(); email = self.entry_email.get(); senha = self.entry_pass.get()
        if nome and email and senha:
            if self.controller.repo.cadastrar_usuario(nome, email, senha):
                messagebox.showinfo("Sucesso", "Conta criada!")
                self.controller.exibir_tela("login")
            else:
                messagebox.showerror("Erro", "E-mail já cadastrado.")
        else:
            messagebox.showwarning("Aviso", "Preencha tudo!")

class DashbordFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, usuario):
        super().__init__(parent, fg_color="#F3F5F9") 
        self.controller = controller
        self.usuario = usuario
        # Define a ordenação padrão
        self.ordenacao_atual = "Prioridade" 

        self.setup_navbar()
        self.setup_header()
        
        self.columns_container = ctk.CTkFrame(self, fg_color="transparent")
        self.columns_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.renderizar_tarefas()

    def setup_navbar(self):
        nav = ctk.CTkFrame(self, fg_color="white", height=70, corner_radius=0)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        # 1. Nome do sistema na esquerda
        ctk.CTkLabel(nav, text="Gerenciador\nde tarefas", text_color="#0061A8", 
                      font=("Arial", 16, "bold"), justify="left").pack(side="left", padx=(30, 40))

        # 2. Botões de navegação colados no nome (sem expandir o frame)
        menu_left = ctk.CTkFrame(nav, fg_color="transparent")
        menu_left.pack(side="left")
        
        # Botão Tarefas (Ativo)
        self.btn_nav_tarefas = ctk.CTkButton(menu_left, text="Tarefas", fg_color="transparent", 
                                             text_color="#0061A8", font=("Arial", 13, "bold"), 
                                             width=100, hover=False)
        self.btn_nav_tarefas.pack(side="left", padx=5)

        # Botão Relatórios (Inativo)
        self.btn_nav_relat = ctk.CTkButton(menu_left, text="Relatório", fg_color="transparent", 
                                            text_color="gray", font=("Arial", 13), 
                                            width=100, command=lambda: self.controller.exibir_tela("relatorios"))
        self.btn_nav_relat.pack(side="left", padx=5)

        # 3. Botão Logout na extrema direita
        ctk.CTkButton(nav, text="Logout", fg_color="transparent", text_color="black", 
                      command=lambda: self.controller.exibir_tela("login")).pack(side="right", padx=30)

        # 4. Botão Nova Tarefa à esquerda do Logout
        ctk.CTkButton(nav, text="+ Nova tarefa", fg_color="#0061A8", corner_radius=8, 
                      width=120, command=self.nova_tarefa).pack(side="right", padx=10)

    def setup_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 10))
        
        # Container para Título e Switch
        title_container = ctk.CTkFrame(header, fg_color="transparent")
        title_container.pack(fill="x")

        ctk.CTkLabel(title_container, text="Dashboard De Tarefas", 
                      font=("Arial", 32, "bold"), text_color="#1A1C1E").pack(side="left")

        # Switch de Ordenação (Segmented Button)
        self.seg_button = ctk.CTkSegmentedButton(title_container, 
                                                 values=["Prioridade", "Data"],
                                                 command=self.mudar_ordenacao,
                                                 selected_color="#0061A8",
                                                 selected_hover_color="#004e87")
        self.seg_button.pack(side="right", pady=10)
        self.seg_button.set("Prioridade")

    def mudar_ordenacao(self, valor):
        self.ordenacao_atual = valor
        self.renderizar_tarefas()

    def renderizar_tarefas(self):
        for child in self.columns_container.winfo_children(): 
            child.destroy()

        tarefas = self.controller.repo.listar_tarefas(self.usuario.id)

        # Lógica de Ordenação
        if self.ordenacao_atual == "Prioridade":
            # Define o peso das prioridades para ordenação
            peso = {"Alta": 0, "Média": 1, "Baixa": 2}
            tarefas.sort(key=lambda t: peso.get(t.prioridade, 3))
        else:
            # Ordena por data (AAAA-MM-DD)
            tarefas.sort(key=lambda t: t.data_limite)

        colunas = {
            "Pendente": ("● Pendentes", "#8B5E3C"), 
            "Em Andamento": ("● Em Andamento", "#0061A8"), 
            "Concluída": ("● Concluídas", "#2E7D32")
        }

        for status, (titulo, cor) in colunas.items():
            col_frame = ctk.CTkFrame(self.columns_container, fg_color="transparent")
            col_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            ctk.CTkLabel(col_frame, text=titulo, text_color=cor, font=("Arial", 16, "bold")).pack(anchor="w", pady=10)
            scroll = ctk.CTkScrollableFrame(col_frame, fg_color="transparent")
            scroll.pack(fill="both", expand=True)

            for t in tarefas:
                if t.status == status: 
                    self.criar_card(scroll, t)

    def criar_card(self, master, tarefa):
        border = "#BA1A1A" if tarefa.esta_atrasada else "#E0E0E0"
        card = ctk.CTkFrame(master, fg_color="white", corner_radius=10, border_width=2, border_color=border)
        card.pack(fill="x", pady=10, padx=5)
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(10, 0))

        prio_c = {"Alta": "#FFDAD4", "Média": "#FFDDB3", "Baixa": "#D7E3FF"}.get(tarefa.prioridade, "#EEE")
        ctk.CTkLabel(header, text=tarefa.prioridade.upper(), font=("Arial", 9, "bold"), fg_color=prio_c, text_color="#333", corner_radius=4, width=70).pack(side="left")

        if tarefa.esta_atrasada:
            ctk.CTkLabel(header, text="⚠️ ATRASADA", font=("Arial", 9, "bold"), text_color="#BA1A1A").pack(side="right")
        
        lbl_titulo = ctk.CTkLabel(card, text=tarefa.titulo, font=("Arial", 14, "bold"), text_color="#1A1C1E", wraplength=180, justify="left", cursor="hand2")
        lbl_titulo.pack(anchor="w", padx=15, pady=5)
        lbl_titulo.bind("<Button-1>", lambda e, t=tarefa: self.editar_tarefa(t))
        
        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkButton(footer, text="<", width=30, height=25, fg_color="#E0E0E0", text_color="black", command=lambda t=tarefa: self.mover_status(t, True)).pack(side="left", padx=2)
        ctk.CTkLabel(footer, text=f"📅 {tarefa.data_limite}", font=("Arial", 10), text_color="gray").pack(side="left", expand=True)
        ctk.CTkButton(footer, text=">", width=30, height=25, fg_color="#0061A8", command=lambda t=tarefa: self.mover_status(t)).pack(side="right", padx=2)

    def mover_status(self, tarefa, retroceder=False):
        fluxo = ["Pendente", "Em Andamento", "Concluída"]
        idx = fluxo.index(tarefa.status) if tarefa.status in fluxo else 0
        if retroceder and idx > 0: novo = fluxo[idx-1]
        elif not retroceder and idx < 2: novo = fluxo[idx+1]
        else: return
        self.controller.repo.atualizar_status(tarefa.id, novo)
        self.renderizar_tarefas()

    def nova_tarefa(self):
        TarefaModal(self, self.usuario.id, self.controller.repo, callback_atualizar=self.renderizar_tarefas)

    def editar_tarefa(self, tarefa):
        TarefaModal(self, self.usuario.id, self.controller.repo, tarefa=tarefa, callback_atualizar=self.renderizar_tarefas)


class RelatorioFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, usuario):
        super().__init__(parent, fg_color="#F3F5F9")
        self.controller = controller
        self.usuario = usuario
        self.tarefas = self.controller.repo.listar_tarefas(self.usuario.id)

        self.setup_navbar()
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(30, 20))
        ctk.CTkLabel(header, text="Relatórios de Tarefas", font=("Arial", 32, "bold"), text_color="#1A1C1E").pack(anchor="w")
        ctk.CTkLabel(header, text="Dashboard analítico de performance e produtividade.", text_color="gray", font=("Arial", 14)).pack(anchor="w")

        stats_container = ctk.CTkFrame(self, fg_color="transparent")
        stats_container.pack(fill="x", padx=40, pady=10)

        total = len(self.tarefas)
        concluidas = len([t for t in self.tarefas if t.status == "Concluída"])
        taxa = (concluidas / total * 100) if total > 0 else 0

        self.criar_card_stat(stats_container, "TOTAL DE TAREFAS", f"{total}", "Volume total de entregas", 0)
        self.criar_card_stat(stats_container, "TAXA DE CONCLUSÃO", f"{taxa:.1f}%", "Eficiência operacional alta", 1)
        self.criar_card_stat(stats_container, "TAREFAS CONCLUÍDAS", f"{concluidas}", "Volume total de concluídas", 2)

    def setup_navbar(self):
        nav = ctk.CTkFrame(self, fg_color="white", height=70, corner_radius=0)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        # 1. Nome do sistema na esquerda (Mesmo padding do Dashboard)
        ctk.CTkLabel(nav, text="Gerenciador\nde tarefas", text_color="#0061A8", 
                      font=("Arial", 16, "bold"), justify="left").pack(side="left", padx=(30, 40))

        # 2. Botões de navegação
        menu_left = ctk.CTkFrame(nav, fg_color="transparent")
        menu_left.pack(side="left")
        
        # Botão Tarefas (Inativo nesta tela)
        ctk.CTkButton(menu_left, text="Tarefas", fg_color="transparent", 
                      text_color="gray", font=("Arial", 13), 
                      width=100, command=lambda: self.controller.exibir_tela("dashboard")).pack(side="left", padx=5)
        
        # Botão Relatório (Ativo nesta tela)
        ctk.CTkButton(menu_left, text="Relatório", fg_color="transparent", 
                      text_color="#0061A8", font=("Arial", 13, "bold"), 
                      width=100, hover=False).pack(side="left", padx=5)

        # 3. Botão Logout na extrema direita
        ctk.CTkButton(nav, text="Logout", fg_color="transparent", text_color="black", 
                      command=lambda: self.controller.exibir_tela("login")).pack(side="right", padx=30)

        # 4. Botão Gerar Relatório à esquerda do Logout
        ctk.CTkButton(nav, text="Gerar relatório", fg_color="#0061A8", corner_radius=8, 
                      width=140, font=("Arial", 12, "bold"), command=self.gerar_pdf).pack(side="right", padx=10)

    def criar_card_stat(self, master, titulo, valor, subtitulo, coluna):
        card = ctk.CTkFrame(master, fg_color="white", corner_radius=12, height=180, width=300)
        card.grid(row=0, column=coluna, padx=15, pady=10, sticky="nsew")
        card.grid_propagate(False)
        master.grid_columnconfigure(coluna, weight=1)

        ctk.CTkLabel(card, text=titulo, font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(card, text=valor, font=("Arial", 36, "bold"), text_color="#0061A8").pack(anchor="w", padx=20)
        ctk.CTkLabel(card, text=subtitulo, font=("Arial", 10), text_color="#4CAFFF").pack(anchor="w", padx=20, pady=5)

    def gerar_pdf(self):
        # 1. Coleta e Formatação dos Dados
        total = len(self.tarefas)
        concluidas_objs = [t for t in self.tarefas if t.status == "Concluída"]
        pendentes_objs = [t for t in self.tarefas if t.status == "Pendente"]
        andamento_objs = [t for t in self.tarefas if t.status == "Em Andamento"]
        
        taxa = (len(concluidas_objs) / total * 100) if total > 0 else 0
        
        # Transforma listas em strings separadas por vírgula
        txt_pendentes = ", ".join([t.titulo for t in pendentes_objs]) or "Nenhuma"
        txt_andamento = ", ".join([t.titulo for t in andamento_objs]) or "Nenhuma"
        txt_concluidas = ", ".join([t.titulo for t in concluidas_objs]) or "Nenhuma"

        # 2. Montagem do Texto conforme Modelo
        texto_completo = (
            f"RELATÓRIO DE TAREFAS\n\n"
            f"Este relatório apresenta uma visão geral do estado atual das tarefas cadastradas no sistema, "
            f"permitindo uma análise clara do progresso e da organização das atividades.\n\n"
            f"Atualmente, o sistema registra um total de {total} tarefas. Dentre essas, {len(concluidas_objs)} "
            f"foram concluídas com sucesso, o que representa uma taxa de conclusão de {taxa:.1f}%. Esses dados "
            f"indicam o nível de produtividade e eficiência na execução das atividades propostas.\n\n"
            f"No que diz respeito às tarefas pendentes, as tarefas classificadas como pendentes são: {txt_pendentes}. "
            f"A análise dessas tarefas é fundamental para o planejamento das próximas ações.\n\n"
            f"Além disso, as tarefas que encontram-se em andamento: {txt_andamento}. Essas atividades "
            f"representam o trabalho atualmente em progresso.\n\n"
            f"Por outro lado, as tarefas concluídas são: {txt_concluidas}. Essas atividades finalizadas "
            f"demonstram o progresso obtido até o momento.\n\n"
            f"Recomenda-se a análise periódica dessas informações para garantir uma melhor organização."
        )

        # 3. Criação do PDF com ReportLab
        nome_arquivo = f"Relatorio_{self.usuario.nome}_{datetime.now().strftime('%d%m%Y_%H%M')}.pdf"
        try:
            c = canvas.Canvas(nome_arquivo, pagesize=letter)
            largura, altura = letter
            
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, altura - 50, "Sistema de Gerenciamento de Tarefas")
            c.setFont("Helvetica", 10)
            c.drawString(50, altura - 65, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            c.line(50, altura - 75, largura - 50, altura - 75)

            
            c.setFont("Helvetica", 12)
            linhas = simpleSplit(texto_completo, "Helvetica", 12, largura - 100)
            
            y = altura - 100
            for linha in linhas:
                if y < 50: # Nova página se acabar o espaço
                    c.showPage()
                    y = altura - 50
                    c.setFont("Helvetica", 12)
                c.drawString(50, y, linha)
                y -= 18

            c.save()
            messagebox.showinfo("Sucesso", f"Relatório gerado: {nome_arquivo}")
            os.startfile(nome_arquivo) # Abre o PDF automaticamente (Windows)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar PDF: {e}")

# --- APP CENTRAL ---

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Tarefas")
        self.geometry("1100x750")

        try:
            # No Windows, usa-se o .ico
            self.iconbitmap("logo.ico") 
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        self.configure(fg_color="#0095FF")
        self.repo = Repository()
        self.usuario_logado = None

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both")
        self.exibir_tela("login")

    def exibir_tela(self, nome_tela):
        for child in self.container.winfo_children():
            child.destroy()

        if nome_tela == "login":
            self.tela_atual = LoginFrame(self.container, self)
        elif nome_tela == "cadastro":
            self.tela_atual = CadastroFrame(self.container, self)
        elif nome_tela == "dashboard":
            self.tela_atual = DashbordFrame(self.container, self, self.usuario_logado)
        elif nome_tela == "relatorios": # <--- NOVA TELA
            self.tela_atual = RelatorioFrame(self.container, self, self.usuario_logado)
    
        self.tela_atual.pack(expand=True, fill="both")

    def mudar_para_tarefas(self, usuario):
        self.usuario_logado = usuario
        self.exibir_tela("dashboard")

if __name__ == "__main__":
    app = App()
    app.mainloop()


# Organizar classes