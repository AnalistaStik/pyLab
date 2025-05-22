import os, re, sys, pyodbc, pyodbc
from datetime import datetime
from Uteis import mostrar_mensagem_temporaria, alternar_visibilidade_senha,formatar_data, formatar_com_apenas_numeros, fazer_conexao_sql_server

if getattr(sys, "frozen", False):
    sys.path.append(os.path.join(sys._MEIPASS, "customtkinter"))

import customtkinter as ctk

# Configuração inicial 
ctk.set_appearance_mode("Dark")  # Modo de aparência (System, Dark, Light)
ctk.set_default_color_theme("dark-blue")  # Tema de cores padrão
    
# Iniciar aplicação após login
def iniciar_aplicacao():
    global label_mensagem, entradas
# Função para buscar o operador no banco de dados
    def buscar_operador():    
        try:
            campo_pesquisa = entrada_pesquisar_op.get().strip()             

            conn = fazer_conexao_sql_server()
            cursor = conn.cursor()

            query = "SELECT * FROM TbOper WHERE Matricula = ?"
            cursor.execute(query, (campo_pesquisa,))
            resultado = cursor.fetchone()

            if resultado:
                mostrar_mensagem_temporaria(label_mensagem_op, "Operador encontrado.", "blue")
                dados_pesquisados_operador(resultado)

                # Verifica se os botões já existem antes de criar
                if not hasattr(buscar_operador, "botao_alterar_op") or not buscar_operador.botao_alterar_op.winfo_ismapped():
                    # Remove os botões "Alterar" e "Excluir" apenas se eles existirem
                    buscar_operador.botao_alterar_op = ctk.CTkButton(frame_acoes_op, text="Alterar", font=("Arial", 20, "bold"), width=100, command=alterar_operador)
                    buscar_operador.botao_alterar_op.pack(side="left", padx=5)

                if not hasattr(buscar_operador, "botao_excluir_op") or not buscar_operador.botao_excluir_op.winfo_ismapped():
                    buscar_operador.botao_excluir_op = ctk.CTkButton(frame_acoes_op, text="Excluir", font=("Arial", 20, "bold"), width=100)
                    buscar_operador.botao_excluir_op.pack(side="left", padx=5)
                
                if botao_salvar_op.winfo_ismapped():
                    botao_salvar_op.pack_forget()
            else:
                mostrar_mensagem_temporaria(label_mensagem_op, "Nenhum operador encontrado.", "red")

            conn.close()

        except pyodbc.Error as e:
            mostrar_mensagem_temporaria(label_mensagem_op, "Erro ao pesquisar operador.", "red")
            print(str(e))

    def alterar_operador():
        for entrada in entradas_op.values():
            entrada.configure(state="normal")
        for botao in turnos_botoes.values():
            botao.configure(state="normal")
        botao_senha.configure(state="normal")
        mostrar_mensagem_temporaria(label_mensagem_op, "Campos prontos para serem alterados.", "blue") 
        
# Função que preenche os campos com os dados do operador encontrado
    def dados_pesquisados_operador(resultado):
        
        entradas_op["Matrícula:"].delete(0, "end")
        entradas_op["Matrícula:"].insert(0, resultado[1])

        entradas_op["Nome:"].delete(0, "end")
        entradas_op["Nome:"].insert(0, resultado[2])

        entrada_senha.configure(show="*") # Mantém a senha oculta
        entradas_op["Senha:"].delete(0, "end")
        entradas_op["Senha:"].insert(0, resultado[3])

        entradas_op["Data Cadastro:"].delete(0, "end")
        entradas_op["Data Cadastro:"].insert(0, resultado[4].strftime("%d/%m/%y") if resultado[4] else "")

        entradas_op["Data Inativo:"].delete(0, "end")
        entradas_op["Data Inativo:"].insert(0, resultado[5].strftime("%d/%m/%y") if resultado[5] else "")

        # Mapear o turno de volta para string
        turno_valor = int(resultado[6]) if resultado[6] is not None else None

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
            entrada_senha.configure(show="*") # Mantém a senha oculta
        for botao in turnos_botoes.values():
            botao.configure(state="disabled") # Desabilita os botões de turno após a pesquisa
        botao_senha.configure(state="disabled") # Desabilita o botão de senha após a pesquisa

    def atualizar_programa(event=None):
        """Reinicia a aplicação executanto novamente o script."""
        python = sys.executable # Caminho do interpretador Python
        os.execv(python, [python] + sys.argv) # Reinicia o programa

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
    tab_insumos = tabview.add("Cadastro")
    
    # Aba Operadores
    def limpa_campos_operador():
        for campo, entrada in entradas_op.items():
            janela.focus()
            entrada.configure(state="normal")  # Habilita os campos para edição
            entrada.delete(0, "end")
            
            if campo == "Data Cadastro:" or campo == "Data Inativo:":
                entrada.configure(placeholder_text="DD/MM/AA")
            else:
                entrada.configure(placeholder_text="Digite aqui...")    

        for botao in turnos_botoes.values():
            botao.configure(state="normal")  # Habilita os botões de turno para edição    
        botao_senha.configure(state="normal")  # Habilita o botão de senha para edição
        turno_var.set("Manhã")  # Reseta o valor do botão de opção  
        label_mensagem_op.configure(text="", text_color="red")  # Limpa mensagens de erro ou sucesso
        entrada_pesquisar_op.delete(0, "end")  # Limpa o campo de pesquisa
        entrada_pesquisar_op.configure(placeholder_text="Pesquisar Matrícula")  # Reseta o placeholder

        # Remove os botões "Alterar" e "Excluir" apenas se eles existirem
        if hasattr(buscar_operador, "botao_alterar_op") and buscar_operador.botao_alterar_op.winfo_ismapped():
            buscar_operador.botao_alterar_op.pack_forget()
        if hasattr(buscar_operador, "botao_excluir_op") and buscar_operador.botao_excluir_op.winfo_ismapped():
            buscar_operador.botao_excluir_op.pack_forget()
        if not botao_salvar_op.winfo_ismapped():
            botao_salvar_op.pack(pady=10, padx=10) 
            
    # Criar um frame para os botões na parte superior
    frame_botoes_op = ctk.CTkFrame(tab_operador, fg_color="transparent")
    frame_botoes_op.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes_op = ctk.CTkFrame(frame_botoes_op)
    frame_acoes_op.pack(pady=5)

    # Criar os botões
    botao_novo_op = ctk.CTkButton(frame_acoes_op, text="Novo", font=("Arial", 20, "bold"), width=100, command=limpa_campos_operador) 
    botao_cancelar_op = ctk.CTkButton(frame_acoes_op, text="Cancelar", font=("Arial", 20, "bold"), width=100, command=limpa_campos_operador)
    
    # Posicionar os botões no frame_acoes lado a lado
    botao_novo_op.pack(side="left", padx=5)
    botao_cancelar_op.pack(side="left", padx=5)

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
            entrada_senha.bind("<KeyRelease>", lambda event: formatar_com_apenas_numeros(event, entrada_senha))

            # Criando o botão dentro do mesmo frame (ao lado direito)
            botao_senha = ctk.CTkButton(frame_senha, text="🔒", width=40, height=30)
            botao_senha.pack(side="right", padx=(5, 0))
            botao_senha.configure(command=lambda: alternar_visibilidade_senha(entrada_senha, botao_senha))

            entradas_op[texto] = entrada_senha      

        elif texto in ["Data Cadastro:", "Data Inativo:"]:
            entrada_data = ctk.CTkEntry(frame_conteudo_op, width=600, height=30, placeholder_text="DD/MM/AA")
            entrada_data.bind("<KeyRelease>", lambda event, e=entrada_data: formatar_data(event, e, label_mensagem_op))
            entradas_op[texto] = entrada_data
            entrada_data.grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
        elif texto == "Matrícula:":
            entrada_matricula = ctk.CTkEntry(frame_conteudo_op, width=600, height=30, placeholder_text="Digite aqui...")
            entrada_matricula.bind("<KeyRelease>", lambda event: formatar_com_apenas_numeros(event, entrada_matricula))
            entradas_op[texto] = entrada_matricula
            entrada_matricula.grid(row=i, column=1, sticky="w", padx=10, pady=5)
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
            conn = fazer_conexao_sql_server()
            cursor = conn.cursor()

            # Conversões de tipo
            try:
                matricula = int(matricula) if matricula else None  # Converte para INT se não estiver vazio
            except ValueError:
                mostrar_mensagem_temporaria(label_mensagem_op, "Erro: Matricula deve ser um número inteiro.", "red")

            try:
                data_cadastro = datetime.strptime(data_cadastro, "%d/%m/%y").date() if data_cadastro else None
                data_inativo = datetime.strptime(data_inativo, "%d/%m/%y").date() if data_inativo else None
            except ValueError:
                mostrar_mensagem_temporaria(label_mensagem_op, "Erro: Data deve estar no formato DD/MM/AA.", "red")

            # Se o botão "Alterar" estiver visível, atualiza os dados
            if hasattr(buscar_operador, "botao_alterar_op") and buscar_operador.botao_alterar_op.winfo_ismapped():
                query = """
                        UPDATE TbOper 
                        SET NmDesc = ?, Senha = ?, DtCadastro = ?, DtInativo = ?, Turno = ?
                        WHERE Matricula = ?"""
                try:    
                    cursor.execute(query, (nome, senha, data_cadastro, data_inativo, turno_int, matricula))
                    conn.commit()
                    mostrar_mensagem_temporaria(label_mensagem_op, "Operador atualizado", "blue")
                except pyodbc.Error as e:
                    mostrar_mensagem_temporaria(label_mensagem_op, "Erro ao atualizar operador", "red")
                    print(str(e))
            else:
                # Query SQL para inserir dados
                query = """
                        INSERT INTO TbOper (Matricula, NmDesc, Senha, DtCadastro, DtInativo, Turno)
                        VALUES (?, ?, ?, ?, ?, ?)"""

            # Executar a query
            cursor.execute(query, (matricula, nome, senha, data_cadastro, data_inativo, turno_int))
            conn.commit()

            mostrar_mensagem_temporaria(label_mensagem_op, "Operador registrado", "blue")

            for campo, entrada in entradas_op.items():
                entrada.delete(0, "end")  # Limpa os campos após o cadastro
                entrada.configure(placeholder_text="DD/MM/AA") if campo == "Data Cadastro:" or campo == "Data Inativo:" else entrada.configure(placeholder_text="Digite aqui...")
            
            turno_var.set("Manhã")  # Reseta o valor do botão de opção

        except pyodbc.Error as e:
            mostrar_mensagem_temporaria(label_mensagem_op, "Erro ao inserir operador", "red")
            print(str(e))

    frame_salvar_op = ctk.CTkFrame(frame_conteudo_op, fg_color="transparent")
    frame_salvar_op.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew")

    # Label para mensagens de sucesso ou erro
    label_mensagem_op = ctk.CTkLabel(frame_salvar_op, text="", font=("Arial", 20))
    label_mensagem_op.pack(pady=10)

    botao_salvar_op = ctk.CTkButton(frame_salvar_op, text="Salvar", font=("Arial", 35, "bold"), 
                                 command=lambda: salvar_operador(entradas_op, turno_var, label_mensagem_op))
    botao_salvar_op.pack(pady=10, padx=10)  

    # Aba Cadastro
    def buscar_cadastro():
        try:
            campo_pesquisa = entrada_pesquisar_in.get().strip()
            tipo_selecionado = entradas_in["Tipo:"].get().strip()

            if not campo_pesquisa or not tipo_selecionado:
                mostrar_mensagem_temporaria(label_mensagem_in, "Informe a descrição e selecione o tipo.", "red")
                return

            # Define a tabela conforme o tipo selecionado
            tabela_dict = {"Corante": "TbCorante", "Cor": "TbCor", "Artigo": "TbArtigo"}
            tabela = tabela_dict.get(tipo_selecionado)
            if not tabela:
                mostrar_mensagem_temporaria(label_mensagem_in, "Tipo inválido.", "red")
                return

            conn = fazer_conexao_sql_server()
            cursor = conn.cursor()
            query = f"SELECT * FROM {tabela} WHERE NmDesc = ?"
            cursor.execute(query, (campo_pesquisa,))
            resultado = cursor.fetchone()

            if resultado:
                mostrar_mensagem_temporaria(label_mensagem_in, "Cadastro encontrado.", "blue")
                dados_pesquisados_cadastro(resultado)

                # Verifica se os botões já existem antes de criar
                if not hasattr(buscar_cadastro, "botao_alterar_in") or not buscar_cadastro.botao_alterar_in.winfo_ismapped():
                    # Remove os botões "Alterar" e "Excluir" apenas se eles existirem
                    buscar_cadastro.botao_alterar_in = ctk.CTkButton(frame_acoes_in, text="Alterar", font=("Arial", 20, "bold"), width=100)
                    buscar_cadastro.botao_alterar_in.pack(side="left", padx=5)
                if not hasattr(buscar_cadastro, "botao_excluir_in") or not buscar_cadastro.botao_excluir_in.winfo_ismapped():
                    buscar_cadastro.botao_excluir_in = ctk.CTkButton(frame_acoes_in, text="Excluir", font=("Arial", 20, "bold"), width=100)
                    buscar_cadastro.botao_excluir_in.pack(side="left", padx=5)
                if botao_salvar_in.winfo_ismapped():
                    botao_salvar_in.pack_forget()
            else:
                mostrar_mensagem_temporaria(label_mensagem_in, "Nenhum cadastro encontrado.", "red")
            conn.close()
       
        except pyodbc.Error as e:
            mostrar_mensagem_temporaria(label_mensagem_in, "Erro ao pesquisar cadastro.", "red")
            print(str(e)) 
    
    def dados_pesquisados_cadastro(resultado):
        tipo_selecionado = entradas_in["Tipo:"].get().strip()
        
        entradas_in["Descrição:"].delete(0, "end")
        entradas_in["Descrição:"].insert(0, resultado[1])

        entradas_in["Data Cadastro:"].delete(0, "end")
        entradas_in["Data Cadastro:"].insert(0, resultado[2].strftime("%d/%m/%y") if resultado[2] else "")

        entradas_in["Data Inativo:"].delete(0, "end")
        entradas_in["Data Inativo:"].insert(0, resultado[3].strftime("%d/%m/%y") if resultado[3] else "")

        # Se for Corante, preenche o campo G/L
        if tipo_selecionado == "Corante" and "G/L:" in entradas_in:
            entradas_in["G/L:"].delete(0, "end")
            entradas_in["G/L:"].insert(0, str(resultado[4]) if resultado[4] is not None else "")
        
        for entrada in entradas_in.values():
            entrada.configure(state="disabled")

    def limpa_campos_cadastro():
        if "G/L:" in entradas_in:
            entradas_in["G/L:"].grid_forget()
            entradas_in["G/L_label"].grid_forget()
            del entradas_in["G/L:"]
            del entradas_in["G/L_label"]
       
        for campo, entrada in entradas_in.items():
            janela.focus()
            entrada.configure(state="normal") # Habilita os campos para edição
            entrada.delete(0, "end")
            
            if "Tipo:" in campo:    
                entrada.configure(placeholder_text="Selecione um tipo")
                entrada.configure(state="readonly")
                
            elif "Data Cadastro:" or "Data Inativo:" in campo:
                entrada.configure(placeholder_text="DD/MM/AA") 
            else:
                entrada.configure(placeholder_text="Digite aqui...")
        entrada_pesquisar_in.delete(0, "end")  # Limpa o campo de pesquisa
        entrada_pesquisar_in.configure(placeholder_text="Pesquisar Descrição")  # Reseta o placeholder

        if hasattr(buscar_cadastro, "botao_alterar_in") and buscar_cadastro.botao_alterar_in.winfo_ismapped():
            buscar_cadastro.botao_alterar_in.pack_forget()
        if hasattr(buscar_cadastro, "botao_excluir_in") and buscar_cadastro.botao_excluir_in.winfo_ismapped():
            buscar_cadastro.botao_excluir_in.pack_forget()
        if not botao_salvar_in.winfo_ismapped():
            botao_salvar_in.pack(pady=10, padx=10)

    # Criar um frame para os botões na parte superior
    frame_botoes_in = ctk.CTkFrame(tab_insumos, fg_color="transparent")
    frame_botoes_in.pack(pady=10, fill="x")

    # Criar um subframe para os botões principais
    frame_acoes_in = ctk.CTkFrame(frame_botoes_in)
    frame_acoes_in.pack(pady=5)

    # Criar os botões
    botao_novo_in = ctk.CTkButton(frame_acoes_in, text="Novo", font=("Arial", 20, "bold"), width=100, command=limpa_campos_cadastro)
    botao_cancelar_in = ctk.CTkButton(frame_acoes_in, text="Cancelar", font=("Arial", 20, "bold"), width=100, command=limpa_campos_cadastro)

    # Posicionar os botões no frame_acoes lado a lado
    botao_novo_in.pack(side="left", padx=5)
    botao_cancelar_in.pack(side="left", padx=5)

    # Criar input de pesquisa
    frame_pesquisar_in = ctk.CTkFrame(frame_botoes_in)
    frame_pesquisar_in.pack()

    entrada_pesquisar_in = ctk.CTkEntry(frame_pesquisar_in, width=305, placeholder_text="Pesquisar Descrição", font=("Arial", 15))
    botao_pesquisar_in = ctk.CTkButton(frame_pesquisar_in, text="Pesquisar", font=("Arial", 20, "bold"), width=100, command=buscar_cadastro)

    entrada_pesquisar_in.pack(side="left", padx=5)
    botao_pesquisar_in.pack(side="left", padx=5)                

    frame_conteudo_in = ctk.CTkFrame(tab_insumos)
    frame_conteudo_in.pack(expand=True, fill="both", padx=10, pady=10)

    # Garante que o frame_conteudo se expanda por toda a tela
    frame_conteudo_in.grid_rowconfigure(999, weight=1)  # Expansão vertical
    frame_conteudo_in.grid_columnconfigure(1, weight=1)  # Expansão horizontal

    campos_in = ["Descrição:", "Tipo:", "Data Cadastro:", "Data Inativo:"]
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

        if opcao == "Corante":
            # Adiciona um novo label e input para "G/L:"
            if "G/L:" not in entradas_in:
                def formatar_campo_gl(event, entrada_gl):
                    texto = entrada_gl.get()

                    # Remove tudo que não é número ou vírgula
                    texto_limpo = re.sub(r"[^\d,]", "", texto)

                    # Substitui vírgula por ponto para converter
                    try:
                        valor = float(texto_limpo.replace(",", "."))
                        valor_formatado = f"{valor:.4f}".replace(".", ",")  # Volta para vírgula
                    except ValueError:
                        valor_formatado = ""

                    entrada_gl.delete(0, "end")
                    entrada_gl.insert(0, valor_formatado)

                label_gl = ctk.CTkLabel(frame_conteudo_in, text="G/L:", font=("Arial", 20, "bold"))
                label_gl.grid(row=4, column=0, sticky="w", padx=10, pady=15)

                entrada_gl = ctk.CTkEntry(frame_conteudo_in, width=600, height=30, placeholder_text="Digite aqui...")
                entrada_gl.bind("<KeyRelease>", lambda event, e=entrada_gl: formatar_campo_gl(event, e))
                entrada_gl.grid(row=4, column=1, sticky="w", padx=10, pady=5)

                entradas_in["G/L:"] = entrada_gl
                entradas_in["G/L_label"] = label_gl                
        else:
            # Remove o label e input "G/L:" se a opção não for "Corante"
            if "G/L:" in entradas_in:
                entradas_in["G/L:"].grid_forget()
                entradas_in["G/L_label"].grid_forget()
                del entradas_in["G/L:"]
                del entradas_in["G/L_label"]

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
            entrada_tipo = ctk.CTkEntry(frame_tipo, width=600, height=30, placeholder_text="Selecione um tipo") 
            entrada_tipo.pack(side="left", fill="both", expand=True)
            entrada_tipo.configure(state="readonly")  # Torna o campo não editável

            # Botão para abrir/fechar o menu suspenso
            botao_tipo = ctk.CTkButton(frame_tipo, text="▼", width=40, height=30, command=toggle_menu)
            botao_tipo.pack(side="right", padx=(5, 0))

            # Frame do menu suspenso (inicia oculto)
            frame_opcoes = ctk.CTkFrame(frame_conteudo_in, width=600) 
            frame_opcoes.place_forget()

            entradas_in[texto] = entrada_tipo

            # Opções do menu suspenso
            opcoes = ["Corante", "Cor", "Artigo"]
            for opcao in opcoes:
                botao_opcao = ctk.CTkButton(frame_opcoes, text=opcao, command=lambda o=opcao: selecionar_opcao(o))
                botao_opcao.pack(fill="x", pady=2)

        elif texto in ["Data Cadastro:", "Data Inativo:"]:
            entrada_in = ctk.CTkEntry(frame_conteudo_in, width=600, height=30, placeholder_text="DD/MM/AA")
            entrada_in.bind("<KeyRelease>", lambda event, e=entrada_in: formatar_data(event, e, label_mensagem_in))
            entradas_in[texto] = entrada_in
            entrada_in.grid(row=i, column=1, sticky="w", padx=10, pady=5)

        else:
            entrada_in = ctk.CTkEntry(frame_conteudo_in, width=600, height=30, placeholder_text="Digite aqui...")
            entradas_in[texto] = entrada_in
            entrada_in.grid(row=i, column=1, sticky="w", padx=10, pady=5)

    def salvar_cadastro(entradas_in, label_mensagem_in):
        try:
            # Obter valores dos campos de entrada
            descricao = entradas_in["Descrição:"].get().strip()
            data_cadastro = entradas_in["Data Cadastro:"].get().strip()
            data_inativo = entradas_in["Data Inativo:"].get().strip()

            tipo_selecionado = entradas_in["Tipo:"].get()
            tipo_dict = {"Corante": 1, "Cor": 2, "Artigo": 3}
            tipo_int = tipo_dict.get(tipo_selecionado, 0) # Obtém o número do tipo
            
            # Verifica se o campo "G/L:" existe e obtém seu valor
            gl = entradas_in["G/L:"].get().strip() if "G/L:" in entradas_in else None
            if gl:
                try:
                    gl = int(gl) if gl else None  # Converte para INT se não estiver vazio
                except ValueError:
                    mostrar_mensagem_temporaria(label_mensagem_in, "Erro: G/L deve ser um número inteiro.", "red")
            else:
                gl = None

            # Conversões de tipo
            try:
                data_cadastro = datetime.strptime(data_cadastro, "%d/%m/%y").date() if data_cadastro else None
                data_inativo = datetime.strptime(data_inativo, "%d/%m/%y").date() if data_inativo else None
            except ValueError:
                mostrar_mensagem_temporaria(label_mensagem_in, "Erro: Data deve estar no formato DD/MM/AA.", "red")

            # Criar conexão com o banco de dados
            conn = fazer_conexao_sql_server()
            cursor = conn.cursor()

            # Query SQL para inserir dados
            if tipo_int == 1:
                query = """
                        INSERT INTO TbCorante (NmDesc, DtCadastro, DtInativo, GramaLitro)
                        VALUES (?, ?, ?, ?)"""
                cursor.execute(query, (descricao, data_cadastro, data_inativo, gl))
                conn.commit()
            if tipo_int == 2:
                query = """
                        INSERT INTO TbCor (NmDesc, DtCadastro, DtInativo)
                        VALUES (?, ?, ?)"""
                cursor.execute(query, (descricao, data_cadastro, data_inativo))
                conn.commit()
            if tipo_int == 3:
                query = """
                        INSERT INTO TbArtigo (NmDesc, DtCadastro, DtInativo)
                        VALUES (?, ?, ?)"""
                cursor.execute(query, (descricao, data_cadastro, data_inativo))
                conn.commit()
            mostrar_mensagem_temporaria(label_mensagem_in, "Cadastro registrado", "blue")
        except pyodbc.Error as e:
            mostrar_mensagem_temporaria(label_mensagem_in, "Erro ao inserir cadastro", "red")
            print(str(e))
        
        for campo, entrada in entradas_in.items():
            janela.focus()
            entrada.delete(0, "end")

            if "Tipo:" in campo:
                entrada.configure(placeholder_text="Selecione um tipo")
                entrada.configure(state="readonly")
            elif "Data Cadastro:" or "Data Inativo:" in campo:
                entrada.configure(placeholder_text="DD/MM/AA")
            else:
                entrada.configure(placeholder_text="Digite aqui...")

    frame_salvar_in = ctk.CTkFrame(frame_conteudo_in, fg_color="transparent")
    frame_salvar_in.grid(row=999, column=0, columnspan=2, pady=20, sticky="sew")

    # Label para mensagens de sucesso ou erro
    label_mensagem_in = ctk.CTkLabel(frame_salvar_in, text="", font=("Arial", 20))
    label_mensagem_in.pack(pady=10)

    botao_salvar_in = ctk.CTkButton(frame_salvar_in, text="Salvar", font=("Arial", 35, "bold"),
                                  command=lambda: salvar_cadastro(entradas_in, label_mensagem_in))
    botao_salvar_in.pack(pady=10, padx=10)        
        
    # Executar Aplicação
    janela.mainloop()

iniciar_aplicacao()
    
# # Função de autenticação
# def autenticar():
#     usuario = entrada_usuario.get()
#     senha = entrada_senha.get()
#     if usuario == "" and senha == "":
#         login_janela.destroy()
#         iniciar_aplicacao()
#     else:
#         label_erro.configure(text="Usuário ou senha incorretos")

# # Login
# login_janela = ctk.CTk()
# login_janela.title("Login")
# login_janela.geometry("500x400")  # Tamanho da janela de login
# login_janela.eval('tk::PlaceWindow . center')  # Centraliza a janela

# label_usuario = ctk.CTkLabel(login_janela, text="Usuário:")
# label_usuario.pack(pady=5)
# entrada_usuario = ctk.CTkEntry(login_janela)
# entrada_usuario.pack(pady=5)

# label_senha = ctk.CTkLabel(login_janela, text="Senha:")
# label_senha.pack(pady=5)
# entrada_senha = ctk.CTkEntry(login_janela, show="*")
# entrada_senha.pack(pady=5)

# botao_login = ctk.CTkButton(login_janela, text="Entrar", command=autenticar)
# botao_login.pack(pady=10)

# label_erro = ctk.CTkLabel(login_janela, text="", text_color="red")
# label_erro.pack()

# login_janela.mainloop()