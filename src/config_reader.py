# src/config_reader.py
import json
from log_manager import log_error, log_info

def read_config(file_path):
    try:
        log_info(f"Lendo arquivo de configuração: {file_path}")
        with open(file_path, 'r') as file:
            config = json.load(file)

        urls = config.pop('urls', [])

        log_info("Arquivo de configuração lido com sucesso.")
        return config, urls
    except Exception as e:
        log_error(f"Erro ao ler o arquivo de configuração: {e}")
        return {}, []
