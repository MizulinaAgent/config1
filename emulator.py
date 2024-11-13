import argparse
import os
import zipfile
import calendar
import datetime

def prompt(username, current_path):
    home_path = "/root"
    if current_path == home_path:
        path_display = "~"
    else:
        path_display = current_path.lstrip('/')
    return f"{username}_emu:{path_display}$ "

def parse_args():
    parser = argparse.ArgumentParser(description="Эмулятор оболочки")
    parser.add_argument('--user', required=True, help='Имя пользователя для приглашения')
    parser.add_argument('--zip', required=True, help='Путь к zip-файлу с виртуальной файловой системой')
    return parser.parse_args()

def run_shell(username, zip_path):
    current_path = "/root"
    with zipfile.ZipFile(zip_path, "a") as zip_file:
        while True:
            command = input(prompt(username, current_path)).strip().split()
            if not command:
                continue
            cmd = command[0]
            if cmd == 'exit':
                exit_shell()
            elif cmd == 'ls':
                if len(command) == 1:
                    list_directory(current_path, zip_file)
                else:
                    print("ls: аргументы не поддерживаются")
            elif cmd == 'cd':
                if len(command) == 2:
                    current_path = change_directory(current_path, command[1], zip_file)
                elif len(command) == 1:
                    print("cd: отсутствует аргумент")
                else:
                    print("cd: слишком много аргументов")
            elif cmd == 'mkdir':
                if len(command) == 2:
                    current_path = make_directory(current_path, command[1], zip_file)
                    with zipfile.ZipFile('root.zip', 'r') as zip_file:
                        zip_file.printdir()
                else:
                    print("mkdir: отсутствует аргумент")
            elif cmd == 'cal':
                if len(command) == 1:
                    show_calendar()
                else:
                    print("cal: аргументы не поддерживаются")
            elif cmd == 'whoami':
                if len(command) == 1:
                    print(username)
                else:
                    print("whoami: аргументы не поддерживаются")
            else:
                print(f"{cmd}: команда не найдена")



def exit_shell():
    exit(0)

def list_directory(current_path, zip_file):
    current_path = current_path.strip('/')
    current_path_len = len(current_path)
    items_in_current_path = set()

    for file in zip_file.namelist():
        if file.startswith(current_path):
            relative_path = file[current_path_len:].lstrip('/')
            if relative_path and '/' not in relative_path:
                items_in_current_path.add(relative_path)
            elif '/' in relative_path:
                items_in_current_path.add(relative_path.split('/')[0] + '/')

    for item in sorted(items_in_current_path):
        print(item)

def change_directory(current_path, target_directory, zip_file):
    if target_directory == "/":
        return "/root"
    if target_directory.startswith("/"):
        new_dir = "/root"
    else:
        new_dir = current_path
    parts = target_directory.split('/')
    for part in parts:
        if part == '' or part == '.':
            continue
        elif part == "..":
            if new_dir != "/root":
                new_dir = "/".join(new_dir.strip('/').split('/')[:-1])
                if not new_dir:
                    new_dir = "/root"
        else:
            new_dir = os.path.join(new_dir, part).replace("\\", "/").strip('/')

    if any(f.startswith(new_dir + '/') for f in zip_file.namelist()):
        return "/" + new_dir if not new_dir.startswith("/") else new_dir
    else:
        print(f"cd: нет такого файла или каталога: {target_directory}")
        return current_path

def make_directory(current_path, dir_name, zip_file):
    new_dir_path = os.path.join(current_path, dir_name).replace("\\", "/")
    if not new_dir_path.endswith('/'):
        new_dir_path += "/"

    if any(f.startswith(new_dir_path) for f in zip_file.namelist()):
        print(f"mkdir: не удается создать каталог '{dir_name}': файл или каталог существует")
        return current_path

    zip_file.writestr(new_dir_path, b'')
    placeholder_file = new_dir_path + 'placeholder.txt'
    zip_file.writestr(placeholder_file, b'')
    print(f"Каталог '{dir_name}' с пустым файлом внутри создан.")
    return current_path

def show_calendar():
    now = datetime.datetime.now()
    cal = calendar.month(now.year, now.month)
    print(cal)