import pyautogui
import time

#inserir o numero de registros
num = int(input("Digite o número de registros: "))

def minimizar():
    pyautogui.moveTo(pyautogui.moveTo(x=1806, y=7))
    pyautogui.click()
    time.sleep(0.5)

#minimizar vscode
minimizar()

#copiar - SIGAMA
pyautogui.moveTo(x=128, y=17)
pyautogui.click()
pyautogui.moveTo(x=38, y=335)
pyautogui.tripleClick()
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.5)

# x, y = pyautogui.locateCenterOnScreen('excel_image.png', confidence = 0.8)
# print(x)
# print(y)
pyautogui.click(pyautogui.locateCenterOnScreen('excel_image.png', confidence = 0.8))
time.sleep(0.5)

pyautogui.moveTo(x=207, y=468)
pyautogui.hotkey('ctrl', 'v')

#minimizar excel
minimizar()
pyautogui.moveTo(x=835, y=332)
pyautogui.doubleClick()

pyautogui.hotkey('ctrl', 'c')

pyautogui.click(pyautogui.locateCenterOnScreen('excel_image.png', confidence = 0.8))
time.sleep(0.5)
pyautogui.moveTo(x=548, y=471)
pyautogui.click()
pyautogui.hotkey('ctrl', 'v')

time.sleep(0.5)