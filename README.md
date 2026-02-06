# Automação SIGAMA – Coleta e Organização de Solicitações de Acesso

## Visão Geral

Este projeto é uma automação em Python desenvolvida para **operacionalizar o fluxo de coleta, registro e organização de solicitações de acesso no sistema SIGAMA**.
A aplicação automatiza interações gráficas com o navegador e o Excel para:

* Extrair dados (nome e CPF) diretamente da interface do SIGAMA
* Registrar automaticamente essas informações em uma planilha de controle
* Criar uma estrutura de pastas padronizada por data e por solicitante
* Realizar o download e organização dos documentos anexados a cada solicitação
* Garantir consistência operacional por meio de validações de conectividade e estado do ambiente

O projeto é voltado para **Windows** e testado no **Google Chrome** e **Firefox**, com uso intensivo de automação de interface gráfica (RPA).

---

## Funcionalidades Principais

* Verificação de conectividade:

  * Internet ativa (socket)
  * Estabilidade HTTP
  * Disponibilidade do SIGAMA
* Fechamento seguro do Excel caso esteja aberto
* Criação automática de estrutura de diretórios por:

  * Ano
  * Mês (nome por extenso)
  * Dia
* Cópia de planilha modelo de controle diário
* Leitura automática de nome e CPF diretamente da tela do SIGAMA
* Escrita incremental no Excel sem sobrescrever dados
* Criação de pasta individual para cada solicitante
* Download automático de documentos anexados
* Organização dos arquivos baixados na pasta correta
* Controle de timeout e falhas de download
* Abertura automática da pasta e da planilha ao final da execução

---

## Tecnologias

### Linguagem

* Python 3.x

### Bibliotecas utilizadas

* pyautogui – automação de interface gráfica
* pyperclip – manipulação da área de transferência
* openpyxl – leitura e escrita em arquivos Excel
* pandas – manipulação de dados em planilhas
* requests – verificação de conectividade HTTP
* win32com.client – automação do Microsoft Excel
* pathlib – manipulação de caminhos
* shutil – cópia e movimentação de arquivos
* socket – verificação de conectividade de rede
* python-dotenv – leitura de variáveis de ambiente (`load_dotenv`)
* PySide6 – interface gráfica (Qt)

---

## Instalação

### Pré-requisitos
- Windows 10+ (recomendado)
- Python 3.10+ (recomendado)
- Excel 365
- Acesso ao SIGAMA via navegador
- Resolução de tela compatível com as imagens de referência
- Navegador de internet (Chrome, Firefox ou Edge)

### Clonar o repositório
```bash
git clone https://github.com/MarciohfCito/sigama-process-automation
cd sigama-process-automation
```

### Criar e ativar um ambiente virtual (recomendado)
Windows (PowerShell):
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows (CMD):
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Instale as dependências:

Este projeto usa pyproject.toml. A forma recomendada é instalar o pacote em modo desenvolvimento:

```bash
pip install -U pip
pip install -e .
```

### Configurar variáveis de ambiente
A automação depende do caminho base do servidor/rede. Configure a variável:

SIGAMA_BASEPATH (exemplo: Z:\SIGAMA)

Você pode configurar de 2 formas:

Variável no terminal:

Windows (PowerShell):
```bash
$env:SIGAMA_BASEPATH="Z:\SIGAMA"
```

Windows (CMD):
```bash
set SIGAMA_BASEPATH=Z:\SIGAMA
```

Arquivo de ambiente (recomendado):
Crie um arquivo keys.env (ou .env) e defina:

```bash
SIGAMA_BASEPATH=Z:\SIGAMA
LOCAL_BASEPATH=<SEU_USUARIO_DO_WINDOWS>
IMAGE_FOLDER=<PASTA_image_EM_SRC>
```

---

## Estrutura do repositório

```
└── sigama-process-automation
  ├── pyproject.toml
  ├── README.md
  ├── .gitignore
  ├── src
  │   └── automation
  │       ├── __init__.py
  │       ├── main.py
  │       ├── config
  │       │   ├── __init__.py
  │       │   └── settings.py
  │       ├── core
  │       │   ├── __init__.py
  │       │   ├── controller.py
  │       │   ├── pipeline.py
  │       │   ├── services.py
  │       │   └── worker.py
  │       ├── image
  │       └── ui
  │           ├── __init__.py
  │           ├── app.py
  │           ├── main_window.py
  │           ├── view_model.py
  │           └── resources
  │               └── main_window.ui
  │       └── utils
  │           ├── __init__.py
  │           ├── connection.py
  │           ├── filesystem.py
  │           ├── input.py
  │           ├── position.py
  │           └── validate.py
  └── tests
    └── unit
      ├── test_connection.py
      ├── test_filesystem.py
      ├── test_input.py
      ├── test_position.py
      └── test_validate.py
```

## Estrutura de saída esperada

O script cria automaticamente a seguinte estrutura no servidor:

```
Z:\SIGAMA\Documentos Solicitaçoes de Acesso\
 └── Ano
     └── Mês
         └── Dia
             ├── Controle de Solicitação.xlsx
             ├── Nome - CPF
             │   ├── documento1.pdf
             │   ├── documento2.pdf
```

---

## Configuração Necessária

### Imagens de Referência

O diretório `./image/` deve conter as imagens usadas para reconhecimento de tela:

* nome_image.png
* cpf_image.png
* operacoes_image.png
* anexo_image.png
* X_image.png

Essas imagens são essenciais para o funcionamento da automação.

### Caminhos Padrão

Alguns caminhos estão definidos diretamente no código e pode existir necessidade de serem ajustados conforme o ambiente:

* Pasta de downloads do usuário
* Caminho da pasta SIGAMA na rede
* Caminho do arquivo modelo `Controle de Solicitação.xlsx`

---

## Uso

Execute o script no terminal localizado em <.\sigama-process-automation\src\automation\ui>:

```bash
python app.py
```

Aplicação funcionando:



Durante a execução, o sistema solicitará:

```text
Digite o número de registros:
```

Esse valor define quantas solicitações consecutivas serão processadas a partir da tela atual do SIGAMA.

A automação assume que:

* O SIGAMA já está aberto
* A tela inicial está posicionada corretamente
* O primeiro registro visível corresponde ao primeiro processamento

Caso ocorra algum problema ajuste o ambiente de funcionamento de acordo com o log de erro explicitado, caso 

---

## Fluxo de Execução(Pipeline)

1. Validação de internet e SIGAMA
2. Fechamento do Excel se estiver aberto
3. Criação da pasta do dia
4. Cópia da planilha modelo
5. Leitura de nome e CPF via interface gráfica
6. Registro no Excel
7. Criação da pasta do solicitante
8. Download dos anexos
9. Organização dos documentos
10. Avanço automático para o próximo registro

---

## Rodar testes unitários
Rode esse comando na raiz do projeto:

```bash
pytest -q tests/unit
```

Ou se quiser rodar apenas um teste específico:

```bash
pytest -q tests/unit/test_especifico
```

---

## Issues(Algumas a serem resolvidas)

* Dependente de resolução de tela e layout do SIGAMA
* Funciona apenas em Windows
* Não é tolerante a mudanças visuais no sistema SIGAMA
* Requer atenção do operador para posicionamento inicial correto
* Configurações de download do navegador: certifique-se de usar a pasta de `Downloads` padrão, desativar a opção de perguntar onde salvar cada arquivo (para não abrir a janela de seleção de caminho) e desativar a abertura automática de arquivos após o download.

---

## Boas Práticas de Uso

* Não usar o computador durante a execução
* Garantir conexão estável com a internet
* Não mover janelas durante a automação
* Manter ampliação do navegador em 100%(Padrão)
* Manter o navegador em tela cheia ou layout conhecido

---

