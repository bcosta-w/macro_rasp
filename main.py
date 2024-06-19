from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import pyautogui

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
        time.sleep(40)

    except Exception as e:
        logging.error(f"Erro durante o login: {e}")
        return False
    
    return True

def open_two_tabs(driver, urls, index):
    # Abrir duas abas
    driver.get(urls[index])
    driver.execute_script("window.open('');")  # Abrir uma nova aba
    driver.switch_to.window(driver.window_handles[1])
    driver.get(urls[(index + 1) % len(urls)])  # Carregar a próxima URL na nova aba
    driver.switch_to.window(driver.window_handles[0])  # Voltar para a primeira aba

def switch_tabs(driver):
    current_tab = driver.current_window_handle
    other_tab = driver.window_handles[0] if driver.window_handles[1] == current_tab else driver.window_handles[1]
    driver.switch_to.window(other_tab)

def detect_and_handle_error(driver):
    try:
        # Adicionar o código para detectar o erro específico aqui
        # Exemplo: Se o elemento de erro tiver o id "error-message"
        error_element = driver.find_element(By.ID, "error-message")
        if error_element.is_displayed():
            logging.error("Erro detectado na tela. Fechando o erro.")
            pyautogui.press('esc')  # Enviar a tecla 'Esc' para fechar o erro
            time.sleep(2)  # Esperar um pouco para garantir que o erro foi fechado
    except Exception as e:
        # Se o elemento de erro não for encontrado, não fazer nada
        pass

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Definir o caminho para o chromedriver
service = Service('/usr/bin/chromedriver')

while True:
    driver = webdriver.Chrome(service=service, options=options)
    try:
        # Ler as configurações e as URLs das páginas a partir do arquivo de configuração
        config, urls = read_config('config.txt')
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
                time.sleep(60)  # Tempo de visualização na aba atual (ajuste conforme necessário)
                driver.get(urls[current_index])  # Recarregar a nova aba ou a mesma URL se não houver mais URLs na lista
                detect_and_handle_error(driver)  # Verificar e fechar erros na tela
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
    time.sleep(15)
