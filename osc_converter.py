'''
Необходимо сохранить весь ответ запроса осциллограммы в файл txt,
затем открыть его данной программой, она сформирует два файла с
расширениями cfg и dat, которые открываются стандартными просмотрщиками
comtrade-осциллограмм.
'''


from tkinter import *
from tkinter import filedialog
import json
import base64
import os

flag = False
file = None



def help():
    global flag
    if not flag:
    
        help_message='''Сохраните json-ответ SCADA на запрос одиночной осциллограммы
в файл с расширение txt. Затем выберете этот файл при помощи
данной программы и нажмите кнопу "Конвертировать".'''
        
        help_window = Toplevel(osc_convert)
        help_window.protocol("WM_DELETE_WINDOW", lambda help_window=help_window: close_help(help_window))
        help_window.resizable(width=False, height=False)
        hh = Label(help_window, height = 7, width = 70, text=help_message).pack(fill=BOTH)
        flag = True


def close_help(help_window):
    global flag
    flag = False
    help_window.destroy()


def get_file():
    global file_name, file
    file = filedialog.askopenfilename(filetypes = (("Text files", "*.txt"),))
    path = file.split('/')
    file_name = str(path[-1]).split('.')[0]
    if file:
        print('Имя файла', file_name)
    

def convert():
    global file_name, file
    if file:
        try:
            with open(file,'rb') as osc:
                f = osc.read()

            json_string = json.loads(f)

            cfg1 = json_string["paramsValue"][0]["value"][0]["cfg"]
            dat1 =json_string["paramsValue"][0]["value"][0]["dat"]

            bcfg = cfg1.encode("utf-8")
            cfg = base64.b64decode(bcfg)
            bdat = dat1.encode("utf-8")
            dat = base64.b64decode(bdat)
            
            if os.path.basename(os.getcwd()) != 'Oscills':           
                os.chdir('Oscills')
                path = os.getcwd()

            cfg_file = file_name+'.cfg'
            dat_file = file_name+'.dat'
            
            with open(cfg_file, 'wb') as f1:
                f1.write(cfg)
            with open(dat_file, 'wb') as f2:
                f2.write(dat)

            print(f'Сформировано два файла {file_name+".cfg"} и {file_name+".dat"}')
            
        except:
            print('Что-то пошло не так, попробуйте другой файл')
    else:
        print('Выберете файл txt')



osc_convert = Tk()
osc_convert.title("Конвертер осциллограм")
osc_convert.resizable(width=False, height=False)
osc_convert.geometry("350x220")

if not 'Oscills' in list(os.listdir(os.getcwd())):
    os.mkdir('Oscills') 


button1 = Button(text = 'Выберите осц', height = 3, width=35, command = get_file)
button1.pack(expand=True)
button2 = Button(text = 'Конвертировать',  height = 3, width=35, command = convert)
button2.pack(expand=True)
button3 = Button(text = 'HELP',  height = 3, width=35, command = help)
button3.pack(expand=True)

osc_convert.mainloop()
