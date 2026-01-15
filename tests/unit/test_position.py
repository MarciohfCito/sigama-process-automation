import time
from pathlib import Path
from automation.utils import position as p

def test_get_name_positions(monkeypatch): # Testa se a função retorna a posição correta 
    monkeypatch.setattr(p.pyautogui, "locateCenterOnScreen", lambda *args, **kwargs: (100, 200))
    assert p.get_name_positions() == [100, 240]

def test_get_cpf_positions(monkeypatch):
    monkeypatch.setattr(p.pyautogui, "locateCenterOnScreen", lambda *args, **kwargs: (10, 20))
    assert p.get_cpf_positions() == [10, 60]

def test_get_lupa_position(monkeypatch):
    monkeypatch.setattr(p.pyautogui, "locateCenterOnScreen", lambda *args, **kwargs: (50, 60))
    assert p.get_lupa_position() == [102, 94]  # 50+52, 60+34

def test_get_docs_position(monkeypatch): 
    calls = {"move": 0}

    def fake_locate(*args, **kwargs): # Mock de locateCenterOnScreen
        return (300, 400)

    def fake_move(*args, **kwargs): # Mock de moveTo
        calls["move"] += 1

    monkeypatch.setattr(p.pyautogui, "locateCenterOnScreen", fake_locate)
    monkeypatch.setattr(p.pyautogui, "moveTo", fake_move)

    x1, y1 = p.get_docs_position()

    assert (x1, y1) == (275, 400)
    assert calls["move"] == 1

def test_get_documents_complete(monkeypatch, tmp_path):
    # evitar sleeps e ações reais
    monkeypatch.setattr(p.time, "sleep", lambda _: None)

    move_calls = {"n": 0}
    click_calls = {"n": 0}
    passed_dest = {"value": None}

    monkeypatch.setattr(p.pyautogui, "moveTo", lambda *args, **kwargs: move_calls.__setitem__("n", move_calls["n"] + 1))
    monkeypatch.setattr(p.pyautogui, "click", lambda *args, **kwargs: click_calls.__setitem__("n", click_calls["n"] + 1))

    # fechar X: para não procurar imagem real
    monkeypatch.setattr(p.pyautogui, "locateCenterOnScreen", lambda *args, **kwargs: (1, 1))

    # mock das validações importadas no módulo
    monkeypatch.setattr(p, "validate_downloads_folder", lambda files_directory: None)

    def fake_validate_download(files_directory, agora, destino):
        passed_dest["value"] = destino

    monkeypatch.setattr(p, "validate_download", fake_validate_download)

    files_directory = tmp_path / "downloads"
    files_directory.mkdir()

    DOCUMENTOS_DIR = tmp_path / "docs"

    p.get_documents(
        x1=100,
        y1=200,
        files_directory=files_directory,
        DOCUMENTOS_DIR=DOCUMENTOS_DIR,
        ano="2026",
        mes="Janeiro",
        dia="15",
        nome_cpf_tratado="Fulano - 000"
    )

    # loop de 5 cliques + 1 clique final do X = 6
    assert click_calls["n"] == 6

    # destino correto
    assert passed_dest["value"] == Path(DOCUMENTOS_DIR, "2026", "Janeiro", "15", "Fulano - 000")
