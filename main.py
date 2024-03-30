from flask import Flask, request, jsonify

app = Flask(__name__)

# Dados de exemplo
"""
{
   'usuario' : 'marcilio',
   'nome' : 'Marcilio F Oliveira',
   'id' : 1,
   'carrinho' : {
        'total' : 42,53
        'produtos' : [
             {
                  'codigo' : 1,
                  'nome' : 'película de celular',
                  'valor': 30,00
              },
              {
                  'codigo' : 22,
                  'nome' : 'caneta de quadro branco',
                  'valor' : 12,53
              }
         ]
    }
}
"""

usuariosBanco = {1 :{
   'usuario' : 'marcilio',
   'nome' : 'Marcilio F Oliveira',
   'id' : 1,
   'carrinho' : {}
}} 


@app.route('/usuarios/todos', methods=['GET'])
def get_usuarios():
    return {'Resposta' : usuariosBanco}

@app.route('/usuarios/novo', methods=['POST'])
def new_usuario():
    if request.json:
        data = request.json
    else:
        return {'Resposta': 'Formato de dados inválido'}

    novoID = len(usuariosBanco) + 1
    novoUsuario = {
        'usuario' : data.get('usuario'),
        'nome' : data.get('nome'),
        'id' : novoID,
        'carrinho' : {}
    }

    usuariosBanco[novoID] = novoUsuario

    return {"Resposta": 'Usuário criado com sucesso!'}

@app.route('/usuarios/atualizar/<int:id>', methods=['PUT'])
def update_usuario(id):
    if request.json:
        data = request.json
    else:
        return {'Resposta': 'Formato de dados inválido'}

    usuariosBanco[id]['nome'] = data.get('nome')
    return {"Resposta": 'Usuário atualizado com sucesso!'}

@app.route('/carrinho/<int:id>', methods=['GET'])
def get_carrinho(id):
    if request.json:
        data = request.json
    else:
        return {'Resposta': 'Formato de dados inválido'}

    return {'Resposta' : usuariosBanco[id]['carrinho']}

@app.route('/carrinho/adicionar/<int:id>', methods=['POST'])
def add_produto(id):
    if request.json:
        data = request.json
    else:
        return {'Resposta': 'Formato de dados inválido'}

    novoProduto = {
        'codigo' : data.get('codigo'),
        'nome' : data.get('nome'),
        'valor' : data.get('valor')
    }

    usuariosBanco[id]['carrinho']['produtos'].append(novoProduto)
    usuariosBanco[id]['carrinho']['total'] += novoProduto['valor']

    return {"Resposta": 'Produto adicionado com sucesso!'}

@app.route('/carrinho/remover/<int:id>', methods=['DELETE'])
def remove_produto(id):
    if request.json:
        data = request.json
    else:
        return {'Resposta': 'Formato de dados inválido'}

    usuariosBanco[id]['carrinho']['total'] -= data.get('valor')
    usuariosBanco[id]['carrinho']['produtos'].remove(data.get('produto'))

    return {"Resposta": 'Produto removido com sucesso!'}

@app.route('/carrinhos/total', methods=['GET'])
def get_total():
    if request.json:
        data = request.json
    else:
        return {'Resposta': 'Formato de dados inválido'}

    total = 0
    for usuario in usuariosBanco:
        total += usuario['carrinho']['total']
    return {'Resposta' : total}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
