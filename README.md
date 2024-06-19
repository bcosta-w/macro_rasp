# Projeto de Automação de Navegação com Selenium

Este projeto automatiza a navegação de páginas web usando Selenium, com login e navegação configurados a partir de um arquivo de texto.

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Logs](#logs)
- [Contribuição](#contribuição)

## Pré-requisitos

Para rodar este projeto, você precisará de:

- Raspberry Pi com Raspberry Pi OS instalado
- Python 3.7 ou superior
- pip (Python package installer)
- Navegador Chrome ou Chromium
- ChromeDriver compatível com a versão do navegador

## Instalação

Siga as etapas abaixo para configurar o projeto no seu Raspberry Pi.

### 1. Atualizar o sistema

Primeiro, atualize o sistema para garantir que você tenha as últimas atualizações de segurança e pacotes.

```
sudo apt update
sudo apt upgrade
```

### 2. Instalar o Python e pip
Instale Python e pip se ainda não estiverem instalados.

```
sudo apt install python3 python3-pip

```

### 3. Instalar o navegador Chrome/Chromium
Instale o navegador Chromium.

```
sudo apt install chromium-browser


```

### 4. Baixar e instalar o ChromeDriver
Baixe o ChromeDriver compatível com a versão do seu Chromium.

```
sudo apt install chromium-chromedriver



```

### 5. Clonar o repositório do projeto
Clone este repositório no seu Raspberry Pi.
```
git clone https://github.com/bcosta-w/macro_rasp.git

```

```
cd macro_rasp

```

### 6. Instalar as dependências do projeto
Instale as dependências do projeto listadas no arquivo requirements.txt.

```
pip3 install -r requirements.txt

```
## Configuração
Crie um arquivo de configuração config.txt no diretório do projeto com o seguinte formato:

```
email=seu-email@example.com
password=sua-senha
https://example.com/page1
https://example.com/page2
https://example.com/page3

```

Substitua seu-email@example.com e sua-senha pelas suas credenciais de login e adicione as URLs das páginas que deseja automatizar.

## Uso
Para rodar o script, execute o comando:

```
python3 main.py

```

O script tentará realizar o login e navegar pelas URLs configuradas, repetindo o processo indefinidamente e registrando erros em script_log.txt.

## Logs
Os erros e eventos importantes são registrados no arquivo script_log.txt. Você pode verificar este arquivo para solucionar problemas e entender o comportamento do script.

## Contribuição
Contribuições são bem-vindas! Para contribuir com este projeto, siga as etapas abaixo:

-- Faça um fork do repositório

-- Crie uma branch para sua feature/bugfix (git checkout -b feature/nova-feature)

-- Faça commit das suas alterações (git commit -am 'Adiciona nova feature')

-- Faça push para a branch (git push origin feature/nova-feature)

-- Abra um Pull Request

Certifique-se de que suas alterações seguem as boas práticas de codificação e inclua testes quando aplicável.
