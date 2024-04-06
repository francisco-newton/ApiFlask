import requests as rq

# Menu de opções
def menu():
    print("1 - Cadastrar novo usuário")
    print("2 - Atualizar usuário")
    print("3 - Buscar todos os usuários")
    print("4 - Adicionar produto ao carrinho")
    print("5 - Remover produto do carrinho")
    print("6 - Total do carrinho")
    print("7 - Sair")
    return int(input("Opção: "))

# Pega os dados de acordo com a opção escolhida
def pega_dados(op):
    if op == 1:
        nome = input("Nome do usuário: ")
        usuario = input("User do usuário: ")
        new_usuario(nome, usuario)
        return True
    elif op == 2:
        id = input("ID: ")
        nome = input("Nome: ")
        atualizar_usuario(id, nome)
        return True
    elif op == 3:
        get_usuarios()
        return True
    elif op == 4:
        codigo = input("Código: ")
        nome = input("Nome: ")
        valor = input("Valor: ")
        add_produto(codigo, nome, valor)
        return True
    elif op == 5:
        id = input("ID: ")
        codigo = input("Código: ")
        remover_produto(id, codigo)
        return True
    elif op == 6:
        total_carrinho()
        return True
    elif op == 7:
        return False


# Busca todos os usuários cadastrados
def get_usuarios():
    url = "http://localhost:5000/usuarios/todos"
    response = rq.get(url)
    print(response.json())

# Cadastra um novo usuário
def new_usuario(nome, usuario):
    url = "http://localhost:5000/usuarios/novo"
    data = {
        "nome": f"{nome}",
        "usuario": f"{usuario}",
    }
    response = rq.post(url, json=data)
    print(response.json())

# Atualiza um usuário
def atualizar_usuario(id, nome):
    url = f"http://localhost:5000/usuarios/atualizar/id={id}"
    data = {
        "nome": f"{nome}",
    }
    response = rq.put(url, json=data)
    print(response.json())

# Busca um carrinho pelo ID
def get_carrinho(id):
    url = f"http://localhost:5000/carrinho/id={id}"
    response = rq.get(url)
    print(response.json())

# Adiciona um produto ao carrinho
def add_produto(codigo, nome, valor):
    url = "http://localhost:5000/carrinho/adicionar"
    data = {
        "codigo": f"{codigo}",
        "nome": f"{nome}",
        "valor": f"{valor}",
    }
    response = rq.post(url, json=data)
    print(response.json())

# Remove um produto do carrinho
def remover_produto(id, codigo):
    url = f"http://localhost:5000/carrinho/remover/codigo={codigo}"
    data = {
        "codigo": f"{codigo}",
    }
    response = rq.delete(url, json=data)
    print(response.json())

# Retorna o total do carrinho
def total_carrinho():
    url = "http://localhost:5000/carrinho/total"
    response = rq.get(url)
    print(response.json())

# Cria o loop que sera executado os comandos
# para a API
while True:
    op = menu()
    if not pega_dados(op):
        break