import os
from re import findall

from moviepy.editor import*
from moviepy.config import change_settings

from tkinter import Tk,filedialog
from art import tprint

import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True,convert=True)

tk=Tk()
tk.withdraw()

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe"})


def GifMaker(show:bool=False):

    ''' Функция Создания GIF-Амимации на основе moviepy
    Внимание!требует установки <ImageMagick> в системе'''

    os.system("cls")
    #==============Получение имя Пользователя в Windows
    user =os.path.expanduser('~').split('\\')[-1]
    #=============Выбор видеофайла
    clip =filedialog.askopenfilename(title= "Выберите ВидеоФайл")
    if len(clip) ==0:print(f"\n\t[INFO]Отменено Пользователем {Fore.GREEN}{user}");raise SystemExit

    #=============Получение имя видеофайла(укороченное)
    clipName =clip.split('/')[-1].split('.')[0]

    #=============Проверка файла на расширение
    fmt=('avi','mkv','mp4','webm','mov','flv','wmv')
    if clip.split(".")[-1].lower() not in fmt:
        input(f"\n\t{Fore.RED}[Error!]{clipName} {Fore.WHITE} Неявляется Видео файлом!");GifMaker()

    #=============Запуск проигрования видеофайла
    os.startfile(clip)
    #========================================

    def timeShift():
        #============Начальное время обрезки в секундах
        startTime =input(f"\n\t{Fore.GREEN}[Start]{Fore.WHITE}Начальное время[int](в секундах): ")
        while len(findall(r"[0-9]+", startTime)) ==0:startTime =input(f"\n\t[Start]Начальное время[int](в секундах): ")
        #============Конечное время обрезки в секундах
        endTime =input(f"\t{Fore.GREEN}[End]{Fore.WHITE}Конечное время[int](в секундах): ")
        while len(findall(r"[0-9]+", endTime)) ==0:startTime =input(f"\t[End]Конечное время[int](в секундах): ")
        return startTime,endTime

    def Colors():
      os.system("cls")
      tprint("Gif Anim",font="rnd-medium")

      color_line =[ 'White', 'Green', 'Red', 'Black','Blue', 'Orange','Brown','Maroon',
     'Pink','Silver','Purple','Gold','Yellow','Violet','MistyRose','Lime']
      for color in color_line:print("\t",color)
      return color_line

    start,end =timeShift()
    if int(start) >= int(end):
        input("\n\t[!]Конечное Время Недолжно быть меньше или равно Начального(му)");start,end =timShift()

    #===========Длительность Анимации на Основе Нач-го и Коне-го времени
    clip_interv =(int(end)-int(start) )-1

    textClip =input(f"\n\t{Fore.GREEN}[Text]{Fore.WHITE}Введите текст для GIF: ")
    if len(textClip) ==0:textClip =""

    fontClip =input(f"\t{Fore.GREEN}[Font]{Fore.WHITE}Размер шрифта(от 0 - 40): ")
    if len(fontClip) ==0:fontClip ='15'

    color =Colors()
    fontColor =input(f"\t{Fore.GREEN}[Color]{Fore.WHITE}Выберите Цвет шрифта: ")
    #=========Если ничего не ввели или неверный цвет, то fontColor ='MistyRose'
    if len(fontColor) ==0 or fontColor not in color:fontColor ='MistyRose'

    sizeClip =input(f"\t{Fore.GREEN}[HW]{Fore.WHITE}Задать Высоту и Ширину (от 0.1 - 1.0):  ")
    #=========Если ничего не ввели или неверный ввод, то sizeClip =0.3
    if len(findall(r"\d{1}\.\d{1}",sizeClip)) ==0:sizeClip =0.3

    #=============================Создание GIF Анимации

    try:
        video =VideoFileClip(clip).subclip(int(start), int(end))
        video_res =video.resize(float(sizeClip))
        txt =(TextClip(textClip,fontsize=int(fontClip),color=fontColor)
                     .set_position('center')
                     .set_duration(clip_interv))
        res = CompositeVideoClip([video_res, txt])

        #=============Проверка что Файл с таким имением сушетвует
        file_exist =True
        ecx =1
        while file_exist:
            if os.path.exists(f"clipName{ecx}.gif"):ecx+=1
            else:file_exist =False
        #================================================    
        os.system('cls')
        tprint("Gif Anim",font="rnd-medium")
        Gif_name =f"clipName{ecx}.gif"
        res.write_gif(Gif_name,fps =30)

        if show:os.startfile(Gif_name)

    except OSError:
        os.system("cls")
        input(f"\n\t{Fore.RED}[FatalError]{Fore.WHITE}Убедитесь в установки <ImageMagick> и Правильности пути к нему! ")
        raise SystemExit
    except Exception as e:print(f"\tОшибка{e}");return False


GifMaker(1)
