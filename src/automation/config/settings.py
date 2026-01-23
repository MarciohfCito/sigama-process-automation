import os
import sys
from pathlib import Path
from dotenv import load_dotenv # Recebe as variáveis de ambiente

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(BASE_DIR / "keys.env")

def resource_path(rel_path):
    base_path = getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[2])
    return Path(base_path) / rel_path

env_path = resource_path("keys.env")
load_dotenv(env_path)

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

#BASEPATH = Path(os.getenv("SIGAMA_BASEPATH")) #caminho padrão do servidor para acesso e manipulação das pastas e arquivos do projeto, criar e alterar o arquivo .env para conter o SIGAMA_BASEPATH(caminho)
basepath_env = os.getenv("SIGAMA_BASEPATH")

if not basepath_env:
    raise RuntimeError(
        "Variável de ambiente SIGAMA_BASEPATH não definida. "
        "Verifique o arquivo keys.env"
    )

BASEPATH = Path(basepath_env)

LOCAL_BASEPATH = Path(os.getenv("LOCAL_BASEPATH"))
IMAGE_BASEPATH = Path(os.getenv("IMAGES_FOLDER"))

if not BASEPATH:
    raise RuntimeError("BASEPATH não definido no .env")

if not LOCAL_BASEPATH:
    raise RuntimeError("LOCAL_BASEPATH não definido no .env")

DOCUMENTOS_DIR = BASEPATH / "Documentos Solicitaçoes de Acesso"
CONTROLE_EXCEL = BASEPATH / "Controle de Solicitação.xlsx"
DOWNLOADS_DIR = LOCAL_BASEPATH / "Downloads"
IMAGE_DIR = IMAGE_BASEPATH

TIMEOUT = 60
