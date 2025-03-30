import os
import mysql.connector
import pandas as pd

# Função para conectar ao MySQL
def conectar_mysql():
    conexao = mysql.connector.connect(
        host="localhost",      
        user="root",   
        password="008301456",  
        database="intuitive"   
    )
    return conexao
# Função para criar a tabela
def criar_tabela(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS operadoras (
        id INT AUTO_INCREMENT PRIMARY KEY,
        reg_ans VARCHAR(20) NOT NULL,  # Alterado para 'REG_ANS'
        cnpj VARCHAR(20) NOT NULL,
        razao_social VARCHAR(255) NOT NULL,
        nome_fantasia VARCHAR(255),
        modalidade VARCHAR(100),
        uf VARCHAR(2),
        data_registro DATE
    );
    """)
    conexao.commit()
    cursor.close()
# Função para importar os arquivos CSV e juntar em uma tabela
def importar_csv(conexao, diretorio):
    cursor = conexao.cursor()
    # Criar um DataFrame vazio para juntar todos os CSVs
    todos_dados = pd.DataFrame()
    # Iterar sobre todos os arquivos CSV na pasta
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".csv"):  # Verifica se é um arquivo CSV
            caminho_arquivo = os.path.join(diretorio, arquivo)
            print(f"Juntando os dados do arquivo: {arquivo}")
            # Carregar os dados do CSV para um DataFrame
            df = pd.read_csv(caminho_arquivo, delimiter=";")
            # Imprimir os nomes das colunas para verificar
            print("Colunas no arquivo:", df.columns)
            # Juntar o DataFrame do arquivo atual com o DataFrame total
            todos_dados = pd.concat([todos_dados, df], ignore_index=True)
    # Agora que todos os dados estão em 'todos_dados', vamos inserir no MySQL
    for i, row in todos_dados.iterrows():
        # Inserção no MySQL com as colunas ajustadas
        cursor.execute("""
        INSERT INTO operadoras (reg_ans, cnpj, razao_social, nome_fantasia, modalidade, uf, data_registro)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (row['REG_ANS'], row['CD_CONTA_CONTABIL'], row['DESCRICAO'], row['VL_SALDO_INICIAL'], row['VL_SALDO_FINAL'], None, None))  # Ajuste conforme necessário

    conexao.commit()
    cursor.close()

# Função principal
def main():
    # Caminho da pasta onde estão os arquivos CSV
    diretorio = r"C:\Users\Pichau\Desktop\Teste IntuitiveCare\Demonstrações"
    # Conectar ao banco de dados MySQL
    conexao = conectar_mysql()
    criar_tabela(conexao)
    # Importar e juntar todos os CSVs
    importar_csv(conexao, diretorio)
    conexao.close()
if __name__ == "__main__":
    main()
