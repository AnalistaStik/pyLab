from datetime import datetime
import re, pyodbc

def permitir_somente_numeros(entrada):
    # Remove caracteres especiais e formata a data
    texto = re.sub(r"[^0-9]", "", entrada)
    return texto   

def formatar_com_barras(texto):
    novo_texto = ""
    for i, char in enumerate(texto):
        if i in [2, 4]:
            novo_texto += "/"
        novo_texto += char
    return novo_texto

def validar_data(texto, label_mensagem):
    # Espera-se que texto seja uma string com 6 dígitos: DDMMYY
    if len(texto) != 6 or not texto.isdigit():
        mostrar_mensagem_temporaria(label_mensagem, "Data inválida", "red")
        return False

    dia, mes, ano = int(texto[:2]), int(texto[2:4]), int(texto[4:])
    ano_atual = datetime.now().year % 100  # Dois últimos dígitos do ano atual

    # Verifica se mês e dia estão em intervalos válidos
    if not (1 <= mes <= 12):
        mostrar_mensagem_temporaria(label_mensagem, "Mês inválido", "red")
        return False
    if not (1 <= dia <= 31):
        mostrar_mensagem_temporaria(label_mensagem, "Dia inválido", "red")
        return False
    if ano > ano_atual:
        mostrar_mensagem_temporaria(label_mensagem, "Ano inválido", "red")
        return False

    # Verifica se a data é válida (ex: 30/02/23 não existe)
    try:
        datetime(2000 + ano, mes, dia)  # Considera anos 2000+
        return True
    except ValueError:
        mostrar_mensagem_temporaria(label_mensagem, "Data inválida", "red")
        return False

def formatar_data(event, entrada, label_mensagem):
    texto = permitir_somente_numeros(entrada.get())
    texto = texto[:6]
    entrada.delete(0, "end")
    texto_formatado = formatar_com_barras(texto)
    entrada.insert(0, texto_formatado)

    if len(texto) == 6:
        if not validar_data(texto, label_mensagem):
            entrada.delete(0, "end")
    else:
        label_mensagem.configure(text="", text_color="red")

def mostrar_mensagem_temporaria(label, texto, cor="blue", tempo=3000):
    """Mostra uma mensagem temporária em um label."""
    label.configure(text=texto, text_color=cor)
    label.after(tempo, lambda: label.configure(text=""))

def alternar_visibilidade_senha(entrada_senha, botao_senha):
    if entrada_senha.cget("show") == "*":
        entrada_senha.configure(show="") # Mostra a senha
        botao_senha.configure(text="🔒")
    else:
        entrada_senha.configure(show="*")
        botao_senha.configure(text="🔓")

def formatar_com_apenas_numeros(event, entrada):
    texto = entrada.get()
    apenas_numeros = permitir_somente_numeros(texto)
    entrada.delete(0, "end")
    entrada.insert(0, apenas_numeros)


def fazer_conexao_sql_server():
    # Configurações de conexão
    server = '168.190.30.2'
    database = 'Laboratorio'
    username = 'sa'
    password = 'Stik0123'

    # Conexão com o banco de dados
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    return conn