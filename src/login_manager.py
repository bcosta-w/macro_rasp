# src/login_manager.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from log_manager import log_error, log_info
import time

def login(driver, email, password):
    try:
        # Acessar a página de login
        driver.get("https://grupowtec.us.qlikcloud.com")

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
        log_info("Login realizado com sucesso.")
    except Exception as e:
        log_error(f"Erro durante o login: {e}")
        return False
    
    return True

def check_login_status(driver):
    try:
        # Verificar se há algum elemento específico que indique que o usuário está logado
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".user-profile")))
        return True
    except Exception:
        return False
