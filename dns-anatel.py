import requests
import datetime
import subprocess
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def create_rpz_zone_file(api_url, output_file):
    """
    Cria um arquivo de zona RPZ com base na resposta da API que retorna uma lista de domínios.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Levanta um erro para respostas HTTP 4xx ou 5xx
        domains = response.json()  # Converte a resposta JSON em uma lista de domínios

        # Gera o número de série com base na data atual
        serial_number = datetime.date.today().strftime("%Y%m%d01")

        # Cria o arquivo de zona RPZ
        with open(output_file, 'w') as file:
            file.write(f"$TTL 1H\n@ IN SOA LOCALHOST. admin.localhost. (\n")
            file.write(f"    {serial_number} ; Serial\n")
            file.write("    1h ; Refresh\n    15m ; Retry\n    30d ; Expire\n    2h ; Negative Cache TTL\n)\n")
            file.write("    NS localhost.\n\n")
            for entry in domains:
                file.write(f"{entry['domain']} IN CNAME .\n")
                file.write(f"{entry['wildcard']} IN CNAME .\n")

        logging.info(f"Arquivo RPZ gerado com sucesso em {output_file}.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar a API: {e}")
        raise  # Levanta novamente a exceção após o log para que o fluxo de execução seja interrompido

    except Exception as e:
        logging.error(f"Erro ao criar o arquivo RPZ: {e}")
        raise

def restart_bind_service():
    """
    Reinicia o serviço Bind9.
    """
    try:
        subprocess.run(['systemctl', 'restart', 'bind9'], check=True)
        logging.info("Serviço Bind9 reiniciado com sucesso.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Falha ao reiniciar o serviço Bind9: {e}")
        raise  # Levanta novamente a exceção para interromper a execução

def test_dns_resolution():
    """
    Executa o comando 'dig uol.com @localhost' para testar a resolução DNS.
    """
    try:
        result = subprocess.run(['dig', 'uol.com', '@localhost'], capture_output=True, text=True, check=True)
        logging.info("Teste de resolução DNS concluído com sucesso.")
        logging.info(f"Saída do comando:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Falha no teste de resolução DNS: {e}")
        logging.error(f"Saída do erro:\n{e.stderr}")
        raise

if __name__ == "__main__":
    API_URL = "https://api.fiber.app.br/list_domains"
    RPZ_FILE = "/var/cache/bind/rpz/db.rpz.zone.hosts"

    try:
        create_rpz_zone_file(API_URL, RPZ_FILE)
        restart_bind_service()
        test_dns_resolution()

    except Exception as e:
        logging.error(f"Erro crítico durante a execução do script: {e}")
        exit(1)  # Encerra o script com código de erro
