import win32com.client as win32 #Permite o python interagir com ferramentas do windows, nesse caso com o Excel
from pathlib import Path #Permite analisarmos e manipularmos caminhos no código

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
        print("Pasta {folder} encontrada")
    else:
        print("Pasta {folder} não encontrada")