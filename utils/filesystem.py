#Importando bibliotecas
from pathlib import Path
import shutil #Para copiar as pastas geradas

def create_directory(base_dir, ano, mes, dia):
    pasta = base_dir / str(ano) / str(mes) / str(dia)
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta

def copy_excel_file(origem, destino):
    destino_arquivo = destino / origem.name
    if not destino_arquivo.exists(): #Não é necessário extrair essa função já que não será reutilizada
        shutil.copy(origem, destino)
        return True
    return False
