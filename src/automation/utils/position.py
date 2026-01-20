import pyautogui
# Abaixo bibliotecas chamadas pelos testes unitários
import time
from datetime import datetime, date, timedelta
from pathlib import Path #Permite analisarmos e manipularmos caminhos no código

from automation.utils.validate import validate_download, validate_downloads_folder

def get_name_positions(IMAGE_DIR):
    arquivo = Path(IMAGE_DIR) / "nome_image.png"
    PNx, PNy = pyautogui.locateCenterOnScreen(str(arquivo), confidence= 0.6)
    final_position = [PNx, PNy + 40] # hardcoded due to software layout// hardcoded por causa do layout do software
    
    return final_position

def get_cpf_positions(IMAGE_DIR):
    arquivo = Path(IMAGE_DIR) / "cpf_image.png"
    PCx, PCy = pyautogui.locateCenterOnScreen(str(arquivo), confidence= 0.5)
    final_position = [PCx, PCy + 40] # hardcoded due to software layout// hardcoded por causa do layout do software
    
    return final_position

def get_lupa_position(IMAGE_DIR):
    arquivo = Path(IMAGE_DIR) / "operacoes_image.png"
    PLx, PLy = pyautogui.locateCenterOnScreen(str(arquivo), confidence= 0.5)
    final_position = [PLx + 52, PLy + 34] # hardcoded due to software layout// hardcoded por causa do layout do software

    return final_position

def get_docs_position(IMAGE_DIR):
    arquivo = Path(IMAGE_DIR) / "anexo_image.png"
    pyautogui.moveTo(pyautogui.locateCenterOnScreen(str(arquivo), confidence = 0.8))
    x1, y1 = pyautogui.locateCenterOnScreen(str(arquivo), confidence = 0.8)
    x1 = x1 - 25

    return x1, y1

def get_documents(x1, y1, files_directory, DOCUMENTOS_DIR, ano, mes, dia, nome_cpf_tratado, IMAGE_DIR):
    pyautogui.moveTo(x1, y1+27)
    for i in range(5):
        y1 = y1+23
        pyautogui.moveTo(x1, y1)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.2)
    #validate_downloads_folder(files_directory)
    time.sleep(0.2)
    arquivo = Path(IMAGE_DIR) / "X_image.png"
    pyautogui.click(pyautogui.locateCenterOnScreen(str(arquivo), confidence = 0.8))

    #Colocar documentos na pasta
    destino = Path(DOCUMENTOS_DIR, str(ano), str(mes), str(dia), nome_cpf_tratado)
    
    #hoje = date.today() -> não usado
    agora = datetime.now()

    #identificar erro no diretório de arquivos
    validate_download(files_directory, agora, destino)