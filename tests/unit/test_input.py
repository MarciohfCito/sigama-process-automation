from automation.utils.input import input_numres

def test_input_numres_returns_user_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "42")

    out = input_numres()

    assert out == "42"