# dns-anatel
Python Automation for RPZ (Response Policy Zone) Synchronization was developed to ensure that BIND9 DNS servers can automatically apply domain blocking policies as requested by ANATEL (National Telecommunications Agency).

+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

nano /etc/bind/named.conf.options

# Adicionar dentro de "options", para mandar para dominio ou localhost.

 options {
 //...
     response-policy {
       zone "rpz.zone" policy CNAME judicial.dominio.com;
     };
 //...

# OU PARA LOCALHOST

options {
 //...
     response-policy {
       zone "rpz.zone" policy CNAME localhost;
     };
//...

+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

nano /etc/bind/named.conf.local

# Adicionar 

zone "rpz.zone" {
    type master;
    file "/var/cache/bind/rpz/db.rpz.zone.hosts";
    allow-query {none;};
    allow-transfer { XXX.XXX.XXX; };
    also-notify { XXX.XXX.XXX; };
};

XXX.XXX.XXX = IP do DNS Secundário 

RPZ
mkdir /var/cache/bind/rpz/

Criar atalho RPZ
ln -s /var/cache/bind/rpz/ /etc/bind/rpz

# Criar pasta do script
mkdir /etc/bind/scripts

# Acessando pasta
cd /etc/bind/scripts

#Baixando script
wget https://raw.githubusercontent.com/telecomsp/dns-anatel/refs/heads/main/dns-anatel.py

# Dar permissão para executar script 
chmod +x /etc/bind/scripts/dns-anatel.py

# Instalar python e dependencias 
apt install python3 python3-requests tree

#Executar script 
python3 /etc/bind/scripts/dns-anatel.py
