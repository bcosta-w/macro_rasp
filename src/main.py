# src/main.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging
import time
from config_reader import read_config
from login_manager import login
from tab_manager import open_two_tabs, switch_tabs
from log_manager import log_error, log_info
from error_handler import check_for_errors

# Configurar o logger
logging.basicConfig(filename='src/logs/script_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class SeleniumAutomator:
    def __init__(self):
        self.running = False
        self.service = Service('/usr/bin/chromedriver', log_path='src/logs/chromedriver.log')

    def start(self):
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        self.service.start()

        self.running = True
        self.driver = webdriver.Chrome(options=options, service=self.service)

        log_info("ChromeDriver iniciado...")

        try:
            self.run_automation_cycle()
        except Exception as e:
            log_error(f"Erro inesperado: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    def run_automation_cycle(self):
        while self.running:
            try:
                config, urls = read_config('src/config/config.json')
                email = config.get('email')
                password = config.get('password')
                time_per_url = config.get('time', 10)  # Default to 60 seconds if no time provided

                log_info("Configurações carregadas...")

                if not login(self.driver, email, password):
                    raise Exception("Falha ao realizar o login inicial.")

                log_info("Login realizado com sucesso.")

                current_index = 0
                open_two_tabs(self.driver, urls, current_index)

                log_info("Abas abertas...")

                while self.running:
                    try:
                        time.sleep(time_per_url)
                        switch_tabs(self.driver)
                        current_index = (current_index + 1) % len(urls)
                        log_info(f"Acessando {urls[current_index]}...")

                        if check_for_errors(self.driver):
                            raise Exception("Erro detectado na tela.")

                    except Exception as e:
                        log_error(f"Erro ao acessar {urls[current_index]}: {e}")
                        log_info("Reiniciando o ciclo de automação...")
                        break

                log_info("Sistema operacional...")

            except Exception as e:
                log_error(f"Erro inesperado: {e}")
            finally:
                if self.driver:
                    self.driver.quit()
                if self.running:
                    log_info("Reiniciando o navegador...")
                    self.driver = webdriver.Chrome(options=Options().add_argument('--start-maximized').add_argument('--no-sandbox'), service=self.service)

    def stop(self):
        self.running = False
        if self.driver:
            self.driver.quit()
        if self.service:
            self.service.stop()
        log_info("Sistema finalizado.")

if __name__ == "__main__":
    from log_manager import setup_logger
    setup_logger()
    
    automator = SeleniumAutomator()

    try:
        automator.start()
    except KeyboardInterrupt:
        automator.stop()
