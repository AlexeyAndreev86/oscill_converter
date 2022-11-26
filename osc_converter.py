from json import JSONDecodeError
from tkinter import Toplevel, Label, Button, BOTH, Tk, filedialog
import json
import base64
import os


class Converter:
    """
    Необходимо сохранить весь ответ запроса осциллограммы в файл txt,
    затем открыть его данной программой, она сформирует два файла с
    расширениями cfg и dat, которые открываются стандартными просмотрщиками
    COMTRADE-осциллограмм.
    """

    def __init__(self):
        self.help_open = False
        self.file = None
        self.file_name = None

        self.osc_convert = Tk()
        self.osc_convert.title("Конвертер осциллограм")
        self.osc_convert.resizable(width=False, height=False)
        self.osc_convert.geometry("350x220")

        self.button1 = Button(text='Выберите осц', height=3, width=35, command=self.get_file)
        self.button1.pack(expand=True)
        self.button2 = Button(text='Конвертировать', height=3, width=35, command=self.convert)
        self.button2.pack(expand=True)
        self.button3 = Button(text='HELP', height=3, width=35, command=self.help)
        self.button3.pack(expand=True)

        if 'Oscills' not in list(os.listdir(os.getcwd())):
            os.mkdir('Oscills')

        self.osc_convert.mainloop()

    def help(self):
        if not self.help_open:
            help_message = '''Сохраните json-ответ SCADA на запрос одиночной осциллограммы
    в файл с расширение txt. Затем выберете этот файл при помощи
    данной программы и нажмите кнопу "Конвертировать".'''

            help_window = Toplevel(self.osc_convert)
            help_window.protocol("WM_DELETE_WINDOW", lambda help_window=help_window: self.close_help(help_window))
            help_window.resizable(width=False, height=False)
            Label(help_window, height=7, width=70, text=help_message).pack(fill=BOTH)
            self.help_open = True

    def close_help(self, help_window):
        self.help_open = False
        help_window.destroy()

    def get_file(self):
        self.file = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),))
        path = os.path.basename(self.file)
        self.file_name = os.path.splitext(path)[0]
        if self.file:
            print('Имя файла', self.file_name)

    def convert(self):
        if self.file:
            try:
                with open(self.file, 'rb') as osc:
                    data = osc.read()

                json_string = json.loads(data)

                cfg1 = json_string["paramsValue"][0]["value"][0]["cfg"]
                dat1 = json_string["paramsValue"][0]["value"][0]["dat"]

                bcfg = cfg1.encode("utf-8")
                cfg = base64.b64decode(bcfg)
                bdat = dat1.encode("utf-8")
                dat = base64.b64decode(bdat)

                if os.path.basename(os.getcwd()) != 'Oscills':
                    os.chdir('Oscills')

                cfg_file = self.file_name + '.cfg'
                dat_file = self.file_name + '.dat'

                with open(cfg_file, 'wb') as f1:
                    f1.write(cfg)
                with open(dat_file, 'wb') as f2:
                    f2.write(dat)

                print(f'Сформировано два файла {cfg_file} и {dat_file}')

            except JSONDecodeError:
                print('Что-то пошло не так, попробуйте другой файл')


if __name__ == "__main__":
    Converter()
