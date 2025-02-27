import customtkinter as ctk
import datetime, os, re, sys

# Configuração inicial 
ctk.set_appearance_mode("Dark")  # Modo de aparência (System, Dark, Light)
ctk.set_default_color_theme("blue")  # Tema de cores padrão

def salvar_operador():
    nome = entrada_nome.get()
    matricula = entrada_matricula.get()
    senha = entrada_senha.get()
    turno = turno_var.get()
    data_cadastro = entrada_data_cadastro.get()
    data_inativo = entrada_data_inativo.get()

    if all([nome, matricula, senha, turno, data_cadastro, data_inativo]):
        print(f"Operador cadastrado: {nome}, Matrícula: {matricula}, Turno: {turno}, Cadastro: {data_cadastro}, Inativo: {data_inativo}")
        label_mensagem.configure(text="Operador cadastrado com sucesso!", text_color="blue")
    else:
        label_mensagem.configure(text="Preencha todos os campos obrigatórios!", text_color="red")

def formatar_data(event, entry):
    texto = entry.get().replace("/", "")
    novo_texto = ""

    # Obtém o ano atual do sistema 
    ano_atual = datetime.datetime.now().year

    # Limita a entrada a no máximo 8 dígitos numéricos
    texto = texto[:8]

    for i, char in enumerate(texto):
        if i in [2, 4]:
            novo_texto += "/"
        novo_texto += char
    
    entry.delete(0, "end")
    entry.insert(0, novo_texto)

    # Validação da data
    if len(texto) == 8:
        try:
            dia, mes, ano = int(texto[:2]), int(texto[2:4]) , int(texto[4:])

            if ano > ano_atual:
                raise ValueError("Ano inválido")
            
            datetime.date(ano, mes, dia) # Tenta criar uma data válida
            label_mensagem.configure(text="", text_color="red")

        except ValueError:
            label_mensagem.configure(text="Data Inválida! Insira um valor correto.", text_color="red")
                
# Iniciar aplicação após login
def iniciar_aplicacao():
    global entrada_nome, entrada_matricula, entrada_senha, turno_var, entrada_data_cadastro, entrada_data_inativo, label_mensagem
    
    def atualizar_programa(event=None):
        """Reinicia a aplicação executanto novamente o script."""
        python = sys.executable # Caminho do interpretador Python
        os.execv(python, [python] + sys.argv) # Reinicia o programa

    def alternar_visibilidade_senha():
        if entrada_senha.cget("show") == "*":
            entrada_senha.configure(show="") # Mostra a senha
            botao_senha.configure(text="🔒")
        else:
            entrada_senha.configure(show="*")
            botao_senha.configure(text="🔓")

    # Janela principal
    janela = ctk.CTk()
    janela.title("Receitas")
    janela.geometry("1155x784")
    janela.resizable(False, False)

    # Associando a tecla F5 para atualizar
    janela.bind("<F5>", atualizar_programa)

    # Tabview
    tabview = ctk.CTkTabview(janela)
    tabview.pack(expand=True, fill="both", padx=10, pady=10)
    tabview._segmented_button.configure(font=("Arial", 15, "bold"))

    # Abas
    tab_operador = tabview.add("Operador")
    tab_insumos = tabview.add("Insumos")
    tab_cor = tabview.add("Cor")
    tab_artigos = tabview.add("Artigos")

    # Aba Operadores
    # Criar um frame para os botões na parte superior
    frame_botoes = ctk.CTkFrame(tab_operador, fg_color="transparent")
    frame_botoes.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes = ctk.CTkFrame(frame_botoes)
    frame_acoes.pack(pady=5)

    # Criar os botões
    botao_novo = ctk.CTkButton(frame_acoes, text="Novo", font=("Arial", 25, "bold"), width=100)
    botao_alterar = ctk.CTkButton(frame_acoes, text="Alterar", font=("Arial", 25, "bold"), width=100)
    botao_cancelar = ctk.CTkButton(frame_acoes, text="Cancelar", font=("Arial", 25, "bold"), width=100)
    botao_excluir = ctk.CTkButton(frame_acoes, text="Excluir", font=("Arial", 25, "bold"), width=100)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo.pack(side="left", padx=5)
    botao_alterar.pack(side="left", padx=5)
    botao_cancelar.pack(side="left", padx=5)
    botao_excluir.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar = ctk.CTkFrame(frame_botoes)
    frame_pesquisar.pack()

    entrada_pesquisar = ctk.CTkEntry(frame_pesquisar, width=305, placeholder_text="Pesquisar Matrícula", font=("Arial", 15))
    botao_pesquisar = ctk.CTkButton(frame_pesquisar, text="Pesquisar", font=("Arial", 25, "bold"), width=100)

    entrada_pesquisar.pack(side="left", padx=5)
    botao_pesquisar.pack(side="left", padx=5)                

    frame_conteudo = ctk.CTkFrame(tab_operador)
    frame_conteudo.pack(expand=True, fill="both", padx=10, pady=10)

    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    campos = ["Nome:", "Matrícula:", "Senha:", "Data Cadastro:", "Data Inativo:"]
    
    entradas = {}
    for i, texto in enumerate(campos):
        label = ctk.CTkLabel(frame_conteudo, text=texto, font=("Arial", 35, "bold"))
        label.grid(row=i, column=0, sticky="w", padx=10, pady=15)

        if texto == "Senha:":
            # Criando um frame para agrupar o campo de senha e o botão
            frame_senha = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
            frame_senha.grid(row=i, column=1, sticky="w", padx=10, pady=5)

            # Criando o campo de senha dentro do frame
            entrada_senha = ctk.CTkEntry(frame_senha, show="*", width=600, height=40)
            entrada_senha.pack(side="left", fill="both", expand=True)

            # Criando o botão dentro do mesmo frame (ao lado direito)
            botao_senha = ctk.CTkButton(frame_senha, text="🔒", width=40, height=40, command=alternar_visibilidade_senha)
            botao_senha.pack(side="right", padx=(5, 0))

            entradas[texto] = entrada_senha        
        
        elif texto in ["Data Cadastro:", "Data Inativo:"]:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=40, placeholder_text="DD/MM/AA")
            entrada.bind("<KeyRelease>", lambda event, e=entrada: formatar_data(event, e))
            entradas[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)
        else:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=40)
            entradas[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)

    entrada_nome = entradas["Nome:"]
    entrada_matricula = entradas["Matrícula:"]
    entrada_senha = entradas["Senha:"]
    entrada_data_cadastro = entradas["Data Cadastro:"]
    entrada_data_inativo = entradas["Data Inativo:"]

    # Turno (botões de seleção)
    turno_var = ctk.StringVar(value="Manhã")  

    label_turno = ctk.CTkLabel(frame_conteudo, text="Turno:", font=("Arial", 35, "bold"))
    label_turno.grid(row=len(campos)+1, column=0, sticky="w", padx=10, pady=5)

    frame_turno = ctk.CTkFrame(frame_conteudo)
    frame_turno.grid(row=len(campos)+1, column=1, sticky="w", padx=10, pady=5)

    turno_manha = ctk.CTkRadioButton(frame_turno, text="Manhã", font=("Arial", 30, "bold"), variable=turno_var, value="Manhã")
    turno_tarde = ctk.CTkRadioButton(frame_turno, text="Tarde", font=("Arial", 30, "bold"), variable=turno_var, value="Tarde")
    turno_noite = ctk.CTkRadioButton(frame_turno, text="Noite", font=("Arial", 30, "bold"), variable=turno_var, value="Noite")

    turno_manha.pack(side="left", padx=15)
    turno_tarde.pack(side="left", padx=15)
    turno_noite.pack(side="left", padx=15)

    # Frame para o botão "salvar"
    frame_salvar = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_salvar.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew")

    # Botão para salvar
    botao_salvar = ctk.CTkButton(frame_salvar, text="Salvar", font=("Arial", 35, "bold"))
    botao_salvar.pack(padx=10, pady=10)
    
    # Mensagem de feedback
    label_mensagem = ctk.CTkLabel(frame_salvar, text="", text_color="red")
    label_mensagem.pack()
    
    # Funções para os botões
    def novo_operador():
        print("Novo operador")

    def alterar_operador():
        print("Alterar operador")

    def cancelar_operador():
        print("Cancelar operação")

    def excluir_operador():
        print("Excluir operador")

    def pesquisar_operador():
        matricula = entrada_matricula.get()
        print(f"Pesquisar operador com matrícula: {matricula}")

    # Aba Insumos
    # Criar um frame para os botões na parte superior
    frame_botoes = ctk.CTkFrame(tab_insumos, fg_color="transparent")
    frame_botoes.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes = ctk.CTkFrame(frame_botoes)
    frame_acoes.pack(pady=5)

    # Criar os botões
    botao_novo = ctk.CTkButton(frame_acoes, text="Novo", font=("Arial", 25, "bold"), width=100)
    botao_alterar = ctk.CTkButton(frame_acoes, text="Alterar", font=("Arial", 25, "bold"), width=100)
    botao_cancelar = ctk.CTkButton(frame_acoes, text="Cancelar", font=("Arial", 25, "bold"), width=100)
    botao_excluir = ctk.CTkButton(frame_acoes, text="Excluir", font=("Arial", 25, "bold"), width=100)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo.pack(side="left", padx=5)
    botao_alterar.pack(side="left", padx=5)
    botao_cancelar.pack(side="left", padx=5)
    botao_excluir.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar = ctk.CTkFrame(frame_botoes)
    frame_pesquisar.pack()

    entrada_pesquisar = ctk.CTkEntry(frame_pesquisar, width=305, placeholder_text="Pesquisar Código", font=("Arial", 15))
    botao_pesquisar = ctk.CTkButton(frame_pesquisar, text="Pesquisar", font=("Arial", 25, "bold"), width=100)

    entrada_pesquisar.pack(side="left", padx=5)
    botao_pesquisar.pack(side="left", padx=5)                

    frame_conteudo = ctk.CTkFrame(tab_insumos)
    frame_conteudo.pack(expand=True, fill="both", padx=10, pady=10)

    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    campos = ["Descrição:", "Tipo:", "Data Cadastro:", "Data Inativo:", "Preço de Custo:", "Quantidade do Estoque:"]
    entradas = {}

    # Estado para controlar a visibilidade do menu
    menu_aberto = False

    # Função para selecionar uma opção
    def selecionar_opcao(opcao):
        entrada_tipo.configure(state="normal")
        entrada_tipo.delete(0, "end")
        entrada_tipo.insert(0, opcao)
        entrada_tipo.configure(state="readonly")
        toggle_menu()  # Fecha o menu após a seleção

    # Função para abrir/fechar o menu suspenso (toggle)
    def toggle_menu():
        nonlocal menu_aberto
        if menu_aberto:
            frame_opcoes.place_forget()
            menu_aberto = False
        else:
            entrada_tipo.update_idletasks()
            x = entrada_tipo.winfo_rootx() - frame_conteudo.winfo_rootx()
            y = entrada_tipo.winfo_rooty() - frame_conteudo.winfo_rooty() + entrada_tipo.winfo_height()
            frame_opcoes.place(x=x, y=y)
            frame_opcoes.lift()  # Traz o menu para frente, sobre os demais widgets
            menu_aberto = True

    for i, texto in enumerate(campos):
        label = ctk.CTkLabel(frame_conteudo, text=texto, font=("Arial", 35, "bold"))
        label.grid(row=i, column=0, sticky="w", padx=10, pady=15)
        
        if texto == "Tipo:":
            frame_tipo = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
            frame_tipo.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            
             # Campo "Tipo" (não editável)
            entrada_tipo = ctk.CTkEntry(frame_tipo, width=600, height=40, placeholder_text="Corante") 
            entrada_tipo.pack(side="left", fill="both", expand=True)

            # Botão para abrir/fechar o menu suspenso
            botao_tipo = ctk.CTkButton(frame_tipo, text="▼", width=40, height=40, command=toggle_menu)
            botao_tipo.pack(side="right", padx=(5, 0))

            # Frame do menu suspenso (inicia oculto)
            frame_opcoes = ctk.CTkFrame(frame_conteudo, width=600) 
            frame_opcoes.place_forget()

            # Opções do menu suspenso
            opcoes = ["Líquido", "Pó", "Gel"]
            for opcao in opcoes:
                botao_opcao = ctk.CTkButton(frame_opcoes, text=opcao, command=lambda o=opcao: selecionar_opcao(o))
                botao_opcao.pack(fill="x", pady=2)

        elif texto == "Preço de Custo:":
            # Função para formatar o preço em "R$ 0,00"
            def formatar_preco(event, entrada):
                texto = re.sub(r"[^\d]", "", entrada.get()) # Remove tudo que não é digito
                if texto:
                    valor = int(texto) / 100
                    entrada.delete(0, "end")
                    entrada.insert(0, f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) # Formato BRL

            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=40)
            entrada.bind("<KeyRelease>", lambda event, e=entrada: formatar_preco(event, e))
            entradas[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)

        elif texto in ["Data Cadastro:", "Data Inativo:"]:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=40, placeholder_text="DD/MM/AA")
            entrada.bind("<KeyRelease>", lambda event, e=entrada: formatar_data(event, e))
            entradas[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)

        else:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=40)
            entradas[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)

    # Frame para o botão "salvar"
    frame_salvar = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_salvar.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew")

    # Botão para salvar
    botao_salvar = ctk.CTkButton(frame_salvar, text="Salvar", font=("Arial", 35, "bold"))
    botao_salvar.pack(padx=10, pady=10)
    
    # Mensagem de feedback
    label_mensagem = ctk.CTkLabel(frame_salvar, text="", text_color="red")
    label_mensagem.pack()
    
    # Aba Cores
    label_cor = ctk.CTkLabel(tab_cor, text="Cadastro de Cores", font=("Arial", 16))
    label_cor.pack(pady=20)

    # Aba Artigos
    # Criar um frame para os botões na parte superior
    frame_botoes = ctk.CTkFrame(tab_artigos, fg_color="transparent")
    frame_botoes.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes = ctk.CTkFrame(frame_botoes)
    frame_acoes.pack(pady=5)

    # Criar os botões
    botao_novo = ctk.CTkButton(frame_acoes, text="Novo", font=("Arial", 25, "bold"), width=100)
    botao_alterar = ctk.CTkButton(frame_acoes, text="Alterar", font=("Arial", 25, "bold"), width=100)
    botao_cancelar = ctk.CTkButton(frame_acoes, text="Cancelar", font=("Arial", 25, "bold"), width=100)
    botao_excluir = ctk.CTkButton(frame_acoes, text="Excluir", font=("Arial", 25, "bold"), width=100)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo.pack(side="left", padx=5)
    botao_alterar.pack(side="left", padx=5)
    botao_cancelar.pack(side="left", padx=5)
    botao_excluir.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar = ctk.CTkFrame(frame_botoes)
    frame_pesquisar.pack()

    entrada_pesquisar = ctk.CTkEntry(frame_pesquisar, width=305, placeholder_text="Pesquisar Artigo", font=("Arial", 15))
    botao_pesquisar = ctk.CTkButton(frame_pesquisar, text="Pesquisar", font=("Arial", 25, "bold"), width=100)

    entrada_pesquisar.pack(side="left", padx=5)
    botao_pesquisar.pack(side="left", padx=5)                

    frame_conteudo = ctk.CTkFrame(tab_artigos)
    frame_conteudo.pack(expand=True, fill="both", padx=10, pady=10)

    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    campos = ["Descrição:", "Data Cadastro:", "Data Inativo:"]
    entradas = {}

    for i, texto in enumerate(campos):
        label = ctk.CTkLabel(frame_conteudo, text=texto, font=("Arial", 35, "bold"))
        label.grid(row=i+1, column=0, sticky="w", padx=10, pady=15)
        
        if texto in ["Data Cadastro:", "Data Inativo:"]:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=40, placeholder_text="DD/MM/AA")
            entrada.bind("<KeyRelease>", lambda event, e=entrada: formatar_data(event, e))
            entradas[texto] = entrada
            entrada.grid(row=i+1, column=1, sticky="w", padx=10, pady=5)
        else:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=40)
            entradas[texto] = entrada
            entrada.grid(row=i+1, column=1, sticky="w", padx=10, pady=5)

    # Frame para o botão "salvar"
    frame_salvar = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_salvar.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew")

    # Botão para salvar
    botao_salvar = ctk.CTkButton(frame_salvar, text="Salvar", font=("Arial", 35, "bold"))
    botao_salvar.pack(padx=10, pady=10)
    
    # Mensagem de feedback
    label_mensagem = ctk.CTkLabel(frame_salvar, text="", text_color="red")
    label_mensagem.pack()
    
    # Executar Aplicação
    janela.mainloop()

# Função de autenticação
def autenticar():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    if usuario == "" and senha == "":
        login_janela.destroy()
        iniciar_aplicacao()
    else:
        label_erro.configure(text="Usuário ou senha incorretos")

# Login
login_janela = ctk.CTk()
login_janela.title("Login")
login_janela.geometry("500x400")  # Tamanho da janela de login
login_janela.eval('tk::PlaceWindow . center')  # Centraliza a janela

label_usuario = ctk.CTkLabel(login_janela, text="Usuário:")
label_usuario.pack(pady=5)
entrada_usuario = ctk.CTkEntry(login_janela)
entrada_usuario.pack(pady=5)

label_senha = ctk.CTkLabel(login_janela, text="Senha:")
label_senha.pack(pady=5)
entrada_senha = ctk.CTkEntry(login_janela, show="*")
entrada_senha.pack(pady=5)

botao_login = ctk.CTkButton(login_janela, text="Entrar", command=autenticar)
botao_login.pack(pady=10)

label_erro = ctk.CTkLabel(login_janela, text="", text_color="red")
label_erro.pack()

login_janela.mainloop()