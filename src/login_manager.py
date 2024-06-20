from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

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

    except Exception as e:
        logging.error(f"Erro durante o login: {e}")
        return False
    
    return True
