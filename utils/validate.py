import time
import sys
import win32com.client as win32 #Permite o python interagir com ferramentas do windows, nesse caso com o Excel
import pyautogui
from datetime import datetime, date, timedelta
from pathlib import Path #Permite analisarmos e manipularmos caminhos no código
import os

def validate_status(status):
    if status != "OK":
        print(f"Problema de conexão: {status}")
        sys.exit()

def validate_resolution():
    largura, altura = pyautogui.size()
    resolucao = str(largura) + "x" + str(altura)
    print(f"A resolução da tela é {resolucao}")
    return resolucao

def validate_excel(): #Valida se a aplicação MExcel está aberta. Se sim, salva o arquivo automaticamente e o fecha. Se não, retorna o aviso
    try:
        excel = win32.GetActiveObject("Excel.Application")
        print("Excel aberto encontrado")

        for wb in excel.Workbooks:
            if not wb.Saved:
                wb.Save()
                print(f"Salvo: {wb.Name}")

        excel.Quit()
        print("Excel fechado com sucesso")

    except Exception:
        print("Excel não está aberto")

def validate_folders(folder): #Valida a existência das pastas chamadas
    if folder.exists(): #método .exists pertence a biblioteca 
        print(f"Pasta {folder} encontrada")
    else:
        print(f"Pasta {folder} não encontrada")

def validate_download(files_directory, timeout=60): #Valida o download e aguarda um tempo padrão para iniciar o carregamento
    inicio = time.time()
    arquivos_iniciais = set(os.listdir(files_directory))

    while True:
        arquivos_atuais = set(os.listdir(files_directory))
        novos_arquivos = arquivos_atuais - arquivos_iniciais

        for arquivo in novos_arquivos:
            if not arquivo.endswith('.crdownload'):
                return os.path.join(files_directory, arquivo)
        
        if time.time() - inicio > timeout:
            raise TimeoutError('Nenhum download detectado')

def validade_date(): #Valida a data para a automação
    data_atual = datetime.today()

    dia = data_atual.strftime("%d")
    mes = data_atual.month
    ano = data_atual.strftime("%Y")

    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }

    mes_nome = meses[mes]

    print(dia, mes_nome, ano)

    return dia, mes_nome, ano

def validate_input(entrada): #Valida a entrada de dados numéricos
    if not entrada.isdigit():
        raise ValueError("Valor digitado precisa ser um inteiro.")

    num = int(entrada)

    if num <= 0:
        raise ValueError("O número deve ser maior que zero.")

    return num

def validate_vscode(): #Valida se o vscode está aberto(Rodando o código) e minimiza. Essa função provavelmente será removida quando for transformado em executável.
    pyautogui.moveTo(pyautogui.moveTo(x=1806, y=7)) # Por enquanto só funciona em 1920x1080
    pyautogui.click()
    time.sleep(0.5)