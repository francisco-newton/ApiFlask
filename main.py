from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

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
    """
    Returns all the users in the database
    ---
    responses:
      200:
        description: A list of users
        schema:
          type: object
          properties:
            Resposta:
              type: object
              properties:
                usuario:
                  type: string
                nome:
                  type: string
                id:
                  type: integer
                carrinho:
                  type: object
                  properties:
                    total:
                      type: float
                    produtos:
                      type: array
                      items:
                        type: object
                        properties:
                          codigo:
                            type: integer
                          nome:
                            type: string
                          valor:
                            type: float
        500:
            description: Invalid data format
            schema:
                type: object
                properties:
                Resposta:
                    type: string
    """
    return {'Resposta' : usuariosBanco}

@app.route('/usuarios/novo', methods=['POST'])
def new_usuario():

    """
    Create a new user
    ---
    parameters:
        - name: usuario
          in: body
          type: string
          required: true
        - name: nome
          in: body
          type: string
          required: true
    responses:
        200:
            description: User created successfully
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
        500:
            description: Invalid data format
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
    """

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
