import time
import pyautogui
import pygetwindow as gw
from datetime import datetime
from windows_toasts import WindowsToaster, Toast, ToastAudio
import pyautogui

pyautogui.FAILSAFE = False

toaster = WindowsToaster("Auto Save")

print("iniciou")

while True:
    janela_ativa = gw.getActiveWindow()

    if (
        janela_ativa
        and "EDIÇÃO PARA PROFESSORES LEGO MINDSTORMS EDUCATION EV3"
        in janela_ativa.title.upper()
    ):
        pyautogui.hotkey("ctrl", "s")

        hora = datetime.now().strftime("%H:%M:%S")

        print("foi " + hora)

        toast = Toast()
        toast.text_fields = [f"Projeto salvo às {hora}"]

        # Notificação sem som
        toast.audio = ToastAudio(silent=True)

        toaster.show_toast(toast)

        print("time de 60s")
        time.sleep(60)
        print("fim do time")

    time.sleep(5)