from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from log_manager import log_error, log_info

def check_for_errors(driver):
    try:
        # Verificar por erros específicos na página, como elementos indicando erro
        error_elements_selectors = [
            "#error",  # Seletor genérico para erro
            ".error",  # Classe genérica para erro
            "#network-error",  # Seletor específico para erro de rede
            ".network-error",  # Classe específica para erro de rede
            "body > h1",  # Verificar se há mensagens de erro como "404 Not Found" no título da página
            ".alert",  # Classe genérica para alertas de erro
            ".alert-danger"  # Classe específica para alertas de erro
        ]
        for selector in error_elements_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed() and any(keyword in element.text.lower() for keyword in ["error", "not found", "failed", "unavailable", "denied"]):
                    log_info(f"Erro detectado no seletor: {selector} com a mensagem: {element.text}")
                    return True
            except NoSuchElementException:
                continue

        # Verificar por mensagens de erro de memória no console
        log_entries = driver.get_log('browser')
        for entry in log_entries:
            if 'OutOfMemory' in entry['message']:
                log_info("Erro de memória detectado.")
                return True

        # Verificar o estado do navegador
        if driver.execute_script("return document.readyState") != "complete":
            log_info("Erro detectado: A página não foi carregada completamente.")
            return True

        # Verificar se o navegador está em um estado de erro geral
        if "err_connection" in driver.page_source.lower():
            log_info("Erro de conexão detectado na fonte da página.")
            return True

    except WebDriverException as e:
        log_error(f"Erro de WebDriverException durante a verificação de erros: {e}")
        return True

    return False
