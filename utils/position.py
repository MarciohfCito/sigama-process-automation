import pyautogui

def get_name_positions():
    PNx, PNy = pyautogui.locateCenterOnScreen('./image/nome_image.png', confidence= 0.6)
    final_position = [PNx, PNy + 40] # hardcoded due to software layout// hardcoded por causa do layout do software
    
    return final_position

def get_cpf_positions():
    PCx, PCy = pyautogui.locateCenterOnScreen('./image/cpf_image.png', confidence= 0.6)
    final_position = [PCx, PCy + 40] # hardcoded due to software layout// hardcoded por causa do layout do software
    
    return final_position

def get_lupa_position():
    PLx, PLy = pyautogui.locateCenterOnScreen('./image/operacoes_image.png', confidence= 0.5)
    final_position = [PLx + 52, PLy + 34] # hardcoded due to software layout// hardcoded por causa do layout do software

    return final_position