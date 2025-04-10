## Trabalho Prático: Infraestrutura de Rede Integrada para a Empresa XPTO

### 📍 Objetivo: 
Projetar e implementar uma infraestrutura de TI robusta para a empresa XPTO integrando tecnologias modernas de redes e segurança. O projeto deve incluir um ambiente de acesso remoto seguro, gerenciamento de tráfego e serviços virtualizados, garantindo confiabilidade e eficiência para a organização. 

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

### Arquitetura da rede
![dagrama-de-redes](https://github.com/user-attachments/assets/4d005e48-e671-4976-875d-962a99841b41)


### Tecnologias usadas
![AWS](https://img.shields.io/badge/aws-232F3E.svg?style=for-the-badge&logo=aws&logoColor=white)
![Ubuntu](https://img.shields.io/badge/ubuntu-E95420.svg?style=for-the-badge&logo=ubuntu&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-1572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Python](https://img.shields.io/badge/python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![AWS RDS](https://img.shields.io/badge/AWS_RDS-527FFF.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)

### Visão Geral
Aplicação web baseada em Docker que consiste em uma arquitetura de múltiplos containers. É dividida em três componentes principais: o backend (que executa o servidor Python/Flask), o Nginx (como proxy reverso e balanceador de carga), e o Banco de Dados AWS RDS (MySQL) (para armazenamento de dados relacionados aos usuários e suas opiniões sobre filmes).

### Estrutura do Projeto
O projeto está organizado da seguinte forma:
- Backend (app1, app2, app3): Três instâncias da aplicação backend, cada uma executando a mesma aplicação, mas distribuídas para melhorar a escalabilidade e o balanceamento de carga;
- Nginx: Atua como um proxy reverso e balanceador de carga, distribuindo as requisições entre as três instâncias de backend (app1, app2, app3);
- Banco de Dados AWS RDS (MySQL): Banco de dados que armazena as informações dos usuários e suas interações com a aplicação (como suas avaliações de filmes).

### Arquitetura e Justificativa

#### Escolha do Docker
O uso do Docker permite isolar os componentes da aplicação (backend e proxy) em containers separados. Isso oferece vantagens:

1. Isolamento e Independência: Cada parte funciona de forma independente, o que facilita a manutenção e a atualização de componentes sem afetar o funcionamento dos outros;
2. Escalabilidade: Com o Docker, é fácil escalar a aplicação para mais instâncias do backend, conforme necessário. Por exemplo, podemos adicionar mais containers appX sem alterar a configuração de outros serviços;
3. Portabilidade: A aplicação é executada no mesmo ambiente em qualquer máquina ou servidor, garantindo consistência entre desenvolvimento, testes e produção.

#### Escolha do Load Balancer (Nginx)
Estamos usando o Nginx como proxy reverso e load balancer por ser uma solução robusta, amplamente utilizada, e de fácil configuração. Ele distribui o tráfego de entrada entre as instâncias do backend (app1, app2, app3), garantindo:

1. Desempenho otimizado: O Nginx é altamente eficiente na distribuição de requisições;
2. Alta disponibilidade: Caso uma das instâncias do backend falhe, o Nginx pode redirecionar as requisições para outras instâncias disponíveis;
3. Escalabilidade: A configuração do Nginx permite facilmente adicionar ou remover instâncias de backend.

#### Banco de Dados - AWS RDS (MySQL)
Utilizar o RDS permite escalar o banco de dados de forma automática, além de contar com a robustez e segurança fornecidas pela AWS. A escolha do MySQL como sistema de gerenciamento de banco de dados é devido à sua simplicidade e compatibilidade com a aplicação.

### Explicação das Configurações

#### Dockerfile
O arquivo Dockerfile define como a imagem do backend será construída:
- Base de Imagem: Utilizamos uma imagem base do Python (python:3.9-slim) para rodar a aplicação;
- Instalação de Dependências: O comando ```sudo apt update``` instala as dependências nativas necessárias para o funcionamento da aplicação, como bibliotecas para conexão com o MySQL;
- Instalação das Dependências Python: O requirements.txt é copiado para dentro do container e as dependências do Python são instaladas;
- Expõe a Porta: A aplicação Flask vai rodar na porta 5000 dentro do container. Essa porta é exposta para permitir a comunicação entre os containers e com o exterior;
- Comando para iniciar a aplicação: O container é configurado para executar o comando python app.py quando iniciado, o que inicia o servidor Flask.

#### Banco de Dados - AWS RDS (MySQL)
O banco de dados MySQL está hospedado na AWS, utilizando o serviço RDS (Relational Database Service). A tabela usuarios foi criada para armazenar informações sobre filmes e opiniões dos usuários.

#### Nginx - Proxy Reverso e Load Balancer
O arquivo default.conf contém a configuração do Nginx para distribuir o tráfego entre os três containers de backend. A configuração do upstream define o grupo de servidores de backend (app1, app2, app3):

- Pesos Diferenciados: Cada servidor tem um peso. O app1 tem um peso maior (3), significando que ele irá receber mais tráfego do que os outros dois servidores (app2 e app3), que têm peso 1;
- Proxy Reverso: Quando uma requisição chega na porta 80 (do Nginx), ela é redirecionada para um dos servidores backend definidos no upstream backend. O Nginx repassa as requisições para os backends disponíveis de forma equilibrada;
- A configuração de proxy_set_header assegura que os cabeçalhos HTTP corretos sejam passados para os servidores backend, incluindo o IP do cliente original.

#### Docker Compose
O arquivo docker-compose.yml orquestra a execução dos containers. Ele define os seguintes serviços:

- app1, app2, app3: Cada um desses serviços é uma instância da aplicação backend. A opção build aponta para o diretório onde o Dockerfile está localizado, garantindo que a imagem seja construída a partir do código-fonte. As portas 5001, 5002, e 5003 são mapeadas para as portas internas 5000, permitindo que as instâncias se comuniquem entre si.
- Nginx: O Nginx depende dos três containers de backend. Ele escuta na porta 80 e repassa as requisições para o backend de acordo com a configuração do default.conf. A configuração depends_on garante que o Nginx só será iniciado após as instâncias do backend estarem prontas.

### Fluxo de Requisições
1. O usuário envia uma requisição para o servidor, que é direcionada à porta 80 do Nginx;
2. O Nginx, atuando como proxy reverso, recebe a requisição e a encaminha para uma das instâncias de backend (app1, app2, ou app3) com base na configuração de balanceamento de carga;
3. A instância do backend processa a requisição, interage com o banco de dados (se necessário) e envia a resposta de volta para o Nginx;
4. O Nginx retorna a resposta ao usuário.

### Conclusão e Benefícios da Arquitetura
- Escalabilidade: O uso de múltiplas instâncias de backend permite que a aplicação lide com mais tráfego, pois o Nginx distribui as requisições entre os servidores;
- Alta Disponibilidade: Com o Nginx como load balancer, se uma instância falhar, as outras ainda poderão atender às requisições, garantindo a continuidade do serviço;
- Facilidade de Manutenção: O backend e o proxy estão isolados em containers separados, o que facilita a manutenção e a atualização de componentes sem afetar os outros. Além disso, o banco de dados, hospedado no AWS RDS MySQL, oferece vantagens como gerenciamento simplificado, backups automáticos, monitoramento integrado, entre outras. Isso garante que o banco de dados seja mantido de forma eficiente e sem a necessidade de intervenção direta no servidor.

Esta abordagem modular e escalável é uma solução ideal para aplicações que precisam lidar com uma carga variável ou crescer conforme a demanda.
