import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from config_reader import read_config
from login_manager import login
from tab_manager import open_two_tabs, switch_tabs

# Configurar o logger
logging.basicConfig(filename='src/logs/script_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')

    log_path = 'src/logs/chromedriver.log'

    while True:
        driver = webdriver.Chrome(options=options)
        try:
            # Ler as configurações e as URLs das páginas a partir do arquivo de configuração
            config, urls = read_config('config/config.txt')
            email = config.get('email')
            password = config.get('password')

            # Realizar login
            if not login(driver, email, password):
                raise Exception("Falha ao realizar o login inicial.")

            # Loop para realizar ações periódicas
            current_index = 0
            open_two_tabs(driver, urls, current_index)

            while True:
                try:
                    time.sleep(10)  # Tempo de visualização na aba atual (ajuste conforme necessário)
                    driver.get(urls[current_index])  # Recarregar a nova aba ou a mesma URL se não houver mais URLs na lista
                    switch_tabs(driver)
                    current_index = (current_index + 1) % len(urls)
                except Exception as e:
                    logging.error(f"Erro ao acessar {urls[current_index]}: {e}")
                    logging.info("Tentando relogar e acessar novamente...")
                    if not login(driver, email, password):
                        logging.error("Falha ao relogar.")
                        break
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
        finally:
            # Fechar o navegador
            driver.quit()

        # Aguarde um pouco antes de reiniciar as rotinas
        time.sleep(10)

if __name__ == "__main__":
    main()
