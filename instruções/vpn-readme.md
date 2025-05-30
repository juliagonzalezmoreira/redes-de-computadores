
# Passo a passo - VPN

## Passo 1: Conectando no CMD

- Copie o seu **Endereço IPv4 público** e no terminal escreva:

```bash
cd Downloads
ssh -i <nome-da-chave>.pem ubuntu@<ip> #Não esqueça de tirar os <> e só substituir.
```

---

## Passo 2: Configurar a VPN!

- Instale a vpn na sua instância

```bash
sudo apt update #Atualiza a instancia
sudo apt install openvpn easy-rsa -y
```

```bash
cd /etc/openvpn/
cd /server

sudo touch servidor.conf #cria o arquivo servidor para a vpn
sudo nano servidor.conf
```

- Escreva as seguintes configurações para servidor.conf:

```bash
dev tun
ifconfig 10.0.0.1 10.0.0.2
secret /etc/openvpn/server/<nome-chave>
port 5000
proto udp
comp-lzo
verb 4
keepalive 10 120
persist-key
persist-tun
float
cipher AES256
```

- Gere a chave e libere a porta 5000 - tipo UDP Personalizado no grupo de segurança:

```bash
sudo openvpn --genkey secret <nome-chave>
```

```bash
sudo nano /etc/openvpn/client/client.ovpn

#Escreva isso:
dev tun
proto udp
remote <ip-da-instancia> 5000
ifconfig 10.0.0.2 10.0.0.1
secret <nome-chave>
cipher AES256
comp-lzo
verb 4
keepalive 10 120
persist-key
persist-tun
float

route 10.0.0.1 255.255.255.255
```

- Vamos startar e atualizar sua vpn

```bash
sudo systemctl start openvpn-server@servidor
sudo systemctl daemon-reload
sudo systemctl restart openvpn-server@servidor #so use se for reconfigurar algo
```

---

## Passo 3: Vamos configurar sua VPN no NGINX!

```bash
cd 
cd <nome-do-repositorio>
sudo nano docker-compose.yml
```

- Edite seu arquivo docker-compose.yml

```bash
   nginx:latest
    container_name: loadbalancer
    depends_on:
      - app1
      - app2
      - app3
    ports:
      - "10.0.0.1:80:80" #Alterei aqui, adicionei o 10.0.0.1:
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
```

- Rebuilde o docker

```bash
sudo docker-compose down
sudo docker-compose up --build -d
```

---

## Passo 4:

```bash
cd 
cd /etc/openvpn/client
sudo cp client.ovpn /home/ubuntu #copio para o ubuntu para ser acessivvel pro scp, que so tem acesso até o ubuntu
```

```bash
cd /etc/openvpn/server
sudo *chmod 40*4 <nome-chave>
sudo cp <nome-chave> /home/ubuntu
```

- Exemplo do terminal:

```bash
ubuntu@ip-172-31-16-164:/etc/openvpn/server$ cd /home/ubuntu
ubuntu@ip-172-31-16-164:~$ ls
Redes-de-Computadores  client.ovpn  <nome-chave>
ubuntu@ip-172-31-16-164:~$ sudo chmod 404 <nome-chave>
ubuntu@ip-172-31-16-164:~$ exit
```

---

## Passo 5:

- No terminal, ainda em Downloads, escreva:

```bash
scp -i <chave-aws>.pem ubuntu@<ip-da-instancia>:/home/ubuntu/<nome-chave> .
scp -i <chave-aws>.pem ubuntu@<ip-da-instancia>:/home/ubuntu/client.ovpn .
```

- Seu terminal vai ficar assim, exemplo:

```bash
#Exemplo de como seu terminal DEVE ficar
C:\Users\matos\Downloads>scp -i sofia.pem [ubuntu@13.218.85.92](mailto:ubuntu@13.218.85.92):/home/ubuntu/sofia .
sofia 100% 636 0.9KB/s 00:00
C:\Users\matos\Downloads>scp -i sofia.pem [ubuntu@13.218.85.92](mailto:ubuntu@13.218.85.92):/home/ubuntu/client.ovpn .
client.ovpn  100%  194     0.4KB/s   00:00
```

---

## Passo 6: Instalar OpenVpn e configurar

- Acesse o site abaixo para baixar o OpenVPN e instale o “Windows 64-bit MSI installer”:
    
    https://openvpn.net/community-downloads/
    
- Você vai receber um aviso como este:
    
    ![aviso-openVpn (1)](https://github.com/user-attachments/assets/1f6c328d-7433-4511-94c3-e3f26bb159d2)

    
- Acesso a pasta manualmente e vou até C:\Users\matos\OpenVpn\config
- Vou em Downloads e copio os arquivos (<nome-chave> e client) para C:\Users\matos\OpenVpn\config- Veja a foto:
    
  ![caminho-pra-copiar (1)](https://github.com/user-attachments/assets/9ab708c8-57fc-461f-aa12-047f32860db7)

    
- Siga o passo da foto-sair: saia do OpenVpn
    
    ![foto-sair](https://github.com/user-attachments/assets/f1f9754a-1bcb-4490-af6a-34e98ee7f84c)
    
- Executar como administrador o OpenVpn
- Usando a foto-sair: Conecte

<aside>
🚨

> LEMBRE-SE: Sempre que você for conectar a sua instância, não se esqueça de alterar o <ip-da-instância> no client.ovpn!!!
> 
</aside>

### 1. Instale o Easy-RSA (se ainda não tiver)

```bash
sudo apt update
sudo apt install easy-rsa
```

### 2. Crie um diretório para o Easy-RSA e acesse ele

```bash
make-cadir ~/openvpn-ca
cd ~/openvpn-c
```

### 4. Inicialize a PKI (Public Key Infrastructure)

```bash

./easyrsa init-pki
```

### 5. Construa a autoridade certificadora (CA)

```bash
./easyrsa build-ca
```

- Vai pedir um nome para a CA (default geralmente é “Easy-RSA CA”, pode usar “redes” por exemplo)
- Crie uma senha para proteger a CA (anote ela!) ou deixe em branco (não recomendado).

### 6. Gere a chave e o certificado do servidor

```bash
./easyrsa gen-req server nopass
```

- Gera uma chave privada do servidor e uma requisição de certificado (CSR).

Depois, assine a requisição com a CA:

```bash
./easyrsa sign-req server server
```

- Confirme a assinatura.

### 7. Gere os parâmetros Diffie-Hellman (DH)

```bash
./easyrsa gen-dh
```

- Cria o arquivo `dh.pem` que é usado para troca segura de chaves.

### 8. Gere a chave TLS para proteção extra (opcional, mas recomendado)

```bash
openvpn --genkey --secret ta.key
```

- Gera o arquivo `ta.key` usado na configuração do TLS Authentication.

### 9. Gere os certificados para os clientes

Para cada cliente, gere uma chave privada e um certificado:

```bash
./easyrsa gen-req client1 nopass
./easyrsa sign-req client client1
```

(Substitua `client1` pelo nome de cada cliente.)

---

# Resumo dos arquivos

- `ca.crt` — Certificado da Autoridade Certificadora (CA)
- `server.crt` e `server.key` — Certificado e chave privada do servidor
- `dh.pem` — Parâmetros Diffie-Hellman
- `ta.key` — Chave para autenticação TLS
- `client1.crt` e `client1.key` — Certificado e chave do cliente
- `server.conf`
- `client.ovpn`

* Mova os arquivos para home/ubuntu e depois para máquina local

OBS: usei a porta 1194 UDP, adicionei nas regras da instância

![image](https://github.com/user-attachments/assets/9e769382-1e86-441e-ba93-dc72238a7532)

