#Importando bibliotecas
import socket #Para protocolos de rede TCP, no caso o teste de conexão de internet
import requests #Para executar requisições HTTP
import time
from automation.utils.validate import validate_status

def internet_ativa(timeout=10): #Verifica conexão de internet ativa na máquina atual
    try:
        socket.create_connection(("1.1.1.1", 443), timeout=timeout)
        return True
    except OSError:
        return False

def sigama_online(): #Verifica através de requisições básicas se o sistema SIGAMA está online
    try:
        r = requests.get("https://sigama.aged.ma.gov.br/", timeout=10)
        return r.status_code < 500
    except:
        return False

def internet_http(url="https://www.google.com", timeout=10): #Verifica com requisições a conexão com a google, método de verificação da rede
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code == 200
    except requests.RequestException:
        return False

def checar_conectividade(): #Checa a conectividade atráves das funções
    if not internet_ativa():
        return "SEM_INTERNET"
    elif not internet_http():
        return "INTERNET_INSTAVEL"
    elif not sigama_online():
        return "SIGAMA caiu"
    else:
        return "OK"

def reconnect():
    for i in range(5):
        status = checar_conectividade()
        if status == "OK":
            print("internet OK")
            break
        elif status != "OK":
            print("Problema de conexão")
            time.sleep(0.2)
        elif status != "OK" and i == 5:
            print("Encerrando automação")
            return validate_status(status)
