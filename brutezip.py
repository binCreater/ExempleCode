from zipfile import is_zipfile,ZipFile
import os

import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)



def Bruteforce_zip(archive,wordlist):
    path_file=os.getcwd()
     
    line ='-'*25
    try:
        #проверка является ли агрив Zip-врхивом!
        if is_zipfile(archive) ==False:print(f"\n\t[!]{Fore.RED}{archive} Неявляется {Fore.GREEN} ZIP-архивом!");return False
        #Проверка что файл с паролями не пуст!
        if len(list(open(wordlist,'rb'))) ==0:print(f"\n\t[!]Файл{Fore.RED}{wordlist}{Fore.YELLOW} Пуст!");return False

        def generator(passwords):
            for word in passwords:
                passwd =word.strip()
                archive_zip.setpassword(passwd.encode())
                
                try:
                    archive_zip.extractall(path_file)
                except:
                    os.system("cls")
                    yield f"\n{Fore.RED}[False]:{Fore.YELLOW}{passwd}"
                else:
                    yield f"\t{line}\n\t{Fore.GREEN}[Найден]:{Fore.YELLOW}{passwd}";return True

        with open(wordlist,'r',errors = 'ignore') as passwords:
            with ZipFile(archive) as archive_zip:
                for password in generator(passwords):
                    print(password)


    except Exception as e:print(f"{Fore.CYAN}{e}")
    
    
 #-----------Точка входа----run
 
 archive ="Название zip-архива"
 wordlist ="Файл с паролями.txt"
 
 Bruteforce_zip(archive,wordlist)
 
 
