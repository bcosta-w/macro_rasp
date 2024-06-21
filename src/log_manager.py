import logging

def setup_logger(log_file, level=logging.INFO):
    """Configura o logger com o nível e o arquivo de log especificados."""
    logging.basicConfig(filename=log_file, level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(message):
    """Registra um erro no log."""
    logging.basicConfig(filename='src/logs/error_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.error(message)

def log_warn(message):
    """Registra um aviso no log."""
    logging.basicConfig(filename='src/logs/script_log.txt', level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.warning(message)

def log_info(message):
    """Registra uma mensagem informativa no log."""
    logging.basicConfig(filename='src/logs/script_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(message)
