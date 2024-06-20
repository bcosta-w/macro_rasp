from log_manager import log_error, log_warn, log_info

def open_two_tabs(driver, urls, index):
    try:
        log_info(f"Abrindo duas abas. Índice inicial: {index}")
        driver.get(urls[index])
        driver.execute_script("window.open('');")  # Abrir uma nova aba
        driver.switch_to.window(driver.window_handles[1])
        driver.get(urls[(index + 1) % len(urls)])  # Carregar a próxima URL na nova aba
        driver.switch_to.window(driver.window_handles[0])  # Voltar para a primeira aba
        log_info("Duas abas abertas com sucesso.")
    except Exception as e:
        log_error(f"Erro ao abrir duas abas: {e}")

def switch_tabs(driver):
    try:
        log_info("Alternando entre abas.")
        current_tab = driver.current_window_handle
        other_tab = driver.window_handles[0] if driver.window_handles[1] == current_tab else driver.window_handles[1]
        driver.switch_to.window(other_tab)
        log_info("Alternância entre abas concluída.")
    except Exception as e:
        log_error(f"Erro ao alternar entre abas: {e}")
