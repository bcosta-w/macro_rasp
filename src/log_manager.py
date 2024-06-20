import logging

def setup_logger(log_file, level=logging.INFO):
    """Configura o logger com o nível e o arquivo de log especificados."""
    logging.basicConfig(filename=log_file, level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(message):
    """Registra um erro no log."""
    logging.error(message)

def log_warn(message):
    """Registra um aviso no log."""
    logging.warning(message)

def log_info(message):
    """Registra uma mensagem informativa no log."""
    logging.info(message)
