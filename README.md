# dns-anatel

Automação em Python para Sincronização de RPZ (Response Policy Zone), desenvolvida para garantir que servidores DNS BIND9 possam aplicar automaticamente as políticas de bloqueio de domínios conforme solicitado pela ANATEL (Agência Nacional de Telecomunicações).

## Configuração

#### 1. Configuração do BIND9

#### Adicionar dentro de `options` para mandar para domínio ou localhost.

Edite o arquivo `/etc/bind/named.conf.options`:

```bash
nano /etc/bind/named.conf.options
```

Adicione a configuração de response-policy:

Para domínio:

```bash
options {
  //...

  response-policy {
    zone "rpz.zone" policy CNAME judicial.dominio.com;
  };

  //...
}
```

Adicione a configuração de response-policy:

Para domínio:
```bash
options {
  //...

  response-policy {
    zone "rpz.zone" policy CNAME localhost;
  };

  //...
}
```

#### 2. Configuração de Zona no BIND9
Edite o arquivo /etc/bind/named.conf.local:
```bash
nano /etc/bind/named.conf.local
```
Adicione a configuração de zona:
```bash
zone "rpz.zone" {
    type master;
    file "/var/cache/bind/rpz/db.rpz.zone.hosts";
    allow-query {none;};
    allow-transfer { XXX.XXX.XXX; };
    also-notify { XXX.XXX.XXX; };
};
```
Nota: Substitua XXX.XXX.XXX pelo IP do DNS Secundário.

#### 3. Criação de Pastas e Links
Crie as pastas necessárias:
```bash
mkdir /var/cache/bind/rpz/
ln -s /var/cache/bind/rpz/ /etc/bind/rpz
mkdir /etc/bind/scripts
```
#### 4. Baixando e Configurando o Script e dando permissão para executar. 
```bash
cd /etc/bind/scripts
```
```bash
wget https://raw.githubusercontent.com/telecomsp/dns-anatel/refs/heads/main/dns-anatel.py
chmod +x /etc/bind/scripts/dns-anatel.py
```
#### 5. Instalar Dependências
Instale o Python e as dependências necessárias:
```bash
apt install python3 python3-requests tree
```
#### 6. Executando o Script
Por fim, execute o script:
```bash
python3 /etc/bind/scripts/dns-anatel.py
```

#### 7. Crie o cron para rodar a cada 1 hora e reinicie o cron.
```bash
echo '0 * * * * root python3 /etc/bind/scripts/dns-anatel.py' >> /etc/crontab
systemctl restart cron
```
## Contribuições
Se você deseja contribuir com este projeto, fique à vontade para fazer um fork e abrir pull requests com melhorias ou correções! 

Licença
Este projeto está licenciado sob a Licença MIT.
```bash
Esse conteúdo está formatado corretamente para o GitHub, com seções e código bem organizados. A estrutura também segue boas práticas para facilitar a instalação e configuração do projeto.
```
