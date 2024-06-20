Aqui está a versão atualizada do arquivo `README.md` com base nas informações fornecidas:

---

# Projeto de Automação de Navegação com Selenium

Este projeto automatiza a navegação de páginas web usando Selenium, com login e navegação configurados a partir de um arquivo de texto.

## Sumário

- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Logs](#logs)
- [Contribuição](#contribuição)

## Instalação

Siga as etapas abaixo para configurar o projeto no seu Raspberry Pi.

### 1. Instalar o navegador Chrome/Chromium
Instale o navegador Chromium.

```bash
sudo apt install chromium-browser
```

### 2. Baixar e instalar o ChromeDriver
Baixe o ChromeDriver compatível com a versão do seu Chromium.

```bash
sudo apt install chromium-chromedriver
```

### 3. Clonar o repositório do projeto
Clone este repositório no seu Raspberry Pi.

```bash
git clone https://github.com/bcosta-w/macro_rasp.git
cd macro_rasp
```

### 4. Iniciar o setup.sh
Inicie o setup automático do sistema.

```bash
./setup.sh
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

Substitua `seu-email@example.com` e `sua-senha` pelas suas credenciais de login e adicione as URLs das páginas que deseja automatizar.

## Uso
O script tentará realizar o login e navegar pelas URLs configuradas, repetindo o processo indefinidamente e registrando erros em script_log.txt.

## Logs
Os erros e eventos importantes são registrados no arquivo script_log.txt. Você pode verificar este arquivo para solucionar problemas e entender o comportamento do script.

## Contribuição
Contribuições são bem-vindas! Para contribuir com este projeto, siga as etapas abaixo:

- Faça um fork do repositório
- Crie uma branch para sua feature/bugfix (`git checkout -b feature/nova-feature`)
- Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`)
- Faça push para a branch (`git push origin feature/nova-feature`)
- Abra um Pull Request

Certifique-se de que suas alterações seguem as boas práticas de codificação e inclua testes quando aplicável.

---

Espero que isso ajude a melhorar a documentação do seu projeto! Se precisar de mais alguma coisa, é só avisar.
