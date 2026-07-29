# ###############
# ### IMPORTS ###
# ###############
import time
import os
import pyautogui
import pygetwindow as gw
from datetime import datetime
from windows_toasts import WindowsToaster, Toast, ToastAudio
import pyautogui
import json
from pathlib import Path
import psutil
import subprocess
import sys
import shutil

# ##############
# ### CONFIG ###
# ##############
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
pyautogui.FAILSAFE = False
toaster = WindowsToaster("Auto Save")

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

with open(ARQUIVO, "r", encoding="utf-8") as f:
    config = json.load(f)


# #################
# ### VARIÁVEIS ###
# #################
global _NOTIFICACOES_ATIVO
global _NOTIFICACOES_TEXT
global _TIME
global _SEGUNDO_PLANO
global _CONFIG
STARTUP = (
    Path(os.getenv("APPDATA"))
    / "Microsoft"
    / "Windows"
    / "Start Menu"
    / "Programs"
    / "Startup"
)

def variveis_config():
    global _CONFIG
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        _CONFIG = json.load(f)
    
    global _NOTIFICACOES_ATIVO
    global _NOTIFICACOES_TEXT
    global _TIME
    global _SEGUNDO_PLANO
    _NOTIFICACOES_ATIVO = _CONFIG["notificação"]["ativo"]
    _NOTIFICACOES_TEXT = _CONFIG["notificação"]["text"]
    _TIME = _CONFIG["time"]
    _SEGUNDO_PLANO = _CONFIG["segundo_plano"]
variveis_config()


# ###############
# ### FUNÇÕES ###
# ###############
# ---------------
# SOMENTE NÚMEROS
def inputComNumeros(text):
    text_base = text
    while True:
        text = input(text_base)
        if not text.isdigit():
            print("Erro: Números não são permitidos. Tente novamente.\n")
            time.sleep(3)
            os.system("cls")
        else:
            text = int(text)
            break
    return text

# -----------------------
# APRESENTAÇÃO DO SISTEMA
def apresentacao():
    os.system("cls")
    print("")
    print("     ███████╗ █████╗ ███████╗██████╗ ███╗   ███╗")
    print("     ██╔════╝██╔══██╗██╔════╝██╔══██╗████╗ ████║")
    print("     ███████╗███████║███████╗██████╔╝██╔████╔██║")
    print("     ╚════██║██╔══██║╚════██║██╔═══╝ ██║╚██╔╝██║")
    print("     ███████║██║  ██║███████║██║     ██║ ╚═╝ ██║")
    print("     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝     ╚═╝")
    print("Salvamento Automático em Segundo Plano do Mindstorms")
    print("C1Studios")


# -----------------------
def configuracoes():
    global _CONFIG
    
    while True:
        apresentacao()
        print("\n- Configurações -")

        opcoes = inputComNumeros("Opções de configurações:\n1. Tempo\n2. Notificações\n3. Iniciar\n4. Voltar\n\nEscolha um dos números: ")

        if opcoes < 1 or opcoes > 4:
            print("Informe somente números entre 1 e 4")
            time.sleep(3)
        else:
            if opcoes == 1:
                while True:
                    apresentacao()
                    print("\n- Configurações / Tempo -")
                    while True:
                        opcoes = inputComNumeros("Opções de configurações do tempo:\n1. Tempo entre os salvamentos\n2. Voltar\n\nEscolha um dos números: ")
                        if opcoes < 1 or opcoes > 2:
                            print("Informe somente números entre 1 e 2")
                            time.sleep(3)
                            break
                        else:
                            break
                    if opcoes == 1:
                        tempo = inputComNumeros("\nDigite um número em segundos: ")
                        _CONFIG["time"] = tempo
                        with open(ARQUIVO, "w", encoding="utf-8") as f:
                            json.dump(_CONFIG, f, indent=4, ensure_ascii=False)
                        variveis_config()
                        reinicarProcessos("salvamento-automatico-em-segundo-plano-do-mindstorms.exe")
                        break
                    elif opcoes == 2:
                        break

            elif opcoes == 2:
                while True:
                    apresentacao()
                    print("\n- Configurações / Notificações -")
                    while True:
                        opcoes = inputComNumeros("Opções de configurações das notificações:\n1. Texto da Notificação\n2. Ativar ou desativar\n3. Voltar\n\nEscolha um dos números: ")
                        if opcoes < 1 or opcoes > 3:
                            print("Informe somente números entre 1 e 2")
                            time.sleep(3)
                            break
                        else:
                            break
                    if opcoes == 1:
                        text = input(f"\nAnteriormente: {_NOTIFICACOES_TEXT}\nDigite um número em segundos: ")
                        _CONFIG["notificação"]["text"] = text
                        with open(ARQUIVO, "w", encoding="utf-8") as f:
                            json.dump(_CONFIG, f, indent=4, ensure_ascii=False)
                        variveis_config()
                        reinicarProcessos("salvamento-automatico-em-segundo-plano-do-mindstorms.exe")
                        break
                    elif opcoes == 2:
                        while True:
                            opcoes = inputComNumeros(F"Opções das notificações (atualmente: {_NOTIFICACOES_ATIVO}):\n1. Ativar\n2. Desativar\n3. Voltar\n\nEscolha um dos números: ")
                            if opcoes < 1 or opcoes > 3:
                                print("Informe somente números entre 1 e 2")
                                time.sleep(3)
                                break
                            else:
                                break
                        if opcoes == 1:
                            _CONFIG["notificação"]["ativo"] = True
                            with open(ARQUIVO, "w", encoding="utf-8") as f:
                                json.dump(_CONFIG, f, indent=4, ensure_ascii=False)
                            variveis_config()
                            reinicarProcessos("salvamento-automatico-em-segundo-plano-do-mindstorms.exe")
                            break
                        elif opcoes == 2:
                            _CONFIG["notificação"]["ativo"] = False
                            with open(ARQUIVO, "w", encoding="utf-8") as f:
                                json.dump(_CONFIG, f, indent=4, ensure_ascii=False)
                            variveis_config()
                            reinicarProcessos("salvamento-automatico-em-segundo-plano-do-mindstorms.exe")
                            break
                        elif opcoes == 3:
                            break
                    elif opcoes == 3:
                        break
            elif opcoes == 3:
                while True:
                    apresentacao()
                    print("\n- Configurações / Iniciar -")
                    while True:
                        opcoes = inputComNumeros(f"Configurar o incio automático (atualmente: {_SEGUNDO_PLANO}):\n1. Ativar\n2. Desativar\n3. Voltar\n\nEscolha um dos números: ")
                        if opcoes < 1 or opcoes > 3:
                            print("Informe somente números entre 1 e 2")
                            time.sleep(3)
                            break
                        else:
                            if opcoes == 1:
                                _CONFIG["segundo_plano"] = True
                                with open(ARQUIVO, "w", encoding="utf-8") as f:
                                    json.dump(_CONFIG, f, indent=4, ensure_ascii=False)
                                variveis_config()
                                reinicarProcessos("salvamento-automatico-em-segundo-plano-do-mindstorms.exe")
                                break
                            elif opcoes == 2:
                                _CONFIG["segundo_plano"] = False
                                with open(ARQUIVO, "w", encoding="utf-8") as f:
                                    json.dump(_CONFIG, f, indent=4, ensure_ascii=False)
                                variveis_config()
                                reinicarProcessos("salvamento-automatico-em-segundo-plano-do-mindstorms.exe")
                                break
                            elif opcoes == 3:
                                break
                    break

            elif opcoes == 4:
                break




# -----------------------
def sobre():
    apresentacao()
    print("\nInformações:\nVersão: 26.2\nAno: 2026\nDesenvolvedor: C1Studios\nGitHub: https://github.com/Camyro/saspmindstorms")
    opcoes = input("\n[ Precione enter para voltar ]")


# ----------------------------
# SALVAR CÓDIGOS DO MINDSTORMS
def salvar():
    global _NOTIFICACOES_ATIVO
    global _NOTIFICACOES_TEXT
    global _TIME

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

def processosAbertos(process_name):
    for proc in psutil.process_iter(['name']):
        try:
            nome = proc.info['name']
            if nome and nome.lower() == process_name.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

def fecharProcessos(process_name):
    if processosAbertos(process_name):
        for proc in psutil.process_iter(['name']):
            try:
                nome = proc.info['name']
                if nome and nome.lower() == process_name.lower():
                    proc.kill()
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False
    return True

def reinicarProcessos(process_name):
    print("Verificando se tem processos em segundo plano...")

    if processosAbertos(process_name):
        print("O processo está aberto, estamos fechando ele...")
        while fecharProcessos(process_name):
            print("Processo fechado")
            print("Verificando novamente")
    else:
        print("O processo não está aberto")

    print("Verificando a pasta Startup...")

    destino = STARTUP / process_name

    if getattr(sys, "frozen", False):
        origem = Path(sys._MEIPASS) / process_name

        try:
            if _SEGUNDO_PLANO:
                # Remove a versão antiga
                if destino.exists():
                    destino.unlink()
                    print("Arquivo antigo removido.")

                # Copia a nova
                shutil.copy2(origem, destino)
                print("Arquivo copiado para Startup.")

                # Inicia o processo
                subprocess.Popen([str(destino)])
                print("Processo iniciado.")

            else:
                # Remove da Startup
                if destino.exists():
                    destino.unlink()
                    print("Arquivo removido da Startup.")
                else:
                    print("O arquivo já não estava na Startup.")

        except PermissionError:
            print("O executável está em uso e não pôde ser alterado.")
        except Exception as erro:
            print(f"Erro: {erro}")

    time.sleep(5)




# ##############
# ### CÓDIGO ###
# ##############
# APRESENTAÇÃO
apresentacao()
print("")
reinicarProcessos("salvamento-automatico-em-segundo-plano-do-mindstorms.exe")

while True:
    # APRESENTAÇÃO
    apresentacao()

    opcoes = inputComNumeros("\nOpções do sistema:\n1. Parar o SASPM\n2. Configurações\n3. Sobre\n4. Sair\n\nEscolha um dos números: ")
    if opcoes < 1 or opcoes > 4:
        print("Informe somente números entre 1 e 3")
        time.sleep(3)
    else:
        if opcoes == 1:
            print("Verificando se tem processos em segundo plano...")
            if processosAbertos("salvamento-automatico-em-segundo-plano-do-mindstorms.exe"):
                print("O processo está aberto, estamos fechando ele...")
                while fecharProcessos("salvamento-automatico-em-segundo-plano-do-mindstorms.exe"):
                    print("Processo fechado")
                    print("Verificando novamente")
            else:
                print("O processo não ta aberto")

            print("Tudo certo")
            sair = input("\n[ Precione enter para sair ]")
            break
        if opcoes == 2:
            configuracoes()
        if opcoes == 3:
            sobre()
        if opcoes == 4:
            break

exit
