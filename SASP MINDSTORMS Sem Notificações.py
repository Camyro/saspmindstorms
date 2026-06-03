import time
import pyautogui
import pygetwindow as gw
from datetime import datetime
from windows_toasts import WindowsToaster, Toast

toaster = WindowsToaster("Auto Save")

print("iniciou")



while True:
    janela_ativa = gw.getActiveWindow()

    if janela_ativa and "EDIÇÃO PARA PROFESSORES LEGO MINDSTORMS EDUCATION EV3" in janela_ativa.title.upper():
        pyautogui.hotkey("ctrl", "s")

        hora = datetime.now().strftime("%H:%M:%S")

        print("foi " + hora)

        print("time de 60s")
        time.sleep(60)
        print("fim do time")