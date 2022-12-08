import os
import subprocess
from pathlib import Path
from art import tprint
from re import findall

import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

from tkinter import filedialog,Tk

tk=Tk()
tk.withdraw()

def show_info_audio_video():
    ''' Функция для получения инфо о видео или аудиофайле
    Принимает один параметр-Имя(путь к) видео или аудиофайла(у)
    Внимание!Требует установки ffmpeg в системе
    Также не забывайте установить
    pip install art
    pip install colorama
    pip install subprocess32'''
    
    user =os.path.expanduser('~').split('\\')[-1]
    try:
        file =filedialog.askopenfilename(title= "Выберите Файл")
        if len(file) ==0:input(f"{Fore.RED}[Dismiss]{Fore.WHITE}Отменено Пользователем {user} ");raise SystemExit
        #==================Проверяем,что файл явля-ся аудио или видео файлом
        fmt_video =('avi','mkv','mp4','webm','mov','flv')
        fmt_audio =('mp3','wma','wav','flac','aac','ogg')
        ext =file.split(".")[-1].lower()

        if ext not in fmt_video and ext not in fmt_audio:
            print(f"\n\t{Fore.RED}[Error!]{file} {Fore.WHITE} Неявляется ни Аудио ни Видео файлом!");raise SystemExit

        #==============Парсим все данные в перем-ю <res> и переводим в строку
        cmd =f'ffmpeg -i {file} -hide_banner'
        p =subprocess.Popen(cmd,stdout =subprocess.PIPE,stderr=subprocess.STDOUT, shell =True)
        res =p.stdout.read().decode().split()
        stdout, stderr =p.communicate()
        res =''.join(res).replace(',', ' ')

        #===========Данные из видео или аудио файла С помощью регулярных выражений
        bitrate =''.join(findall(r"bitrate:\d{3,5}kb/s",res))
        Duration =''.join(findall(r"Duration:\d{2}\:\d{2}\:\d{2}\.\d{2}",res))
        fps =''.join(findall(r"\d{2}.\d{1,2}fps",str(res)) or findall(r"\d{2}fps",res))
        resolution =''.join(findall(r"\d{3,4}x\d{3,4}",res))
        ratio =''.join(findall(r"1DAR\d{1,2}:\d{1,2}",res)).replace('1DAR', '')
        #===========укороченое название файла
        push_file =file.split("/")[-1]
        #===========Получение размера файла
        size =round(Path(file).stat().st_size / 1024 /1024,2)
        #============Стильный вывод на Экран
        os.system("cls")
        #=push_file[:12]-выводим название файла,но небольше 12 cимволов
        tprint(f"{push_file[:12]}",font="rnd-medium")
        print("" + "="*20 + "ИНФО" + "="*20)

        if 'Nosuchfileordirectory' in res:print(f"\n\t{Fore.RED}[Error]{Fore.CYAN}Данные Недоступны!Из-за страного названия файла  \
            \n\tили Наличии Кирилицы в названии!!");raise SystemExit

        #======================run
        if ext in fmt_video:
            if len(ratio) ==0:ratio =None
            print(f'\n\t{Fore.CYAN}\n\t█{bitrate} *\n\t█{Duration} *\n\t█FPS:{fps} *\n\t█RES:{resolution} *\n\t█Ratio:{ratio} *\n\t█Размер:{size} Мб')

        else:
            if len(bitrate) ==0:bitrate =None
            if len(Duration) ==0:Duration=None
            print(f'\n\t{Fore.CYAN}\n\t█{bitrate} *\n\t█{Duration} *\n\t█Размер:{size} Мб')
            if bitrate !=None:bitrate=bitrate.replace('bitrate:','').replace('kb/s','')

        input("\n\tPress <ENTER>-продолжить")  

        return resolution,ratio,bitrate

    except Exception as e:print(f"Ошибка:{e}") 

show_info_audio_video()  

    

