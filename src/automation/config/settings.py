import os
from pathlib import Path
from dotenv import load_dotenv # Recebe as variáveis de ambiente

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "keys.env")

#print(teste)
#print(BASE_DIR)

#RESOLUCOES = {
#    (3840, 2160): config_4k,
#    (1920, 1080): config_fullhd,
#    (1366, 768): config_hd,
#    (1280, 720): config_hdready,
#}

#vscode_4k = VSCodeConfig(minimizar_x=3720, minimizar_y=10)
#vscode_fullhd = VSCodeConfig(minimizar_x=1806, minimizar_y=7)
#vscode_hd = VSCodeConfig(minimizar_x=1350, minimizar_y=7)
#vscode_hdready = VSCodeConfig(minimizar_x=1250, minimizar_y=7)

#as configs de app receberão os itens do dicionario para acertar os parametros

BASEPATH = Path(os.getenv("SIGAMA_BASEPATH")) #caminho padrão do servidor para acesso e manipulação das pastas e arquivos do projeto, criar e alterar o arquivo .env para conter o SIGAMA_BASEPATH(caminho)
LOCAL_BASEPATH = Path(os.getenv("LOCAL_BASEPATH"))

if not BASEPATH:
    raise RuntimeError("BASEPATH não definido no .env")

if not LOCAL_BASEPATH:
    raise RuntimeError("LOCAL_BASEPATH não definido no .env")

DOCUMENTOS_DIR = BASEPATH / "Documentos Solicitaçoes de Acesso"
CONTROLE_EXCEL = BASEPATH / "Controle de Solicitação.xlsx"
DOWNLOADS_DIR = LOCAL_BASEPATH / "Downloads"

TIMEOUT = 60
