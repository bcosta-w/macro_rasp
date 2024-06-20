#!/bin/bash

echo "Iniciando setup."

echo "Criando o diretório de logs."
# Criar o diretório de logs, se não existir
mkdir -p src/logs


# Função para exibir mensagens de erro
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# Instalar Python3
sudo apt update || error_exit "Falha ao atualizar os pacotes."
sudo apt install -y python3 python3-venv python3-pip || error_exit "Falha ao instalar Python3."

# Verificar se virtualenv está instalado, caso contrário, instalar
if ! python3 -m venv --help > /dev/null 2>&1; then
  echo "virtualenv não encontrado. Instalando..."
  sudo apt install -y python3-venv || error_exit "Falha ao instalar python3-venv."
fi

# Criar o ambiente virtual usando python3 -m venv
python3 -m venv venv || error_exit "Falha ao criar o ambiente virtual."

# Ativar o ambiente virtual
source venv/bin/activate || error_exit "Falha ao ativar o ambiente virtual."

# Instalar as dependências no ambiente virtual
pip install -r requirements.txt || error_exit "Falha ao instalar dependências."

echo "Setup concluído."

# Executar o programa usando o interpretador Python do ambiente virtual
echo "Iniciando sistema."
venv/bin/python src/main.py || error_exit "Erro ao iniciar o sistema."

# Desativar o ambiente virtual após a execução
deactivate || error_exit "Erro ao desativar o ambiente virtual."
