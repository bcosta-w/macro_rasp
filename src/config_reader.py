from log_manager import log_error, log_info

def read_config(file_path):
    try:
        log_info(f"Lendo arquivo de configuração: {file_path}")
        with open(file_path, 'r') as file:
            lines = file.readlines()

        config = {}
        urls = []

        for line in lines:
            line = line.strip()
            if line.startswith("email="):
                config['email'] = line.split('=', 1)[1]
            elif line.startswith("password="):
                config['password'] = line.split('=', 1)[1]
            elif line.startswith("time="):
                config['time'] = int(line.split('=', 1)[1])
            else:
                urls.append(line)

        log_info("Arquivo de configuração lido com sucesso.")
        return config, urls
    except Exception as e:
        log_error(f"Erro ao ler o arquivo de configuração: {e}")
        return {}, []
