from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


usuariosBanco = {1 :{
   'usuario' : 'pessoa1',
   'nome' : 'Pessoa 1 Padrão',
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
            description: Erro interno
            schema:
                type: object
                properties:
                Resposta:
                    type: string
    """
    try:
        return {'Resposta' : usuariosBanco}, 200
    except:
        return {'Resposta': 'Erro interno'}, 500

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
        400:
            description: Invalid data format
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
        500:
            description: Erro interno
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
    """

    try:
        if request.json:
            data = request.json
        else:
            return {'Resposta': 'Formato de dados inválido'}, 400

        novoID = len(usuariosBanco) + 1
        novoUsuario = {
            'usuario' : data.get('usuario'),
            'nome' : data.get('nome'),
            'id' : novoID,
            'carrinho' : {}
        }

        usuariosBanco[novoID] = novoUsuario
        return {"Resposta": novoUsuario}, 200
    except:
        return {'Resposta': 'Erro interno'}, 500

@app.route('/usuarios/atualizar/<int:id>', methods=['PUT'])
def update_usuario(id):

    """
    Update an existing user
    ---
    parameters:
        - name: id
          in: path
          type: integer
          required: true
        - name: nome
          in: body
          type: string
          required: true
    responses:
        200:
            description: User updated successfully
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
        400:
            description: Invalid data format
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
        500:
            description: Erro interno
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
    """

    try:
        if request.json:
            data = request.json
        else:
            return {'Resposta': 'Formato de dados inválido'}, 400

        usuariosBanco[id]['nome'] = data.get('nome')
        return {"Resposta": 'Usuário atualizado com sucesso!'}, 200
    except:
        return {'Resposta': 'Erro interno'}, 500

@app.route('/carrinho/<int:id>', methods=['GET'])
def get_carrinho(id):
    """
    Get the user's cart	
    ---	
    parameters:
        - name: id
          in: path
          type: integer
          required: true
    responses:
        200:
            description: The user's cart
            schema:
                type: object
                properties:
                    Resposta:
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
            description: Erro interno
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
    """

    try:
        if request.json:
            data = request.json
        else:
            return {'Resposta': 'Formato de dados inválido'}, 400

        return {'Resposta' : usuariosBanco[id]['carrinho']}, 200
    except:
        return {'Resposta': 'Erro interno'}, 500

@app.route('/carrinho/adicionar/<int:id>', methods=['POST'])
def add_produto(id):
    """
    Add a product to the user's cart
    ---
    parameters:
        - name: id
          in: path
          type: integer
          required: true
        - name: produto
          in: body
          type: object
          required: true
          properties:
            codigo:
              type: integer
            nome:
              type: string
            valor:
              type: float
    responses: 
        201:
            description: Product added successfully
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
        400:
            description: Invalid data format
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
        500:
            description: Erro interno
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
    """
    try:
        if request.json:
            data = request.json
        else:
            return {'Resposta': 'Formato de dados inválido'}, 400

        novoProduto = {
            'codigo' : data.get('codigo'),
            'nome' : data.get('nome'),
            'valor' : data.get('valor')
        }

        usuariosBanco[id]['carrinho']['produtos'].append(novoProduto)
        usuariosBanco[id]['carrinho']['total'] += novoProduto['valor']

        return {"Resposta": 'Produto adicionado com sucesso!'}, 201
    except:
        return {'Resposta': 'Erro interno'}, 500

@app.route('/carrinho/remover/<int:id>', methods=['DELETE'])
def remove_produto(id):
    """
    Remove a product from the user's cart
    ---
    parameters:
        - name: id
          in: path
          type: integer
          required: true
        - name: produto
          in: body
          type: object
          required: true
          properties:
            valor:
              type: float
            produto:
              type: object
              properties:
                codigo:
                  type: integer
                nome:
                  type: string
                valor:
                  type: float
    responses:
        200:
            description: Product removed successfully
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
        400:
            description: Invalid data format
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
        500:
            description: Erro interno
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
    """
    try:
        if request.json:
            data = request.json
        else:
            return {'Resposta': 'Formato de dados inválido'}, 400

        usuariosBanco[id]['carrinho']['total'] -= data.get('valor')
        usuariosBanco[id]['carrinho']['produtos'].remove(data.get('codigo'))

        return {"Resposta": 'Produto removido com sucesso!'}, 200
    except:
        return {'Resposta': 'Erro interno'}, 500

@app.route('/carrinhos/total', methods=['GET'])
def get_total():
    """
    Get the total value of all carts
    ---
    responses:
        200:
            description: The total value of all carts
            schema:
                type: object
                properties:
                    Resposta:
                        type: float
        500:
            description: Erro interno
            schema:
                type: object
                properties:
                    Resposta:
                        type: string
    """
    try:
        if request.json:
            data = request.json
        else:
            return {'Resposta': 'Formato de dados inválido'}, 400

        total = 0
        for usuario in usuariosBanco:
            total += usuario['carrinho']['total']
        return {'Resposta' : total}, 200
    except:
        return {'Resposta': 'Erro interno'}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
