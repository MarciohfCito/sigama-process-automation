# Automação SIGAMA – Coleta e Organização de Solicitações de Acesso

## Visão Geral

Este projeto é uma automação em Python desenvolvida para **operacionalizar o fluxo de coleta, registro e organização de solicitações de acesso no sistema SIGAMA**.
A aplicação automatiza interações gráficas com o navegador e o Excel para:

* Extrair dados (nome e CPF) diretamente da interface do SIGAMA
* Registrar automaticamente essas informações em uma planilha de controle
* Criar uma estrutura de pastas padronizada por data e por solicitante
* Realizar o download e organização dos documentos anexados a cada solicitação
* Garantir consistência operacional por meio de validações de conectividade e estado do ambiente

O projeto é voltado para **Windows**, com uso intensivo de automação de interface gráfica (RPA).

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

---

## Requisitos

* Windows 10 ou superior
* Python 3.x
* Excel 365
* Acesso ao sistema SIGAMA via navegador
* Resolução de tela compatível com as imagens de referência
* Estrutura de pastas de rede configurada (ex: Z:\SIGAMA)

---

## Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

Instale as dependências:

```bash
pip install pyautogui pyperclip openpyxl pandas requests pywin32
```

---

## Estrutura do repositório

O script cria automaticamente a seguinte estrutura:

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

Alguns caminhos estão definidos diretamente no código e devem ser ajustados conforme o ambiente:

* Pasta de downloads do usuário
* Caminho da pasta SIGAMA na rede
* Caminho do arquivo modelo `Controle de Solicitação.xlsx`

---

## Uso

Execute o script:

```bash
python main.py
```

Durante a execução, o sistema solicitará:

```text
Digite o número de registros:
```

Esse valor define quantas solicitações consecutivas serão processadas a partir da tela atual do SIGAMA.

A automação assume que:

* O SIGAMA já está aberto
* A tela inicial está posicionada corretamente
* O primeiro registro visível corresponde ao primeiro processamento

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

## Issues(Algumas a serem resolvidas)

* Dependente de resolução de tela e layout do SIGAMA
* Funciona apenas em Windows
* Não é tolerante a mudanças visuais no sistema SIGAMA
* Requer atenção do operador para posicionamento inicial correto

---

## Boas Práticas de Uso

* Não usar o computador durante a execução
* Garantir conexão estável com a internet
* Não mover janelas durante a automação
* Manter o navegador em tela cheia ou layout conhecido

---

