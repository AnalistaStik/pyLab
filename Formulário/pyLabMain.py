import customtkinter as ctk
import datetime, os, re, sys

# Configuração inicial 
ctk.set_appearance_mode("Dark")  # Modo de aparência (System, Dark, Light)
ctk.set_default_color_theme("blue")  # Tema de cores padrão

def salvar_dados(entradas, label_mensagem):
    if not entradas:
        return 
    
    dados = {campo: entrada.get().strip() for campo, entrada in entradas.items()}

    campos_vazios = [campo for campo, valor, in dados.items() if not valor]
    if campos_vazios:
        mensagem = f"Preencha todos os campos!"
        cor = "red"
    else:
        print("Dados salvos:")
        for campo, valor in dados.items():
            print(f"{campo}: {valor}")
        mensagem = "Dados salvos com sucesso!"
        cor = "blue"
    
    if label_mensagem:
        label_mensagem.configure(text=mensagem, text_color=cor)

def formatar_data(event, entry, label_mensagem):
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
    global label_mensagem, entradas

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
    botao_novo = ctk.CTkButton(frame_acoes, text="Novo", font=("Arial", 20, "bold"), width=100)
    botao_alterar = ctk.CTkButton(frame_acoes, text="Alterar", font=("Arial", 20, "bold"), width=100)
    botao_cancelar = ctk.CTkButton(frame_acoes, text="Cancelar", font=("Arial", 20, "bold"), width=100)
    botao_excluir = ctk.CTkButton(frame_acoes, text="Excluir", font=("Arial", 20, "bold"), width=100)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo.pack(side="left", padx=5)
    botao_alterar.pack(side="left", padx=5)
    botao_cancelar.pack(side="left", padx=5)
    botao_excluir.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar = ctk.CTkFrame(frame_botoes)
    frame_pesquisar.pack()

    entrada_pesquisar = ctk.CTkEntry(frame_pesquisar, width=305, placeholder_text="Pesquisar Matrícula", font=("Arial", 15))
    botao_pesquisar = ctk.CTkButton(frame_pesquisar, text="Pesquisar", font=("Arial", 20, "bold"), width=100)

    entrada_pesquisar.pack(side="left", padx=5)
    botao_pesquisar.pack(side="left", padx=5)                

    frame_conteudo = ctk.CTkFrame(tab_operador)
    frame_conteudo.pack(expand=True, fill="both", padx=10, pady=10)

    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    campos = ["Nome:", "Matrícula:", "Senha:", "Data Cadastro:", "Data Inativo:"]
    
    entradas_op = {}
    for i, texto in enumerate(campos):
        label = ctk.CTkLabel(frame_conteudo, text=texto, font=("Arial", 20, "bold"))
        label.grid(row=i, column=0, sticky="w", padx=10, pady=15)

        if texto == "Senha:":
            # Criando um frame para agrupar o campo de senha e o botão
            frame_senha = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
            frame_senha.grid(row=i, column=1, sticky="w", padx=10, pady=5)

            # Criando o campo de senha dentro do frame
            entrada_senha = ctk.CTkEntry(frame_senha, show="*", width=600, height=30, placeholder_text="Digite aqui...")
            entrada_senha.pack(side="left", fill="both", expand=True)

            # Criando o botão dentro do mesmo frame (ao lado direito)
            botao_senha = ctk.CTkButton(frame_senha, text="🔒", width=40, height=30, command=alternar_visibilidade_senha)
            botao_senha.pack(side="right", padx=(5, 0))

            entradas_op[texto] = entrada_senha        
        
        elif texto in ["Data Cadastro:", "Data Inativo:"]:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=30, placeholder_text="DD/MM/AA")
            entrada.bind("<KeyRelease>", lambda event, e=entrada: formatar_data(event, e, label_mensagem_op))
            entradas_op[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)
        else:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=30, placeholder_text="Digite aqui...")
            entradas_op[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)
    # Turno (botões de seleção)
    turno_var = ctk.StringVar(value="Manhã")  

    label_turno = ctk.CTkLabel(frame_conteudo, text="Turno:", font=("Arial", 20, "bold"))
    label_turno.grid(row=len(campos)+1, column=0, sticky="w", padx=10, pady=5)

    frame_turno = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_turno.grid(row=len(campos)+1, column=1, sticky="w", padx=10, pady=5)

    turno_manha = ctk.CTkRadioButton(frame_turno, text="Manhã", font=("Arial", 20, "bold"), variable=turno_var, value="Manhã")
    turno_tarde = ctk.CTkRadioButton(frame_turno, text="Tarde", font=("Arial", 20, "bold"), variable=turno_var, value="Tarde")
    turno_noite = ctk.CTkRadioButton(frame_turno, text="Noite", font=("Arial", 20, "bold"), variable=turno_var, value="Noite")

    turno_manha.pack(side="left", padx=15)
    turno_tarde.pack(side="left", padx=15)
    turno_noite.pack(side="left", padx=15)

    frame_salvar_op = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_salvar_op.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew")

    # Label para mensagens de sucesso ou erro
    label_mensagem_op = ctk.CTkLabel(frame_salvar_op, text="", font=("Arial", 20))
    label_mensagem_op.pack(pady=10)

    botao_salvar_op = ctk.CTkButton(frame_salvar_op, text="Salvar", font=("Arial", 35, "bold"), 
                                 command=lambda: salvar_dados(entradas_op, label_mensagem_op))
    botao_salvar_op.pack(pady=10, padx=10)        

    # Aba Insumos
    # Criar um frame para os botões na parte superior
    frame_botoes = ctk.CTkFrame(tab_insumos, fg_color="transparent")
    frame_botoes.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes = ctk.CTkFrame(frame_botoes)
    frame_acoes.pack(pady=5)

    # Criar os botões
    botao_novo = ctk.CTkButton(frame_acoes, text="Novo", font=("Arial", 20, "bold"), width=100)
    botao_alterar = ctk.CTkButton(frame_acoes, text="Alterar", font=("Arial", 20, "bold"), width=100)
    botao_cancelar = ctk.CTkButton(frame_acoes, text="Cancelar", font=("Arial", 20, "bold"), width=100)
    botao_excluir = ctk.CTkButton(frame_acoes, text="Excluir", font=("Arial", 20, "bold"), width=100)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo.pack(side="left", padx=5)
    botao_alterar.pack(side="left", padx=5)
    botao_cancelar.pack(side="left", padx=5)
    botao_excluir.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar = ctk.CTkFrame(frame_botoes)
    frame_pesquisar.pack()

    entrada_pesquisar = ctk.CTkEntry(frame_pesquisar, width=305, placeholder_text="Pesquisar Código", font=("Arial", 15))
    botao_pesquisar = ctk.CTkButton(frame_pesquisar, text="Pesquisar", font=("Arial", 20, "bold"), width=100)

    entrada_pesquisar.pack(side="left", padx=5)
    botao_pesquisar.pack(side="left", padx=5)                

    frame_conteudo = ctk.CTkFrame(tab_insumos)
    frame_conteudo.pack(expand=True, fill="both", padx=10, pady=10)

    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    campos = ["Descrição:", "Tipo:", "Data Cadastro:", "Data Inativo:", "Preço de Custo:", "Quantidade do Estoque:"]
    entradas_in = {}

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
        label = ctk.CTkLabel(frame_conteudo, text=texto, font=("Arial", 20, "bold"))
        label.grid(row=i, column=0, sticky="w", padx=10, pady=15)
        
        if texto == "Tipo:":
            frame_tipo = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
            frame_tipo.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            
             # Campo "Tipo" (não editável)
            entrada_tipo = ctk.CTkEntry(frame_tipo, width=600, height=30, placeholder_text="Corante") 
            entrada_tipo.pack(side="left", fill="both", expand=True)

            # Botão para abrir/fechar o menu suspenso
            botao_tipo = ctk.CTkButton(frame_tipo, text="▼", width=40, height=30, command=toggle_menu)
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

            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=30, placeholder_text="R$:")
            entrada.bind("<KeyRelease>", lambda event, e=entrada: formatar_preco(event, e))
            entradas_in[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)

        elif texto in ["Data Cadastro:", "Data Inativo:"]:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=30, placeholder_text="DD/MM/AA")
            entrada.bind("<KeyRelease>", lambda event, e=entrada: formatar_data(event, e, label_mensagem_in))
            entradas_in[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)

        else:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=30, placeholder_text="Digite aqui...")
            entradas_in[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)

    frame_salvar_in = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_salvar_in.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew")

    # Label para mensagens de sucesso ou erro
    label_mensagem_in = ctk.CTkLabel(frame_salvar_in, text="", font=("Arial", 20))
    label_mensagem_in.pack(pady=10)

    botao_salvar_in = ctk.CTkButton(frame_salvar_in, text="Salvar", font=("Arial", 35, "bold"),
                                  command=lambda: salvar_dados(entradas_in, label_mensagem_in))
    botao_salvar_in.pack(pady=10, padx=10)        
        
    # Aba Cores
    # Criar um frame para os botões na parte superior
    frame_botoes = ctk.CTkFrame(tab_cor, fg_color="transparent")
    frame_botoes.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes = ctk.CTkFrame(frame_botoes)
    frame_acoes.pack(pady=5)

    # Criar os botões
    botao_novo = ctk.CTkButton(frame_acoes, text="Novo", font=("Arial", 20, "bold"), width=100)
    botao_alterar = ctk.CTkButton(frame_acoes, text="Alterar", font=("Arial", 20, "bold"), width=100)
    botao_cancelar = ctk.CTkButton(frame_acoes, text="Cancelar", font=("Arial", 20, "bold"), width=100)
    botao_excluir = ctk.CTkButton(frame_acoes, text="Excluir", font=("Arial", 20, "bold"), width=100)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo.pack(side="left", padx=5)
    botao_alterar.pack(side="left", padx=5)
    botao_cancelar.pack(side="left", padx=5)
    botao_excluir.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar = ctk.CTkFrame(frame_botoes)
    frame_pesquisar.pack()

    entrada_pesquisar = ctk.CTkEntry(frame_pesquisar, width=305, placeholder_text="Pesquisar Cor", font=("Arial", 15))
    botao_pesquisar = ctk.CTkButton(frame_pesquisar, text="Pesquisar", font=("Arial", 20, "bold"), width=100)

    entrada_pesquisar.pack(side="left", padx=5)
    botao_pesquisar.pack(side="left", padx=5)                
        
    # Criação dos subframes, todos ainda vinculados ao tab_cor
    frame_conteudo = ctk.CTkFrame(tab_cor)
    frame_conteudo.pack(expand=True, fill="both", padx=10, pady=10)

    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    frame_linha_unica = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_linha_unica.grid(row=0, column=0, sticky="sew", padx=10)

    frame_paralelo = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_paralelo.grid(row=1, column=0, sticky="sew", padx=10)

    frame_ultimo = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_ultimo.grid(row=2, column=0, sticky="sew", padx=10)

    # Campos
    campos_cor = [
        ("Data Cadastro:",),
        ("Data Inativo:",)
    ]

    # Campos paralelos
    campos_paralelos_cor = [
        ("Corante 01:", "Corante 02:"),  
        ("Gramas:", "Gramas:"), 
        ("Corante 03:", "Corante 04:"), 
        ("Gramas:", "Gramas:"), 
    ]
    entradas_cor = {}

    label = ctk.CTkLabel(frame_linha_unica, text="Descrição:", font=("Arial", 20, "bold"))
    label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    entrada = ctk.CTkEntry(frame_linha_unica, width=600, height=30, placeholder_text="Digite aqui...")
    entrada.grid(row=0, column=1, sticky="w", padx=50, pady=5)
    entradas_cor["Descrição"] = entrada

    # Adicionando campos paralelos
    row_index = 0
    for i, linha in enumerate(campos_paralelos_cor):
        for j, texto in enumerate(linha):
            label = ctk.CTkLabel(frame_paralelo, text=texto, font=("Arial", 20, "bold"))
            label.grid(row=row_index, column=j * 2, sticky="w", padx=10, pady=5)
            
            entrada = ctk.CTkEntry(frame_paralelo, width=370, height=30, placeholder_text="Digite aqui...")
            entrada.grid(row=row_index + 1, column=j * 2, sticky="w", padx=10, pady=5)
            entradas_cor[texto] = entrada
    
        row_index += 2  # Incrementar para manter espaço entre linhas
    
    # Adicionando campos de linha única
    for i, linha in enumerate(campos_cor):
        if len(linha) == 1:
            texto = linha[0]
            label = ctk.CTkLabel(frame_ultimo, text=texto, font=("Arial", 20, "bold"))
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            
            largura = 600
            placeholder = "DD/MM/AA" if "Data" in texto else "Digite aqui..."
            
            entrada = ctk.CTkEntry(frame_ultimo, width=largura, height=30, placeholder_text=placeholder)
            if "Data" in texto:
                entrada.bind("<KeyRelease>", lambda event, e=entrada: formatar_data(event, e, label_mensagem_cor))
            
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            entradas_cor[texto] = entrada

    frame_salvar_cor = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_salvar_cor.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew"),

    # Label para mensagens de sucesso ou erro
    label_mensagem_cor = ctk.CTkLabel(frame_salvar_cor, text="", font=("Arial", 20))
    label_mensagem_cor.pack(pady=10)
 
    botao_salvar_cor = ctk.CTkButton(frame_salvar_cor, text="Salvar", font=("Arial", 35, "bold"),
                                  command=lambda: salvar_dados(entradas_cor, label_mensagem_cor))
    botao_salvar_cor.pack(pady=10, padx=10)        
   
    # Aba Artigos
    # Criar um frame para os botões na parte superior
    frame_botoes = ctk.CTkFrame(tab_artigos, fg_color="transparent")
    frame_botoes.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes = ctk.CTkFrame(frame_botoes)
    frame_acoes.pack(pady=5)

    # Criar os botões
    botao_novo = ctk.CTkButton(frame_acoes, text="Novo", font=("Arial", 20, "bold"), width=100)
    botao_alterar = ctk.CTkButton(frame_acoes, text="Alterar", font=("Arial", 20, "bold"), width=100)
    botao_cancelar = ctk.CTkButton(frame_acoes, text="Cancelar", font=("Arial", 20, "bold"), width=100)
    botao_excluir = ctk.CTkButton(frame_acoes, text="Excluir", font=("Arial", 20, "bold"), width=100)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo.pack(side="left", padx=5)
    botao_alterar.pack(side="left", padx=5)
    botao_cancelar.pack(side="left", padx=5)
    botao_excluir.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar = ctk.CTkFrame(frame_botoes)
    frame_pesquisar.pack()

    entrada_pesquisar = ctk.CTkEntry(frame_pesquisar, width=305, placeholder_text="Pesquisar Artigo", font=("Arial", 15))
    botao_pesquisar = ctk.CTkButton(frame_pesquisar, text="Pesquisar", font=("Arial", 20, "bold"), width=100)

    entrada_pesquisar.pack(side="left", padx=5)
    botao_pesquisar.pack(side="left", padx=5)                

    frame_conteudo = ctk.CTkFrame(tab_artigos)
    frame_conteudo.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    campos = ["Descrição:", "Data Cadastro:", "Data Inativo:"]
    entradas_art = {}

    for i, texto in enumerate(campos):
        label = ctk.CTkLabel(frame_conteudo, text=texto, font=("Arial", 20, "bold"))
        label.grid(row=i+1, column=0, sticky="w", padx=10, pady=15)
        
        if texto in ["Data Cadastro:", "Data Inativo:"]:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=30, placeholder_text="DD/MM/AA")
            entrada.bind("<KeyRelease>", lambda event, e=entrada: formatar_data(event, e, label_mensagem_art))
            entradas_art[texto] = entrada
            entrada.grid(row=i+1, column=1, sticky="w", padx=10, pady=5)
        else:
            entrada = ctk.CTkEntry(frame_conteudo, width=600, height=30, placeholder_text="Digite aqui...")
            entradas_art[texto] = entrada
            entrada.grid(row=i+1, column=1, sticky="w", padx=10, pady=5)

    # Frame para o botão "salvar"
    frame_salvar_art = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_salvar_art.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew")

    # Label para mensagens de sucesso ou erro
    label_mensagem_art = ctk.CTkLabel(frame_salvar_art, text="", font=("Arial", 20))
    label_mensagem_art.pack(pady=10)

    botao_salvar_art = ctk.CTkButton(frame_salvar_art, text="Salvar", font=("Arial", 35, "bold"),
                                  command=lambda: salvar_dados(entradas_art, label_mensagem_art))
    botao_salvar_art.pack(pady=10, padx=10)        

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