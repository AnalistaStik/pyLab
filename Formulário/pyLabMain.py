import os, re, sys, subprocess, pyodbc, pyodbc
from datetime import datetime

if getattr(sys, "frozen", False):
    sys.path.append(os.path.join(sys._MEIPASS, "customtkinter"))

import customtkinter as ctk

# Configuração inicial 
ctk.set_appearance_mode("Dark")  # Modo de aparência (System, Dark, Light)
ctk.set_default_color_theme("blue")  # Tema de cores padrão



def formatar_data(event, entry, label_mensagem):
    texto = entry.get().replace("/", "")
    novo_texto = ""

    # Obtém o ano atual do sistema 
    ano_atual = datetime.now().year

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
            
            datetime(ano, mes, dia).date() # Tenta criar uma data válida
            label_mensagem.configure(text="", text_color="red")

        except ValueError:
            label_mensagem.configure(text="Data Inválida! Insira um valor correto.", text_color="red")
         
# def atualizar_sistema():
#     hora_atual = datetime.now()
#     # Atualiza o sistema baixando a última versão do Github.
#     diretorio_projeto = os.path.dirname(os.path.abspath(__file__))

#     # Verifica se o diretório é um repositório Git
#     if os.path.exists(os.path.join(diretorio_projeto, ".git")):
#         try:
#             if hora_atual.hour == 12:
#                 # Puxa as últimas alterações do repositório
#                 subprocess.run(["git", "pull"], cwd=diretorio_projeto, check=True)
#                 print("Sistema atualizado com sucesso! Reiniciando...")

#                 # Reinicia o programa apoós a atualização
#                 python_exe = os.path.basename(os.sys.executable)
#                 os.execl(python_exe, python_exe, *os.sys.argv)
#             else:
#                 print("Uma nova versão está disponivel, o programa será atualizado ás 12:00. Não desligue o computador.")
#         except subprocess.CalledProcessError as e:
#             print("Erro ao atualizar", e)
#     else:
#         print("Este programa não está dentro de um repositório Git.")
    
# Iniciar aplicação após login
def iniciar_aplicacao():
    global label_mensagem, entradas
# Função para buscar o operador no banco de dados
    def buscar_operador():    
        try:
            campo_pesquisa = entrada_pesquisar_op.get().strip()             

            conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};SERVER=168.190.30.2;DATABASE=Teste_Gabriel;UID=sa;PWD=Stik0123"
            )
            cursor = conn.cursor()

            query = "SELECT * FROM Operador WHERE ID = ?"
            cursor.execute(query, (campo_pesquisa,))
            resultado = cursor.fetchone()

            if resultado:
                label_mensagem_op.configure(text="Operador encontrado.", text_color="blue")
                dados_pesquisados_operador(resultado)
            else:
                label_mensagem_op.configure(text="Nenhum operador encontrado.", text_color="red")

            conn.close()

        except pyodbc.Error as e:
            label_mensagem_op.configure(text="Erro ao pesquisar operador.", text_color="red")
            print(str(e))

# Função que preenche os campos com os dados do operador encontrado
    def dados_pesquisados_operador(resultado):
        for entrada in entradas_op.values():
            entrada.configure(state="normal")  # Habilita os campos após a pesquisa
        for botao in turnos_botoes.values():
            botao.configure(state="normal") # Habilita os botões de turno após a pesquisa
        
        entradas_op["Matrícula:"].delete(0, "end")
        entradas_op["Matrícula:"].insert(0, resultado[0])

        entradas_op["Nome:"].delete(0, "end")
        entradas_op["Nome:"].insert(0, resultado[1])

        entradas_op["Senha:"].delete(0, "end")
        entradas_op["Senha:"].insert(0, resultado[2])

        entradas_op["Data Cadastro:"].delete(0, "end")
        entradas_op["Data Cadastro:"].insert(0, resultado[3].strftime("%d/%m/%y") if resultado[3] else "")

        entradas_op["Data Inativo:"].delete(0, "end")
        entradas_op["Data Inativo:"].insert(0, resultado[4].strftime("%d/%m/%y") if resultado[4] else "")

        # Mapear o turno de volta para string
        turno_valor = int(resultado[5]) if resultado[5] is not None else None

        if turno_valor == 1:
            turno_var.set("Manhã")
        elif turno_valor == 2:
            turno_var.set("Tarde")
        elif turno_valor == 3:
            turno_var.set("Noite")
        else:
            turno_var.set("")  # caso o valor não exista

        for entrada in entradas_op.values():
            entrada.configure(state="disabled")  # Desabilita os campos após a pesquisa
        for botao in turnos_botoes.values():
            botao.configure(state="disabled") # Desabilita os botões de turno após a pesquisa
        botao_senha.configure(state="disabled") # Desabilita o botão de senha após a pesquisa

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
    janela.geometry("974x816")
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
    def novo_operador():
        for campo, entrada in entradas_op.items():
            entrada.configure(state="normal") # Habilita os campos para edição
            entrada.delete(0, "end")
            if "Data" in campo:
                entrada.configure(placeholder_text="DD/MM/AA")
            else:
                entrada.configure(placeholder_text="Digite aqui...")    
       
        for botao in turnos_botoes.values():
            botao.configure(state="normal") # Habilita os botões de turno para edição    
        botao_senha.configure(state="normal") # Habilita o botão de senha para edição
        turno_var.set("Manhã")  # Reseta o valor do botão de opção  
        label_mensagem_op.configure(text="", text_color="red") # Limpa mensagens de erro ou sucesso


    # Criar um frame para os botões na parte superior
    frame_botoes_op = ctk.CTkFrame(tab_operador, fg_color="transparent")
    frame_botoes_op.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes_op = ctk.CTkFrame(frame_botoes_op)
    frame_acoes_op.pack(pady=5)

    # Criar os botões
    botao_novo_op = ctk.CTkButton(frame_acoes_op, text="Novo", font=("Arial", 20, "bold"), width=100, command=novo_operador) 
    botao_alterar_op = ctk.CTkButton(frame_acoes_op, text="Alterar", font=("Arial", 20, "bold"), width=100)
    botao_cancelar_op = ctk.CTkButton(frame_acoes_op, text="Cancelar", font=("Arial", 20, "bold"), width=100)
    botao_excluir_op = ctk.CTkButton(frame_acoes_op, text="Excluir", font=("Arial", 20, "bold"), width=100)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo_op.pack(side="left", padx=5)
    botao_alterar_op.pack(side="left", padx=5)
    botao_cancelar_op.pack(side="left", padx=5)
    botao_excluir_op.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar_op = ctk.CTkFrame(frame_botoes_op)
    frame_pesquisar_op.pack()

    entrada_pesquisar_op = ctk.CTkEntry(frame_pesquisar_op, width=305, placeholder_text="Pesquisar Matrícula", font=("Arial", 15))
    botao_pesquisar_op = ctk.CTkButton(frame_pesquisar_op, text="Pesquisar", font=("Arial", 20, "bold"), width=100,
                                        command=buscar_operador)

    entrada_pesquisar_op.pack(side="left", padx=5)
    botao_pesquisar_op.pack(side="left", padx=5)                
    
    frame_conteudo_op = ctk.CTkFrame(tab_operador)
    frame_conteudo_op.pack(expand=True, fill="both", padx=10, pady=10)

    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo_op.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo_op.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    campos_op = ["Matrícula:", "Nome:", "Senha:", "Data Cadastro:", "Data Inativo:"]
    
    entradas_op = {}
    for i, texto in enumerate(campos_op):
        label = ctk.CTkLabel(frame_conteudo_op, text=texto, font=("Arial", 20, "bold"))
        label.grid(row=i, column=0, sticky="w", padx=10, pady=15)

        if texto == "Senha:":
            # Criando um frame para agrupar o campo de senha e o botão
            frame_senha = ctk.CTkFrame(frame_conteudo_op, fg_color="transparent")
            frame_senha.grid(row=i, column=1, sticky="w", padx=10, pady=5)

            # Criando o campo de senha dentro do frame
            entrada_senha = ctk.CTkEntry(frame_senha, show="*", width=600, height=30, placeholder_text="Digite aqui...")
            entrada_senha.pack(side="left", fill="both", expand=True)

            # Criando o botão dentro do mesmo frame (ao lado direito)
            botao_senha = ctk.CTkButton(frame_senha, text="🔒", width=40, height=30, command=alternar_visibilidade_senha)
            botao_senha.pack(side="right", padx=(5, 0))

            entradas_op[texto] = entrada_senha        
        
        elif texto in ["Data Cadastro:", "Data Inativo:"]:
            entrada = ctk.CTkEntry(frame_conteudo_op, width=600, height=30, placeholder_text="DD/MM/AA")
            entrada.bind("<KeyRelease>", lambda event, e=entrada: formatar_data(event, e, label_mensagem_op))
            entradas_op[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)
        else:
            entrada = ctk.CTkEntry(frame_conteudo_op, width=600, height=30, placeholder_text="Digite aqui...")
            entradas_op[texto] = entrada
            entrada.grid(row=i, column=1, sticky="w", padx=10, pady=5)
   
    # Turno (botões de seleção)
    turno_var = ctk.StringVar(value="Manhã")  

    label_turno = ctk.CTkLabel(frame_conteudo_op, text="Turno:", font=("Arial", 20, "bold"))
    label_turno.grid(row=len(campos_op)+1, column=0, sticky="w", padx=10, pady=5)

    frame_turno = ctk.CTkFrame(frame_conteudo_op, fg_color="transparent")
    frame_turno.grid(row=len(campos_op)+1, column=1, sticky="w", padx=10, pady=5)

    turnos_botoes = {
        "Manhã": ctk.CTkRadioButton(frame_turno, text="Manhã", font=("Arial", 20, "bold"), variable=turno_var, value="Manhã"),
        "Tarde": ctk.CTkRadioButton(frame_turno, text="Tarde", font=("Arial", 20, "bold"), variable=turno_var, value="Tarde"),
        "Noite": ctk.CTkRadioButton(frame_turno, text="Noite", font=("Arial", 20, "bold"), variable=turno_var, value="Noite")
    }

    for botao in turnos_botoes.values():
        botao.pack(side="left", padx=15)

    def salvar_operador(entradas_op, turno_var, label_mensagem_op):
        """Salva os dados do operador no banco de dados."""
        try:
            # Obter valores dos campos de entrada
            matricula = entradas_op["Matrícula:"].get().strip()
            nome = entradas_op["Nome:"].get().strip()
            senha = entradas_op["Senha:"].get().strip()
            data_cadastro = entradas_op["Data Cadastro:"].get().strip()
            data_inativo = entradas_op["Data Inativo:"].get().strip()

            turno_selecionado = turno_var.get()
            turno_dict = {"Manhã": 1, "Tarde": 2, "Noite": 3}
            turno_int = turno_dict.get(turno_selecionado, 0) # Obtém o número do turno
            
            # Criar conexão com o banco de dados
            conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};SERVER=168.190.30.2;DATABASE=Teste_Gabriel;UID=sa;PWD=Stik0123"
            )
            cursor = conn.cursor()

            # Conversões de tipo
            try:
                matricula = int(matricula) if matricula else None  # Converte para INT se não estiver vazio
            except ValueError:
                label_mensagem_op.configure(text="Erro: Matricula deve ser um número inteiro.", text_color="red")

            try:
                data_cadastro = datetime.strptime(data_cadastro, "%d/%m/%y").date() if data_cadastro else None
                data_inativo = datetime.strptime(data_inativo, "%d/%m/%y").date() if data_inativo else None
            except ValueError:
                label_mensagem_op.configure(text="Erro: Data deve estar no formato DD/MM/AA.", text_color="red")

            # Query SQL para inserir dados
            query = """
                    INSERT INTO Operador (ID, Descricao, Senha, DataCadastro, DataInativo, Turno)
                    VALUES (?, ?, ?, ?, ?, ?)"""

            # Executar a query
            cursor.execute(query, (matricula, nome, senha, data_cadastro, data_inativo, turno_int))
            conn.commit()

            label_mensagem_op.configure(text="Operador registrado", text_color="blue")

        except pyodbc.Error as e:
            label_mensagem_op.configure(text=f"Erro ao inserir operador", text_color="red")
            print(str(e))


    frame_salvar_op = ctk.CTkFrame(frame_conteudo_op, fg_color="transparent")
    frame_salvar_op.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew")

    # Label para mensagens de sucesso ou erro
    label_mensagem_op = ctk.CTkLabel(frame_salvar_op, text="", font=("Arial", 20))
    label_mensagem_op.pack(pady=10)

    botao_salvar_op = ctk.CTkButton(frame_salvar_op, text="Salvar", font=("Arial", 35, "bold"), 
                                 command=lambda: salvar_operador(entradas_op, turno_var, label_mensagem_op))
    botao_salvar_op.pack(pady=10, padx=10)  

    # Aba Insumos
    # Criar um frame para os botões na parte superior
    frame_botoes_in = ctk.CTkFrame(tab_insumos, fg_color="transparent")
    frame_botoes_in.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes_in = ctk.CTkFrame(frame_botoes_in)
    frame_acoes_in.pack(pady=5)

    # Criar os botões
    botao_novo_in = ctk.CTkButton(frame_acoes_in, text="Novo", font=("Arial", 20, "bold"), width=100)
    botao_alterar_in = ctk.CTkButton(frame_acoes_in, text="Alterar", font=("Arial", 20, "bold"), width=100)
    botao_cancelar_in = ctk.CTkButton(frame_acoes_in, text="Cancelar", font=("Arial", 20, "bold"), width=100)
    botao_excluir_in = ctk.CTkButton(frame_acoes_in, text="Excluir", font=("Arial", 20, "bold"), width=100)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo_in.pack(side="left", padx=5)
    botao_alterar_in.pack(side="left", padx=5)
    botao_cancelar_in.pack(side="left", padx=5)
    botao_excluir_in.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar_in = ctk.CTkFrame(frame_botoes_in)
    frame_pesquisar_in.pack()

    entrada_pesquisar_in = ctk.CTkEntry(frame_pesquisar_in, width=305, placeholder_text="Pesquisar Código", font=("Arial", 15))
    botao_pesquisar_in = ctk.CTkButton(frame_pesquisar_in, text="Pesquisar", font=("Arial", 20, "bold"), width=100)

    entrada_pesquisar_in.pack(side="left", padx=5)
    botao_pesquisar_in.pack(side="left", padx=5)                

    frame_conteudo_in = ctk.CTkFrame(tab_insumos)
    frame_conteudo_in.pack(expand=True, fill="both", padx=10, pady=10)

    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo_in.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo_in.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    campos_in = ["Descrição:", "Tipo:", "Data Cadastro:", "Data Inativo:", "Preço de Custo:", "Quantidade do Estoque:"]
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
            x = entrada_tipo.winfo_rootx() - frame_conteudo_in.winfo_rootx()
            y = entrada_tipo.winfo_rooty() - frame_conteudo_in.winfo_rooty() + entrada_tipo.winfo_height()
            frame_opcoes.place(x=x, y=y)
            frame_opcoes.lift()  # Traz o menu para frente, sobre os demais widgets
            menu_aberto = True

    for i, texto in enumerate(campos_in):
        label_in = ctk.CTkLabel(frame_conteudo_in, text=texto, font=("Arial", 20, "bold"))
        label_in.grid(row=i, column=0, sticky="w", padx=10, pady=15)
        
        if texto == "Tipo:":
            frame_tipo = ctk.CTkFrame(frame_conteudo_in, fg_color="transparent")
            frame_tipo.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            
             # Campo "Tipo" (não editável)
            entrada_tipo = ctk.CTkEntry(frame_tipo, width=600, height=30, placeholder_text="Corante") 
            entrada_tipo.pack(side="left", fill="both", expand=True)

            # Botão para abrir/fechar o menu suspenso
            botao_tipo = ctk.CTkButton(frame_tipo, text="▼", width=40, height=30, command=toggle_menu)
            botao_tipo.pack(side="right", padx=(5, 0))

            # Frame do menu suspenso (inicia oculto)
            frame_opcoes = ctk.CTkFrame(frame_conteudo_in, width=600) 
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

            entrada_in = ctk.CTkEntry(frame_conteudo_in, width=600, height=30, placeholder_text="R$:")
            entrada_in.bind("<KeyRelease>", lambda event, e=entrada_in: formatar_preco(event, e))
            entradas_in[texto] = entrada_in
            entrada_in.grid(row=i, column=1, sticky="w", padx=10, pady=5)

        elif texto in ["Data Cadastro:", "Data Inativo:"]:
            entrada_in = ctk.CTkEntry(frame_conteudo_in, width=600, height=30, placeholder_text="DD/MM/AA")
            entrada_in.bind("<KeyRelease>", lambda event, e=entrada_in: formatar_data(event, e, label_mensagem_in))
            entradas_in[texto] = entrada_in
            entrada_in.grid(row=i, column=1, sticky="w", padx=10, pady=5)

        else:
            entrada_in = ctk.CTkEntry(frame_conteudo_in, width=600, height=30, placeholder_text="Digite aqui...")
            entradas_in[texto] = entrada_in
            entrada_in.grid(row=i, column=1, sticky="w", padx=10, pady=5)

        
    frame_salvar_in = ctk.CTkFrame(frame_conteudo_in, fg_color="transparent")
    frame_salvar_in.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew")

    # Label para mensagens de sucesso ou erro
    label_mensagem_in = ctk.CTkLabel(frame_salvar_in, text="", font=("Arial", 20))
    label_mensagem_in.pack(pady=10)

    botao_salvar_in = ctk.CTkButton(frame_salvar_in, text="Salvar", font=("Arial", 35, "bold"),
                                  command=lambda: salvar_operador(entradas_in, label_mensagem_in))
    botao_salvar_in.pack(pady=10, padx=10)        
        
    # Aba Cores
    # Criar um frame para os botões na parte superior
    frame_botoes_cor = ctk.CTkFrame(tab_cor, fg_color="transparent")
    frame_botoes_cor.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes_cor = ctk.CTkFrame(frame_botoes_cor)
    frame_acoes_cor.pack(pady=5)

    # Criar os botões
    botao_novo_cor = ctk.CTkButton(frame_acoes_cor, text="Novo", font=("Arial", 20, "bold"), width=100)
    botao_alterar_cor = ctk.CTkButton(frame_acoes_cor, text="Alterar", font=("Arial", 20, "bold"), width=100)
    botao_cancelar_cor = ctk.CTkButton(frame_acoes_cor, text="Cancelar", font=("Arial", 20, "bold"), width=100)
    botao_excluir_cor = ctk.CTkButton(frame_acoes_cor, text="Excluir", font=("Arial", 20, "bold"), width=100)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo_cor.pack(side="left", padx=5)
    botao_alterar_cor.pack(side="left", padx=5)
    botao_cancelar_cor.pack(side="left", padx=5)
    botao_excluir_cor.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar_cor = ctk.CTkFrame(frame_botoes_cor)
    frame_pesquisar_cor.pack()

    entrada_pesquisar_cor = ctk.CTkEntry(frame_pesquisar_cor, width=305, placeholder_text="Pesquisar Cor", font=("Arial", 15))
    botao_pesquisar_cor = ctk.CTkButton(frame_pesquisar_cor, text="Pesquisar", font=("Arial", 20, "bold"), width=100)

    entrada_pesquisar_cor.pack(side="left", padx=5)
    botao_pesquisar_cor.pack(side="left", padx=5)                
        
    # Criação dos subframes, todos ainda vinculados ao tab_cor
    frame_conteudo_cor = ctk.CTkFrame(tab_cor)
    frame_conteudo_cor.pack(expand=True, fill="both", padx=10, pady=10)

    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo_cor.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo_cor.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    frame_linha_unica = ctk.CTkFrame(frame_conteudo_cor, fg_color="transparent")
    frame_linha_unica.grid(row=0, column=0, sticky="sew", padx=10)

    frame_paralelo = ctk.CTkFrame(frame_conteudo_cor, fg_color="transparent")
    frame_paralelo.grid(row=1, column=0, sticky="sew", padx=10)

    frame_ultimo = ctk.CTkFrame(frame_conteudo_cor, fg_color="transparent")
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

    label_cor = ctk.CTkLabel(frame_linha_unica, text="Descrição:", font=("Arial", 20, "bold"))
    label_cor.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    entrada_cor = ctk.CTkEntry(frame_linha_unica, width=600, height=30, placeholder_text="Digite aqui...")
    entrada_cor.grid(row=0, column=1, sticky="w", padx=50, pady=5)
    entradas_cor["Descrição"] = entrada_cor

    # Adicionando campos paralelos
    row_index = 0
    for i, linha in enumerate(campos_paralelos_cor):
        for j, texto in enumerate(linha):
            label_cor = ctk.CTkLabel(frame_paralelo, text=texto, font=("Arial", 20, "bold"))
            label_cor.grid(row=row_index, column=j * 2, sticky="w", padx=10, pady=5)
            
            entrada_cor = ctk.CTkEntry(frame_paralelo, width=370, height=30, placeholder_text="Digite aqui...")
            entrada_cor.grid(row=row_index + 1, column=j * 2, sticky="w", padx=10, pady=5)
            entradas_cor[texto] = entrada_cor
    
        row_index += 2  # Incrementar para manter espaço entre linhas
    
    # Adicionando campos de linha única
    for i, linha in enumerate(campos_cor):
        if len(linha) == 1:
            texto = linha[0]
            label_cor = ctk.CTkLabel(frame_ultimo, text=texto, font=("Arial", 20, "bold"))
            label_cor.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            
            largura = 600
            placeholder = "DD/MM/AA" if "Data" in texto else "Digite aqui..."
            
            entrada_cor = ctk.CTkEntry(frame_ultimo, width=largura, height=30, placeholder_text=placeholder)
            if "Data" in texto:
                entrada_cor.bind("<KeyRelease>", lambda event, e=entrada_cor: formatar_data(event, e, label_mensagem_cor))
            
            entrada_cor.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            entradas_cor[texto] = entrada_cor

    frame_salvar_cor = ctk.CTkFrame(frame_conteudo_cor, fg_color="transparent")
    frame_salvar_cor.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew"),

    # Label para mensagens de sucesso ou erro
    label_mensagem_cor = ctk.CTkLabel(frame_salvar_cor, text="", font=("Arial", 20))
    label_mensagem_cor.pack(pady=10)
 
    # botao_salvar_cor = ctk.CTkButton(frame_salvar_cor, text="Salvar", font=("Arial", 35, "bold"),
    #                               command=lambda: salvar_dados(entradas_cor, label_mensagem_cor))
    # botao_salvar_cor.pack(pady=10, padx=10)        
   
    # Aba Artigos
    # Criar um frame para os botões na parte superior
    frame_botoes_art = ctk.CTkFrame(tab_artigos, fg_color="transparent")
    frame_botoes_art.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes_art = ctk.CTkFrame(frame_botoes_art)
    frame_acoes_art.pack(pady=5)

    # Criar os botões
    botao_novo_art = ctk.CTkButton(frame_acoes_art, text="Novo", font=("Arial", 20, "bold"), width=100)
    botao_alterar_art = ctk.CTkButton(frame_acoes_art, text="Alterar", font=("Arial", 20, "bold"), width=100)
    botao_cancelar_art = ctk.CTkButton(frame_acoes_art, text="Cancelar", font=("Arial", 20, "bold"), width=100)
    botao_excluir_art = ctk.CTkButton(frame_acoes_art, text="Excluir", font=("Arial", 20, "bold"), width=100)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo_art.pack(side="left", padx=5)
    botao_alterar_art.pack(side="left", padx=5)
    botao_cancelar_art.pack(side="left", padx=5)
    botao_excluir_art.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar_art = ctk.CTkFrame(frame_botoes_art)
    frame_pesquisar_art.pack()

    entrada_pesquisar_art = ctk.CTkEntry(frame_pesquisar_art, width=305, placeholder_text="Pesquisar Artigo", font=("Arial", 15))
    botao_pesquisar_art = ctk.CTkButton(frame_pesquisar_art, text="Pesquisar", font=("Arial", 20, "bold"), width=100)

    entrada_pesquisar_art.pack(side="left", padx=5)
    botao_pesquisar_art.pack(side="left", padx=5)                

    frame_conteudo_art = ctk.CTkFrame(tab_artigos)
    frame_conteudo_art.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo_art.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo_art.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    campos_art = ["Descrição:", "Data Cadastro:", "Data Inativo:"]
    entradas_art = {}

    for i, texto in enumerate(campos_art):
        label_art = ctk.CTkLabel(frame_conteudo_art, text=texto, font=("Arial", 20, "bold"))
        label_art.grid(row=i+1, column=0, sticky="w", padx=10, pady=15)
        
        if texto in ["Data Cadastro:", "Data Inativo:"]:
            entrada_art = ctk.CTkEntry(frame_conteudo_art, width=600, height=30, placeholder_text="DD/MM/AA")
            entrada_art.bind("<KeyRelease>", lambda event, e=entrada_art: formatar_data(event, e, label_mensagem_art))
            entradas_art[texto] = entrada_art
            entrada_art.grid(row=i+1, column=1, sticky="w", padx=10, pady=5)
        else:
            entrada_art = ctk.CTkEntry(frame_conteudo_art, width=600, height=30, placeholder_text="Digite aqui...")
            entradas_art[texto] = entrada_art
            entrada_art.grid(row=i+1, column=1, sticky="w", padx=10, pady=5)

    # Frame para o botão "salvar"
    frame_salvar_art = ctk.CTkFrame(frame_conteudo_art, fg_color="transparent")
    frame_salvar_art.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew")

    # Label para mensagens de sucesso ou erro
    label_mensagem_art = ctk.CTkLabel(frame_salvar_art, text="", font=("Arial", 20))
    label_mensagem_art.pack(pady=10)

    # botao_salvar_art = ctk.CTkButton(frame_salvar_art, text="Salvar", font=("Arial", 35, "bold"),
    #                               command=lambda: salvar_dados(entradas_art, label_mensagem_art))
    # botao_salvar_art.pack(pady=10, padx=10)        

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