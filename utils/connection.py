#Importando bibliotecas
import socket #Para protocolos de rede TCP, no caso o teste de conexão de internet
import requests #Para executar requisições HTTP

def internet_ativa(timeout=5): #Verifica conexão de internet ativa na máquina atual
    try:
        socket.create_connection(("1.1.1.1", 443), timeout=timeout)
        return True
    except OSError:
        return False

def sigama_online(): #Verifica através de requisições básicas se o sistema SIGAMA está online
    try:
        r = requests.get("https://sigama.aged.ma.gov.br/", timeout=5)
        return r.status_code < 500
    except:
        return False

def internet_http(url="https://www.google.com", timeout=5): #Verifica com requisições a conexão com a google, método de verificação da rede
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
