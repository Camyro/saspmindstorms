import time
import pyautogui
import pygetwindow as gw
from datetime import datetime
from windows_toasts import WindowsToaster, Toast, ToastAudio
from pathlib import Path
import json

toaster = WindowsToaster("Auto Save")

CONFIG_PADRAO = {
    "notificação": {
        "ativo": True,
        "text": "Projeto salvo."
    },
    "time": 60,
    "segundo_plano": True
}
DRIVE = Path.cwd().anchor
CAMINHO = Path(DRIVE) / "C1Studios" / "saspmindstorms" / "config"
ARQUIVO = CAMINHO / "config.json"
global _NOTIFICACOES_ATIVO
global _NOTIFICACOES_TEXT
global _TIME
global _SEGUNDO_PLANO
global _CONFIG
with open(ARQUIVO, "r", encoding="utf-8") as f:
    _CONFIG = json.load(f)
_NOTIFICACOES_ATIVO = _CONFIG["notificação"]["ativo"]
_NOTIFICACOES_TEXT = _CONFIG["notificação"]["text"]
_TIME = _CONFIG["time"]
_SEGUNDO_PLANO = _CONFIG["segundo_plano"]

def atualizar_config(config, padrao):
    for chave, valor in padrao.items():
        if chave not in config:
            config[chave] = valor
        elif isinstance(valor, dict) and isinstance(config[chave], dict):
            atualizar_config(config[chave], valor)

def carregar_config():
    # Cria todas as pastas necessárias
    CAMINHO.mkdir(parents=True, exist_ok=True)

    # Se o arquivo não existir, cria
    if not ARQUIVO.exists():
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(CONFIG_PADRAO, f, indent=4, ensure_ascii=False)
        return CONFIG_PADRAO.copy()

    # Lê o arquivo
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception:
        config = {}

    # Adiciona configurações novas sem apagar as antigas
    atualizar_config(config, CONFIG_PADRAO)

    # Salva caso tenha sido atualizado
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    return config

config = carregar_config()
print(config)

while True:
    janela_ativa = gw.getActiveWindow()

    if (
        janela_ativa
        and "EDIÇÃO PARA PROFESSORES LEGO MINDSTORMS EDUCATION EV3"
        in janela_ativa.title.upper()
    ):
        pyautogui.hotkey("ctrl", "s")

        hora = datetime.now().strftime("%H:%M:%S")

        if _NOTIFICACOES_ATIVO:
            toast = Toast()
            toast.text_fields = [f"{_NOTIFICACOES_TEXT} Hora: {hora}"]
            # Notificação sem som
            toast.audio = ToastAudio(silent=True)
            toaster.show_toast(toast)

        time.sleep(_TIME)

    time.sleep(5)
