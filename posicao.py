import pyautogui
import time

time.sleep(5)

print(pyautogui.position())
print(pyautogui.size())
# time.sleep(2)
# pyautogui.moveTo(pyautogui.locateOnScreen('./image/carregando_image.png', confidence= 0.4))

#-------- TELA CHEIA ---------
#SIGAMA
#nome1 = 26x 314y
#nome2 = 26x 355y
#largura = 45y
#meio nome = 77x
#meio cpf = 839x
#primeiro nome = x=77, y=336

#EXCEL
#nome 1 = 37x 297y
#nome 2 = 37x 323y
#largura = 26y
#meio nome = 252x
#meio cpf = 590x
#primeiro nome = x=252, y=309




# ---- TELA DIVIDIDA -------
#largura excel - 24y - 12y
#meio do nome - 1217x 299y
#meio cpf - 1550x
#nome1 = x1217 y311
#cpf1 = 1550x 311y


#largura sigama - 78y - 39y
#nome - 72x
#nome = 72x 325y
#meio cpf - 118x
#nome1 = 72x 364y
#cpf1 = 118x 364y

#DOCUMENTO 1
#anexo
# x, y = pyautogui.locateCenterOnScreen('anexo_image.png', confidence=0.8)
# print('x =', x, 'y =', y)
#x=955, y=588
#x=925, y=604
#diferença = 16y
#x=925, y=626
#diferença2 = 22y
#diferença do anexo para meio do doc1 = 11y + 16y = 27y