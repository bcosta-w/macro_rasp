from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging
import threading
from gui_manager import App
from log_manager import log_error, log_info
import time
from config_reader import read_config
from login_manager import login
from tab_manager import open_two_tabs, switch_tabs
import tkinter as tk

# Configurar o logger
logging.basicConfig(filename='src/logs/script_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class SeleniumAutomator:
    def __init__(self, gui_app):
        self.gui_app = gui_app
        self.running = False
        self.driver = None
        self.service = Service('/usr/bin/chromedriver', log_path='src/logs/chromedriver.log')

    def start(self):
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        self.service.start()

        self.running = True
        self.driver = webdriver.Chrome(options=options, service=self.service)

        self.gui_app.update_progress(20)
        self.gui_app.update_log("ChromeDriver iniciado...")

        try:
            config, urls = read_config('src/config/config.txt')
            email = config.get('email')
            password = config.get('password')
            times = config.get('times', [60] * len(urls))  # Default to 60 seconds if no times provided

            self.gui_app.update_progress(40)
            self.gui_app.update_log("Configurações carregadas...")

            if not login(self.driver, email, password):
                raise Exception("Falha ao realizar o login inicial.")

            log_info("Login realizado com sucesso.")
            self.gui_app.update_progress(60)
            self.gui_app.update_log("Login realizado com sucesso...")

            current_index = 0
            open_two_tabs(self.driver, urls, current_index)

            self.gui_app.update_progress(80)
            self.gui_app.update_log("Abas abertas...")

            while self.running:
                try:
                    time.sleep(times[current_index])
                    switch_tabs(self.driver)
                    current_index = (current_index + 1) % len(urls)
                    self.gui_app.update_log(f"Acessando {urls[current_index]}...")
                except Exception as e:
                    log_error(f"Erro ao acessar {urls[current_index]}: {e}")
                    self.gui_app.update_log(f"Erro ao acessar {urls[current_index]}: {e}")
                    if not login(self.driver, email, password):
                        log_error("Falha ao relogar.")
                        self.gui_app.update_log("Falha ao relogar.")
                        break

            self.gui_app.update_progress(100)
            self.gui_app.update_log("Sistema operacional...")

        except Exception as e:
            log_error(f"Erro inesperado: {e}")
            self.gui_app.update_log(f"Erro inesperado: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    def stop(self):
        self.running = False
        if self.driver:
            self.driver.quit()
        if self.service:
            self.service.stop()
        self.gui_app.update_log("Sistema finalizado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)

    def start_automator():
        automator_thread = threading.Thread(target=app.start_system)
        automator_thread.start()

    def stop_automator():
        app.stop_system()

    app.start_system = start_automator
    app.stop_system = stop_automator

    root.mainloop()
