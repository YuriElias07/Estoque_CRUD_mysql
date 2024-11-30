import mysql.connector
from mysql.connector import Error
from datetime import datetime


# CONEXÃO COM O MYSQL
def db_config():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mysql102030",    
            database="estoque"
        )
        if connection.is_connected():
            print("Conexão bem-sucedida ao banco de dados!")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None


# REGISTRAR PRODUTOS NO DB
def inserir_produto():
    nome = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição do produto: ")
    qtde_disp = int(input("Digite a quantidade disponível: "))
    preco = float(input("Digite o preço do produto: "))
    
    connection = db_config()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO produtos (nome, descrição, qtde_disp, preco)
            VALUES (%s, %s, %s, %s)
        """, (nome, descricao, qtde_disp, preco))
        connection.commit()
        print(f"Produto '{nome}' inserido com sucesso!")
        cursor.close()
        connection.close()


# LISTAR PRODUTOS EM ESTOQUE NO DB
def listar_produtos():
    connection = db_config()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        print("\nProdutos no estoque:")
        for produto in produtos:
            print(produto)
        cursor.close()
        connection.close()


# ATUALIZAR PRODUTO EXISTENTE NO DB
def atualizar_produto():
    id_produto = int(input("Digite o ID do produto a ser atualizado: "))
    nome = input("Digite o novo nome do produto: ")
    descricao = input("Digite a nova descrição do produto: ")
    qtde_disp = int(input("Digite a nova quantidade disponível: "))
    preco = float(input("Digite o novo preço do produto: "))
    
    connection = db_config()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE produtos
            SET nome = %s, descrição = %s, qtde_disp = %s, preco = %s
            WHERE id = %s
        """, (nome, descricao, qtde_disp, preco, id_produto))
        connection.commit()
        print(f"Produto {id_produto} atualizado com sucesso!")
        cursor.close()
        connection.close()


# REMOVER PRODUTO NO MYSQL
def deletar_produto():
    id_produto = int(input("Digite o ID do produto a ser deletado: "))
    
    connection = db_config()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM vendas WHERE id_produtos = %s", (id_produto,))

        cursor.execute("DELETE FROM produtos WHERE id = %s", (id_produto,))
        connection.commit()
        
        print(f"Produto {id_produto} e suas vendas associadas foram deletados com sucesso!")
        
        cursor.close()
        connection.close()


# REGISTRAR VENDA DE PRODUTOS
def registrar_venda():
    id_produto = int(input("Digite o ID do produto que foi vendido: "))
    qtde_vendida = int(input("Digite a quantidade vendida: "))
    
    connection = db_config()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT qtde_disp FROM produtos WHERE id = %s", (id_produto,))
        produto = cursor.fetchone()
        
        if produto and produto[0] >= qtde_vendida:
            nova_qtde = produto[0] - qtde_vendida
            cursor.execute("UPDATE produtos SET qtde_disp = %s WHERE id = %s", (nova_qtde, id_produto))

            data_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT INTO vendas (qtde_vendida, data_venda, id_produtos)
                VALUES (%s, %s, %s)
            """, (qtde_vendida, data_venda, id_produto))
            connection.commit()
            print(f"Venda registrada: {qtde_vendida} unidades do produto {id_produto}.")
        else:
            print(f"Quantidade insuficiente em estoque para o produto {id_produto}.")
        
        cursor.close()
        connection.close()


# LISTAR VENDAS FEITAS
def listar_vendas():
    connection = db_config()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM vendas")
        vendas = cursor.fetchall()
        print("\nVendas registradas:")
        for venda in vendas:
            print(venda)
        cursor.close()
        connection.close()


def menu():
    while True:
        print("""
    Escolha uma das opções abaixo:              
        1 - Inserir produto
        2 - Listar produtos
        3 - Atualizar produtos
        4 - Deletar produto
        5 - Registrar venda
        6 - Listar vendas
        7 - Sair
              """)
        
        opcao = int(input("Digite a opção desejada: "))

        if opcao == 1:
            inserir_produto()
        elif opcao == 2:
            listar_produtos()
        elif opcao == 3:
            atualizar_produto()
        elif opcao == 4:
            deletar_produto()
        elif opcao == 5:
            registrar_venda()
        elif opcao == 6:
            listar_vendas()
        elif opcao == 7:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


menu()
