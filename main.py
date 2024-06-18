from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Configurar o logger
logging.basicConfig(filename='script_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def read_config(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    config = {}
    urls = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("email="):
            config['email'] = line.split('=', 1)[1]
        elif line.startswith("password="):
            config['password'] = line.split('=', 1)[1]
        else:
            urls.append(line)
    
    return config, urls

def login(driver, email, password):
    try:
        # Acessar a página de login
        driver.get("https://grupowtec.us.qlikcloud.com/single/?appid=57891e3e-7901-407c-a1f2-f0e5668c265f&sheet=932f8724-a761-4cf0-9354-168ea942d2c9&theme=card&opt=nointeraction,noselections&identity=preview")

        # Esperar até que os campos de login estejam presentes e visíveis
        wait = WebDriverWait(driver, 30)
        username_input = wait.until(EC.visibility_of_element_located((By.NAME, "email")))
        password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))

        # Preencher os campos de login
        username_input.send_keys(email)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)  # Pressionar Enter para enviar o formulário

        # Aguardar o carregamento da página após o login
        time.sleep(20)

    except Exception as e:
        logging.error(f"Erro durante o login: {e}")
        return False
    
    return True

# Configurar opções do navegador para rodar no modo headless (sem interface gráfica)
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

while True:
    driver = webdriver.Chrome(options=options)
    try:
        # Ler as configurações e as URLs das páginas a partir do arquivo de configuração
        config, urls = read_config('config.txt')
        email = config.get('email')
        password = config.get('password')

        # Realizar login
        if not login(driver, email, password):
            raise Exception("Falha ao realizar o login inicial.")

        # Loop para realizar ações periódicas
        while True:
            for url in urls:
                try:
                    driver.get(url)
                    time.sleep(10)  # Aguardar o carregamento da página (ajuste conforme necessário)
                except Exception as e:
                    logging.error(f"Erro ao acessar {url}: {e}")
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
    time.sleep(30)
