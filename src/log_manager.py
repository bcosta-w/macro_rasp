# src/log_manager.py
import logging

def setup_logger():
    """Configura o logger para exibir logs no terminal e armazenar logs de erros em um arquivo."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Formato do log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler para erros
    file_handler = logging.FileHandler('src/logs/error_log.txt')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def log_error(message):
    """Registra um erro no log."""
    logging.error(message)

def log_warn(message):
    """Registra um aviso no log."""
    logging.warning(message)

def log_info(message):
    """Registra uma mensagem informativa no log."""
    logging.info(message)

# Chame a função setup_logger no início do seu script principal
setup_logger()
