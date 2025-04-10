# Usa uma imagem leve do Python baseada no Debian Bookworm
FROM python:3.9-slim-bookworm

# Atualiza o gerenciador de pacotes e instala bibliotecas do sistema necessárias
RUN apt-get update && apt-get install -y \
    # Ferramentas para compilar pacotes Python nativos
    build-essential \       
    # Dependência necessária para MySQL (por exemplo, para mysqlclient)          
    default-libmysqlclient-dev \
    # Utilitário de configuração de pacotes C/C++     
    pkg-config \             
    # Limpa o cache do APT para reduzir o tamanho da imagem final        
    && rm -rf /var/lib/apt/lists/*   

# Define o diretório de trabalho no container
WORKDIR /app

# Copia apenas o requirements.txt primeiro para instalar dependências em cache
COPY requirements.txt .

# Instala as bibliotecas Python listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação para dentro do container
COPY . .

# Expõe a porta 5000 (usada pelo Flask por padrão)
EXPOSE 5000

# Comando que roda o app Flask
CMD ["python", "app.py"]
