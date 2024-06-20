def open_two_tabs(driver, urls, index):
    # Abrir duas abas
    driver.get(urls[index])
    driver.execute_script("window.open('');")  # Abrir uma nova aba
    driver.switch_to.window(driver.window_handles[1])
    driver.get(urls[(index + 1) % len(urls)])  # Carregar a próxima URL na nova aba
    driver.switch_to.window(driver.window_handles[0])  # Voltar para a primeira aba

def switch_tabs(driver):
    current_tab = driver.current_window_handle
    other_tab = driver.window_handles[0] if driver.window_handles[1] == current_tab else driver.window_handles[1]
    driver.switch_to.window(other_tab)
