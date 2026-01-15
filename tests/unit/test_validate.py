import pytest
import os
from pathlib import Path
from automation.utils import validate as v

def test_validate_status_success(capsys): # Se retornar "OK", não deve imprimir nada nem sair
    v.validate_status("OK")
    out = capsys.readouterr().out
    assert out == ""

def test_validate_status_error(capsys): # Se retornar diferente de "OK", deve imprimir a mensagem e sair
    with pytest.raises(SystemExit):
        v.validate_status("ERRO")

    out = capsys.readouterr().out
    assert "Problema de conexão" in out
    assert "ERRO" in out

def test_validate_resolution(monkeypatch, capsys): # Se a resolução for 1920x1080, deve retornar essa string e imprimir a mensagem correta
    monkeypatch.setattr(v.pyautogui, "size", lambda: (1920, 1080)) # O Mocking substitui o método size para retornar 1920x1080, válido para o teste

    res = v.validate_resolution()

    assert res == "1920x1080"
    out = capsys.readouterr().out
    assert "A resolução da tela é 1920x1080" in out

# As classes a seguir também são mocks para simular o comportamento do Excel no teste
class FakeWB:
    def __init__(self, name, saved):
        self.Name = name
        self.Saved = saved
        self.saved_called = False

    def Save(self):
        self.saved_called = True
        self.Saved = True

class FakeExcel:
    def __init__(self, workbooks):
        self.Workbooks = workbooks
        self.quit_called = False

    def Quit(self):
        self.quit_called = True

def test_validate_excel(monkeypatch, capsys): # Se o Excel estiver aberto, deve salvar os arquivos não salvos e fechar o Excel
    wb1 = FakeWB("A.xlsx", saved=False)
    wb2 = FakeWB("B.xlsx", saved=True)
    excel = FakeExcel([wb1, wb2])

    monkeypatch.setattr(v.win32, "GetActiveObject", lambda _: excel)

    v.validate_excel()

    assert wb1.saved_called is True
    assert wb2.saved_called is False
    assert excel.quit_called is True

    out = capsys.readouterr().out
    assert "Excel aberto encontrado" in out
    assert "Salvo: A.xlsx" in out
    assert "Excel fechado com sucesso" in out

def test_validate_excel_error(monkeypatch, capsys): # Se o Excel não estiver aberto, deve imprimir a mensagem correta
    def raise_exc(_):
        raise Exception("no excel")
    monkeypatch.setattr(v.win32, "GetActiveObject", raise_exc)

    v.validate_excel()

    out = capsys.readouterr().out
    assert "Excel não está aberto" in out


def test_validate_folders_exists(tmp_path, capsys): # Se a pasta existir, deve imprimir a mensagem correta
    folder = tmp_path / "pasta"
    folder.mkdir()

    v.validate_folders(folder)

    out = capsys.readouterr().out
    assert "encontrada" in out

def test_validate_folders_not_exists(tmp_path, capsys): # Se a pasta não existir, deve imprimir a mensagem digitada
    folder = tmp_path / "nao_existe"

    v.validate_folders(folder)

    out = capsys.readouterr().out
    assert "não encontrada" in out

def test_validate_downloads_folder(monkeypatch, tmp_path):
    downloads = tmp_path
    # simular listdir mudando ao longo do tempo
    calls = {"n": 0}

    def fake_listdir(_):
        calls["n"] += 1
        if calls["n"] == 1:
            return ["a.tmp"]
        return ["a.tmp", "novo.pdf"]

    # simular tempo sempre dentro do timeout
    t = {"now": 0.0}
    def fake_time():
        t["now"] += 1.0
        return t["now"]

    monkeypatch.setattr(v.os, "listdir", fake_listdir)
    monkeypatch.setattr(v.time, "time", fake_time)

    found = v.validate_downloads_folder(str(downloads), timeout=60)

    assert found.endswith(os.path.join(str(downloads), "novo.pdf"))


def test_validate_downloads_folder_times_out(monkeypatch, tmp_path):
    monkeypatch.setattr(v.os, "listdir", lambda _: ["a.tmp"])

    # tempo vai passar rápido além do timeout
    times = iter([0.0, 1000.0])
    monkeypatch.setattr(v.time, "time", lambda: next(times))

    with pytest.raises(TimeoutError):
        v.validate_downloads_folder(str(tmp_path), timeout=1)

def test_validade_date(): # Se passar deve retornar dia, mês (string) e ano corretamente
    dia, mes_nome, ano = v.validade_date()
    assert len(dia) == 2
    assert isinstance(mes_nome, str)
    assert len(ano) == 4

def test_validate_input(): # Se a entrada for um número válido, deve retornar o número como inteiro
    assert v.validate_input("10") == 10

@pytest.mark.parametrize("entrada", ["abc", "10.5", "-1", ""]) # Mock de entradas inválidas para testar ValueError
def test_validate_input_wrong(entrada):
    with pytest.raises(ValueError):
        v.validate_input(entrada)

def test_validate_input_zero_or_negative(): # Testa se a entrada é zero ou negativa
    with pytest.raises(ValueError):
        v.validate_input("0")

def test_validate_click_single(monkeypatch): # Testa se o clique é realizado corretamente para entrada "1", teoricamente não é necessário
    called = {"x": 0}                        # os outros pois, se funcionar para 1, funciona para os demais. Além disso, tem um teste para os inválidos
    monkeypatch.setattr(v.pyautogui, "click", lambda: called.__setitem__("x", called["x"] + 1))
    v.validate_click("1")
    assert called["x"] == 1

def test_validate_click_invalid_raises(): # Testa se a entrada inválida levanta ValueError
    with pytest.raises(ValueError):
        v.validate_click("9")

def test_validate_position(monkeypatch): # Testa se a posição é movida e o texto copiado corretamente, declara algumas funções como mocks
    monkeypatch.setattr(v.pyautogui, "moveTo", lambda _: None)
    monkeypatch.setattr(v.pyautogui, "hotkey", lambda *args: None)
    monkeypatch.setattr(v.time, "sleep", lambda _: None)
    monkeypatch.setattr(v.pyperclip, "paste", lambda: "COPIADO")

    # não é pra executar click real -> mock validate_click
    monkeypatch.setattr(v, "validate_click", lambda _: None)

    out = v.validate_position((100, 200), clicks="1")
    assert out == "COPIADO"

def test_validate_position(monkeypatch):
    monkeypatch.setattr(v.pyautogui, "moveTo", lambda _: None)
    monkeypatch.setattr(v.time, "sleep", lambda _: None)
    monkeypatch.setattr(v, "validate_click", lambda _: None)
    
    # se tentar copiar, deve falhar o teste
    monkeypatch.setattr(v.pyautogui, "hotkey", lambda *args: (_ for _ in ()).throw(AssertionError("não deveria copiar")))
    monkeypatch.setattr(v.pyperclip, "paste", lambda: (_ for _ in ()).throw(AssertionError("não deveria colar")))

    out = v.validate_position("position_lupa", clicks="1")
    assert out is None