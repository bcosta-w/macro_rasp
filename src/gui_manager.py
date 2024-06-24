import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from config_reader import read_config
from log_manager import log_error, log_info
import threading
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de URLs e Login")

        self.config_file = 'src/config/config.txt'
        self.email = ""
        self.password = ""
        self.urls = []
        self.times = []
        self.automator = None

        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.login_frame = ttk.Frame(self.notebook)
        self.urls_frame = ttk.Frame(self.notebook)
        self.control_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.login_frame, text='Login')
        self.notebook.add(self.urls_frame, text='URLs')
        self.notebook.add(self.control_frame, text='Controle')

        self.setup_login_ui()
        self.setup_urls_ui()
        self.setup_control_ui()

    def setup_login_ui(self):
        ttk.Label(self.login_frame, text="Email:").pack(padx=10, pady=5)
        self.email_entry = ttk.Entry(self.login_frame, width=50)
        self.email_entry.pack(padx=10, pady=5)

        ttk.Label(self.login_frame, text="Senha:").pack(padx=10, pady=5)
        self.password_entry = ttk.Entry(self.login_frame, width=50, show='*')
        self.password_entry.pack(padx=10, pady=5)

        self.save_login_button = ttk.Button(self.login_frame, text="Salvar Login", command=self.save_login)
        self.save_login_button.pack(pady=10)

    def setup_urls_ui(self):
        ttk.Label(self.urls_frame, text="Adicionar URL:").pack(padx=10, pady=5)
        self.url_entry = ttk.Entry(self.urls_frame, width=50)
        self.url_entry.pack(padx=10, pady=5)

        ttk.Label(self.urls_frame, text="Tempo de permanência (s):").pack(padx=10, pady=5)
        self.time_entry = ttk.Entry(self.urls_frame, width=50)
        self.time_entry.pack(padx=10, pady=5)

        self.add_url_button = ttk.Button(self.urls_frame, text="Adicionar URL", command=self.add_url)
        self.add_url_button.pack(pady=10)

        self.url_list_frame = ttk.Frame(self.urls_frame)
        self.url_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.url_listbox = tk.Listbox(self.url_list_frame, height=10, selectmode=tk.SINGLE)
        self.url_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.url_list_frame, orient=tk.VERTICAL, command=self.url_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.url_listbox.config(yscrollcommand=self.scrollbar.set)

        self.url_listbox.bind("<Double-1>", self.remove_url)

    def setup_control_ui(self):
        self.progress = ttk.Progressbar(self.control_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=10)

        self.start_button = ttk.Button(self.control_frame, text="Iniciar Sistema", command=self.start_system)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.control_frame, text="Parar Sistema", command=self.stop_system)
        self.stop_button.pack(pady=10)

        self.log_text = tk.Text(self.control_frame, state='disabled', height=15)
        self.log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def load_config(self):
        self.config, self.urls = read_config(self.config_file)
        self.email = self.config.get('email', '')
        self.password = self.config.get('password', '')
        self.times = self.config.get('times', [0] * len(self.urls))

        self.email_entry.insert(0, self.email)
        self.password_entry.insert(0, self.password)

        self.refresh_url_list()

    def save_login(self):
        self.email = self.email_entry.get()
        self.password = self.password_entry.get()
        self.save_config()
        messagebox.showinfo("Sucesso", "Email e senha salvos com sucesso.")

    def add_url(self):
        new_url = self.url_entry.get()
        new_time = self.time_entry.get()
        if new_url and new_time.isdigit():
            self.urls.append(new_url)
            self.times.append(int(new_time))
            self.refresh_url_list()
            self.save_config()
            self.url_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)

    def remove_url(self, event):
        selected_index = self.url_listbox.curselection()
        if selected_index:
            del self.urls[selected_index[0]]
            del self.times[selected_index[0]]
            self.refresh_url_list()
            self.save_config()

    def refresh_url_list(self):
        self.url_listbox.delete(0, tk.END)
        for url, time in zip(self.urls, self.times):
            self.url_listbox.insert(tk.END, f"{url} - {time}s")

    def save_config(self):
        try:
            with open(self.config_file, 'w') as file:
                file.write(f"email={self.email}\n")
                file.write(f"password={self.password}\n")
                for url, time in zip(self.urls, self.times):
                    file.write(f"{url},{time}\n")
            log_info("Configuração salva com sucesso.")
        except Exception as e:
            log_error(f"Erro ao salvar configuração: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar configuração: {e}")

    def start_system(self):
        if not self.automator:
            from main import SeleniumAutomator
            self.automator = SeleniumAutomator(self)

        self.progress['value'] = 0
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        self.update_log("Iniciando sistema...")

        automator_thread = threading.Thread(target=self.automator.start)
        automator_thread.start()

    def stop_system(self):
        if self.automator:
            self.automator.stop()
            self.progress['value'] = 0
            self.update_log("Sistema parado.")
            self.clear_logs()

    def update_log(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')

    def clear_logs(self):
        try:
            with open('src/logs/script_log.txt', 'w') as log_file:
                log_file.truncate()
            self.update_log("Logs apagados.")
        except Exception as e:
            log_error(f"Erro ao apagar logs: {e}")
            messagebox.showerror("Erro", f"Erro ao apagar logs: {e}")

    def update_progress(self, value):
        self.progress['value'] = value

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
