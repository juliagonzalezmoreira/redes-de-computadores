from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL
import os

# Cria a aplicação Flask
app = Flask(__name__)

# Captura o nome do servidor enviado pela variável de ambiente (usado para mostrar qual container respondeu)
server_name = os.environ.get("SERVER_NAME", "Default Server")

# Configurações de conexão com o banco de dados MySQL hospedado na AWS RDS
app.config['MYSQL_HOST'] = 'database-1.cyuqerkjhmh8.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'ProjetoRedes' #SENHA AQUI
app.config['MYSQL_DB'] = 'bdaws'

# Inicializa o MySQL com as configurações acima
mysql = MySQL(app)

# Rota principal para cadastro de usuários
@app.route('/', methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        # Coleta os dados enviados pelo formulário
        nome = request.form['nome']
        email = request.form['email']
        filme = request.form['filme']
        nota = request.form['nota']
        opiniao = request.form['opiniao']

        # Insere os dados no banco de dados
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios(nome, email, filme, nota, opiniao) VALUES (%s, %s, %s, %s, %s)", 
                    (nome, email, filme, nota, opiniao))
        mysql.connection.commit()
        cur.close()

        # Recarrega a página após o cadastro
        return render_template('cadastro.html')
    
    # Renderiza o formulário se for GET
    return render_template('cadastro.html')

# Rota para editar um cadastro existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        # Atualiza os dados do usuário no banco
        nome = request.form['nome']
        email = request.form['email']
        filme = request.form['filme']
        nota = request.form['nota']
        opiniao = request.form['opiniao']

        cur.execute("""
            UPDATE usuarios 
            SET nome=%s, email=%s, filme=%s, nota=%s, opiniao=%s 
            WHERE id=%s
        """, (nome, email, filme, nota, opiniao, id))
        mysql.connection.commit()
        cur.close()

        # Redireciona para a página de listagem após salvar
        return redirect(url_for('users'))
    
    # Busca os dados do usuário no banco para preencher o formulário
    cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    return render_template('editar.html', user=user)

# Rota para excluir um usuário
@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('users'))

# Rota para listar todos os usuários cadastrados
@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM usuarios")

    if users > 0:
        userDetails = cur.fetchall()  # Pega todos os registros
        return render_template("users.html", userDetails=userDetails)
    
    # Caso não haja nenhum registro
    return 'Nenhum usuário encontrado.'

# Torna o nome do servidor acessível nos templates HTML
@app.context_processor
def inject_server_name():
    return dict(server_name=server_name)

# Roda a aplicação Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
