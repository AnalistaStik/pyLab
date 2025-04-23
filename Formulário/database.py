import pyodbc, time
print(pyodbc.drivers())
# class Database:
#     def __init__(self):
#         self.conn = None
#         self.create_connection()

#     def create_connection(self): 
#         server = "168.190.30.2"
#         database = "Teste_Gabriel"
#         username = "sa"
#         password = "Stik0123"

#         connection_string = (
#             f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};'
#             f'UID={username};PWD={password}'
#         )

#         try:
#             self.conn = pyodbc.connect(connection_string)
#             print("Conexão Estabelecida!")
#         except pyodbc.Error as e:
#             print(f'Erro ao conectar ao banco de dados: {str(e)}')
    
#     def close_connection(self):
#         if self.conn:
#             self.conn.close()
#             print("Conexão fechada.")

# db = Database()

# input("Pressione Enter para fechar a conexão...\n")

# db.close_connection()