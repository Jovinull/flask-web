# Importa a classe MethodView do Flask e módulos necessários para a renderização de templates e manipulação de requisições
from flask.views import MethodView
from flask import request, render_template, redirect
from src.db import mysql  # Importa a biblioteca PyMySQL

# Define um controlador de exemplo utilizando a classe MethodView do Flask
class IndexController(MethodView):
    def get(self):
        # Método para lidar com requisições GET
        # Realiza uma consulta ao banco de dados para obter todos os produtos
        with mysql.cursor() as cur:
            cur.execute('SELECT * FROM produtos')
            data = cur.fetchall()
        # Retorna o conteúdo renderizado do template 'public/index.html', passando os dados obtidos como contexto
        return render_template('public/index.html', data=data)

    def post(self):
        # Método para lidar com requisições POST
        # Obtém os dados do formulário enviado através da requisição POST
        code = request.form['code']
        name = request.form['name']
        stock = request.form['stock']
        value = request.form['value']
        
        # Insere os dados do novo produto no banco de dados
        with mysql.cursor() as cur:
            cur.execute('INSERT INTO produtos(code, name, stock, value) VALUES(%s, %s, %s, %s)', (code, name, stock, value))
            cur.connection.commit()
            # Redireciona para a página inicial após a inserção
            return redirect('/')

# Define um controlador para excluir um produto
class DeleteProdutoController(MethodView):
    def post(self, code):
        # Método para lidar com requisições POST para excluir um produto
        # Obtém o código do produto a ser excluído da URL
        # Executa uma instrução SQL para excluir o produto com o código fornecido
        with mysql.cursor() as cur:
            cur.execute('DELETE FROM produtos WHERE code=%s', (code,))
            cur.connection.commit()
            # Redireciona para a página inicial após a exclusão
            return redirect('/')

# Define um controlador para atualizar os detalhes de um produto
class UpdateProdutoController(MethodView):
    def get(self, code):
        # Método para lidar com requisições GET para exibir o formulário de atualização do produto
        # Obtém os detalhes do produto com o código fornecido
        with mysql.cursor() as cur:
            cur.execute('SELECT * FROM produtos WHERE code=%s', (code,))
            produto = cur.fetchone()
            # Renderiza o template 'public/update.html', passando os detalhes do produto como contexto
            return render_template('public/update.html', produto=produto)

    def post(self, code):
        # Método para lidar com requisições POST para atualizar os detalhes do produto
        # Obtém os dados do formulário enviado através da requisição POST
        produtoCode = request.form['code']
        name = request.form['name']
        stock = request.form['stock']
        value = request.form['value']

        # Executa uma instrução SQL para atualizar os detalhes do produto com o código fornecido
        with mysql.cursor() as cur:
            cur.execute('UPDATE produtos SET code=%s, name=%s, stock=%s, value=%s WHERE code=%s', (produtoCode, name, stock, value, code))
            cur.connection.commit()
            # Redireciona para a página inicial após a atualização
            return redirect('/')
