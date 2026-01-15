import requests
from automation.utils import connection as c

def test_internet_ativa_socket(monkeypatch): # Testa se a conexão de socket funciona
    monkeypatch.setattr(c.socket, "create_connection", lambda *args, **kwargs: object())
    assert c.internet_ativa() is True

def test_internet_ativa_error(monkeypatch): # Testa se a conexão de socket falha e retorna falso
    def raise_oserror(*args, **kwargs):
        raise OSError("no network")
    monkeypatch.setattr(c.socket, "create_connection", raise_oserror)
    assert c.internet_ativa() is False

class Resp: # Mock de resposta HTTP
    def __init__(self, status_code):
        self.status_code = status_code

def test_sigama_online_true(monkeypatch): # Testa se o site do Sigama está online
    monkeypatch.setattr(c.requests, "get", lambda *a, **k: Resp(200))
    assert c.sigama_online() is True

def test_sigama_online_false(monkeypatch): # Testa se o site do Sigama está offline
    monkeypatch.setattr(c.requests, "get", lambda *a, **k: Resp(503))
    assert c.sigama_online() is False

def test_sigama_online_false_on_exception(monkeypatch): # Testa se o site do Sigama está offline ao ocorrer uma exceção
    def raise_exc(*a, **k):
        raise Exception("boom")
    monkeypatch.setattr(c.requests, "get", raise_exc)
    assert c.sigama_online() is False

def test_internet_http_true(monkeypatch): # Testa se a conexão HTTP funciona
    monkeypatch.setattr(c.requests, "get", lambda *a, **k: Resp(200))
    assert c.internet_http() is True

def test_internet_http_false(monkeypatch): # Testa se a conexão HTTP falha
    monkeypatch.setattr(c.requests, "get", lambda *a, **k: Resp(204))
    assert c.internet_http() is False

def test_internet_http_false_exception(monkeypatch): # Testa se a conexão HTTP falha ao ocorrer uma exceção
    def raise_req_exc(*a, **k):
        raise requests.RequestException("fail")
    monkeypatch.setattr(c.requests, "get", raise_req_exc)
    assert c.internet_http() is False

def test_checar_conectividade_sem_internet(monkeypatch): # Testa o cenário sem internet
    monkeypatch.setattr(c, "internet_ativa", lambda: False)
    # se não tem internet, não importa o resto
    assert c.checar_conectividade() == "SEM_INTERNET"

def test_checar_conectividade_internet_instavel(monkeypatch): # Testa o cenário de internet instável
    monkeypatch.setattr(c, "internet_ativa", lambda: True)
    monkeypatch.setattr(c, "internet_http", lambda: False)
    assert c.checar_conectividade() == "INTERNET_INSTAVEL"

def test_checar_conectividade_sigama_caiu(monkeypatch): # Testa o cenário em que o Sigama está offline
    monkeypatch.setattr(c, "internet_ativa", lambda: True)
    monkeypatch.setattr(c, "internet_http", lambda: True)
    monkeypatch.setattr(c, "sigama_online", lambda: False)
    assert c.checar_conectividade() == "SIGAMA caiu"

def test_checar_conectividade_ok(monkeypatch): # Testa o cenário em que tudo está ok
    monkeypatch.setattr(c, "internet_ativa", lambda: True)
    monkeypatch.setattr(c, "internet_http", lambda: True)
    monkeypatch.setattr(c, "sigama_online", lambda: True)
    assert c.checar_conectividade() == "OK"
