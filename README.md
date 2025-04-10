# 🚀 Trabalho Prático: Infraestrutura de Rede Integrada para a Empresa XPTO

## 🎯 Objetivo

Este projeto tem como objetivo a criação de uma infraestrutura de TI robusta para a empresa XPTO, integrando tecnologias modernas de rede e computação em nuvem. O foco é desenvolver um ambiente de acesso seguro, alta disponibilidade e gerenciamento eficiente de tráfego e dados, promovendo confiabilidade e eficiência para a organização.

---

## 🧩 Arquitetura da Rede
![dagrama-de-redes](https://github.com/user-attachments/assets/4d005e48-e671-4976-875d-962a99841b41)

---

## 🛠️ Tecnologias Utilizadas

![Docker](https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![NGINX](https://img.shields.io/badge/-NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![AWS](https://img.shields.io/badge/-AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![MySQL](https://img.shields.io/badge/-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

---

## 🌐 Visão Geral

A aplicação foi construída utilizando Docker, organizada em múltiplos containers. A estrutura contempla:

- **3 containers backend Flask** (Python), replicando a aplicação
- **NGINX como proxy reverso e load balancer**
- **Banco de dados MySQL** hospedado na **AWS RDS**

<Details>   
  <Summary>    
    📝 Requisitos:
  </Summary>

</br>

**1. Arquitetura da Rede:** 
Desenhar a topologia da rede;

**2. Configuração do Load Balancer:**
Implementar um Load Balancer com Nginx ou HAProxy, configurar o balanceamento entre, no mínimo, 3 máquinas para distribuir o tráfego, criar um mecanismo de monitoramento de disponibilidade e resposta dos servidores; 

**3. Proxy Reverso:** 
Configurar uma máquina com Nginx para atuar como Proxy Reverso, gerenciar requisições e redirecioná-las para os servidores apropriados;

**4. Banco de Dados:** 
Criar um servidor dedicado para o banco de dados usando Docker ou AWS RDS, escolher entre MySQL, PostgreSQL ou MongoDB e justificar a escolha;

**5. VPN (Virtual Private Network):** 
Configurar uma VPN segura (OpenVPN) para acessos externos e integrar a VPN ao firewall da rede para maior controle de acessos;

**6. Docker e Virtualização:** 
Utilizar Docker para hospedar servidores web e banco de dados, criar um docker-compose para gerenciamento facilitado dos serviços, demonstrar a escalabilidade dos containers e a comunicação entre eles;

**7. Endereçamento IPv4 e Segmentação de Redes:** 
Definir a estrutura de endereçamento da empresa e implementar DHCP para gerenciar alocação dinâmica de endereços.

</Details>

---

## 🏗️ Estrutura do Projeto

O projeto está dividido em:

- **Backend (Flask)**: Três instâncias da aplicação com rotas REST.
- **NGINX**: Load balancer que distribui requisições para os containers backend.
- **Docker Compose**: Orquestra os containers e redes.
- **Banco de Dados (MySQL na AWS)**: Armazena os dados de usuários e pedidos.
- **RDS da AWS**: Oferece segurança, escalabilidade e gerenciamento automatizado.

---

## 🧠 Arquitetura e Justificativa Técnica

### Uso do Docker

- Cada serviço é containerizado de forma independente.
- Facilita deploy, manutenção e escalabilidade.
- Garante isolamento de ambiente e portabilidade.

### Balanceamento de Carga com NGINX

- Garante distribuição uniforme das requisições.
- Aumenta disponibilidade e tolerância a falhas.
- Usa algoritmo **round-robin**.

### Banco de Dados na AWS RDS

- Alta disponibilidade com replicação e backups automáticos.
- Segurança com grupos de segurança e acesso restrito por IP.
- Gerenciamento simplificado.

---

## ⚙️ Explicação das Configurações

### 🧱 Passo a Passo Completo da Infraestrutura (EC2, Docker, NGINX)

1. Criar instância EC2 (Ubuntu 22.04)
* Configure a porta 80 (HTTP) e porta 22 (SSH) no grupo de segurança

2. Acessar a instância via SSH
No terminal da sua máquina:

```
chmod 400 exemplo.pem
ssh -i "exemplo.pem" ubuntu@<ENDEREÇO_IP_PUBLICO>
```
3. Atualizar sistema e instalar Docker + Docker Compose
```
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose nano -y
```
📁 4. Criar estrutura de diretórios e arquivos
Criar pasta do projeto
```
mkdir projeto
cd projeto
```

Criar arquivo app.py
```
nano app.py
```
Conteúdo app.py:

```
# Importa as bibliotecas necessárias
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
app.config['MYSQL_PASSWORD'] = 'ProjetoRedes'  # Atenção: nunca compartilhe senhas reais em repositórios públicos!
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

```
Criar requirements.txt
```
nano requirements.txt
```
Conteúdo:
```
# Utilitário de sinais usado internamente pelo Flask
blinker==1.9.0

# Biblioteca para criação de comandos de linha de comando (CLI), usada pelo Flask
click==8.1.8

# Fornece suporte a cores no terminal, útil em ambientes Windows
colorama==0.4.6

# Microframework web principal utilizado no projeto
Flask==3.1.0

# Fornece funções para segurança, como geração de tokens, usado internamente no Flask
itsdangerous==2.2.0

# Template engine utilizada pelo Flask para renderizar HTML
Jinja2==3.1.6

# Dependência do Jinja2, usada para manipulação segura de strings HTML
MarkupSafe==3.0.2

# Ferramenta WSGI que gerencia requisições/respostas HTTP no Flask
Werkzeug==3.1.3

# Extensão do Flask para integração com bancos de dados MySQL
Flask-MySQLdb==2.0.0
```

Criar Dockerfile
```
nano Dockerfile
```
Conteúdo:

```
# Usa uma imagem leve do Python baseada no Debian Bookworm
FROM python:3.9-slim-bookworm

# Atualiza os pacotes do sistema e instala dependências necessárias para compilar e conectar ao MySQL
RUN apt-get update && apt-get install -y \
    build-essential \                   # Ferramentas para compilar pacotes Python com código C/C++
    default-libmysqlclient-dev \       # Biblioteca necessária para conectar com MySQL (ex: mysqlclient)
    pkg-config \                        # Utilitário que ajuda na compilação de pacotes nativos
    && rm -rf /var/lib/apt/lists/*     # Limpa o cache do APT para reduzir o tamanho final da imagem

# Define o diretório de trabalho dentro do container (tudo será executado a partir daqui)
WORKDIR /app

# Copia primeiro o arquivo requirements.txt para instalar as dependências (boa prática de cache)
COPY requirements.txt .

# Instala as bibliotecas Python necessárias para o projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação (app.py, templates, etc.) para o container
COPY . .

# Expõe a porta 5000, que é onde o Flask roda por padrão
EXPOSE 5000

# Comando que será executado ao iniciar o container (roda o app Flask)
CMD ["python", "app.py"]

```
🌐 5. Configurar NGINX como Proxy Reverso e Load Balancer
Voltar para pasta raiz e criar pasta nginx
```
cd ..
mkdir nginx
cd nginx
nano default.conf
```
Conteúdo default.conf:
```
# Define o grupo de servidores (backend) para balanceamento de carga
upstream backend {
        server app1:5000 weight=3;  # O container app1 tem mais peso (será escolhido com mais frequência)
        server app2:5000 weight=1;  # app2 e app3 têm menos peso, usados com menos frequência
        server app3:5000 weight=1;
}

# Configuração do servidor NGINX que escuta na porta 80
server {
        listen 80;  # Porta padrão para requisições HTTP

        location / {
                # Redireciona as requisições para o grupo de servidores definido acima
                proxy_pass http://backend;

                # Encaminha o nome do host original (opcional, mas pode ser útil para logs)
                proxy_set_header Host $host;

                # Encaminha o IP real do cliente que fez a requisição
                proxy_set_header X-Real-IP $remote_addr;
        }
}

```

🧩 6. Criar docker-compose.yml na raiz do projeto

```bash

cd ..
nano docker-compose.yml
```
Conteúdo:
```
version: '3.8'  # Define a versão do Docker Compose

services:  # Seção onde definimos os serviços (containers)

  # Primeiro container da aplicação
  app1:
    build: ./projeto-web            # Caminho para o Dockerfile da aplicação
    container_name: app1            # Nome do container no Docker (facilita identificar)
    environment:
      SERVER_NAME: "Servidor 1"     # Variável de ambiente que será usada na aplicação Flask
    ports:
      - "5001:5000"                 # Porta externa 5001 → porta interna 5000

  # Segundo container da aplicação
  app2:
    build: ./projeto-web
    container_name: app2
    environment:
      SERVER_NAME: "Servidor 2"
    ports:
      - "5002:5000"

  # Terceiro container da aplicação
  app3:
    build: ./projeto-web
    container_name: app3
    environment:
      SERVER_NAME: "Servidor 3"
    ports:
      - "5003:5000"

  # Container do NGINX atuando como proxy reverso e balanceador de carga
  nginx:
    image: nginx:latest             # Usa a imagem mais recente do NGINX
    container_name: loadbalancer    # Nome do container do NGINX
    depends_on:
      - app1
      - app2
      - app3                        # Garante que o NGINX só suba após os apps
    ports:
      - "80:80"                     # Porta 80 do host → porta 80 do container (HTTP padrão)
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
        # Monta o arquivo de configuração do NGINX no container
        # :ro = read-only (protege contra alterações acidentais)

```
      
▶️ 7. Rodar a aplicação
```bash
docker-compose up -d
```
Acesse no navegador: http://<ENDEREÇO_IP_PUBLICO> ou  http://localhost

Você verá a aplicação em uma das instâncias (app1, app2 ou app3)

----

## 📝 Resumo:
🐳 Dockerfile
* Define como a imagem do backend será criada:
* Usa imagem base Python 3.9;
* Instala bibliotecas do sistema e dependências Python (via requirements.txt);
* Expõe a porta 5000 para acesso à aplicação Flask;
* Inicia a aplicação com python app.py.

💾 Banco de Dados (AWS RDS MySQL)
* Banco de dados hospedado na AWS RDS;
* Tabela criada para armazenar dados dos usuários e suas opiniões sobre filmes.

🌐 Nginx (Proxy Reverso + Load Balancer)
* Distribui o tráfego entre 3 containers de backend (app1, app2, app3);
* Usa pesos para definir quais instâncias recebem mais requisições (app1 recebe mais);
* Encaminha requisições da porta 80 para o backend de forma equilibrada.

🧩 Docker Compose
* Orquestra a execução de todos os containers;
* Define os serviços app1, app2, app3 (backends) e nginx;
* Garante que o Nginx só inicie após os backends estarem prontos.

🔁 Fluxo das Requisições
* O usuário acessa o sistema via navegador (porta 80);
* O Nginx recebe a requisição e a redireciona para uma instância de backend;
* O backend processa e consulta o banco de dados, se necessário;
* O Nginx retorna a resposta ao usuário.

✅ Benefícios da Arquitetura
* Escalável: Suporta mais acessos com múltiplos containers;
* Alta Disponibilidade: Se uma instância falhar, as outras continuam funcionando;
* Fácil de manter: Componentes isolados e banco de dados gerenciado na nuvem.


