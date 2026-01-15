from automation.utils import filesystem as f

def test_create_directory(tmp_path): # Testa se a pasta é criada corretamente
    base = tmp_path
    pasta = f.create_directory(base, 2026, "Janeiro", 15)

    assert pasta.exists()
    assert pasta.is_dir()
    assert pasta == base / "2026" / "Janeiro" / "15"

def test_copy_excel_file_doesnt_exists(tmp_path): # Testa se o arquivo é copiado quando não existe no destino
    origem = tmp_path / "controle.xlsx"
    origem.write_text("data")

    destino = tmp_path / "dest"
    destino.mkdir()

    copied = f.copy_excel_file(origem, destino)

    assert copied is True
    assert (destino / "controle.xlsx").exists()

def test_copy_excel_file_doesnt_overwrite(tmp_path): # Testa se o arquivo não é copiado quando já existe no destino
    origem = tmp_path / "controle.xlsx"
    origem.write_text("data1")

    destino = tmp_path / "dest"
    destino.mkdir()
    (destino / "controle.xlsx").write_text("data2")

    copied = f.copy_excel_file(origem, destino)

    assert copied is False
    assert (destino / "controle.xlsx").read_text() == "data2"
