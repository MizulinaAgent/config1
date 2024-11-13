import argparse
import zipfile


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
    with zipfile.ZipFile(zip_path, "a") as zip_file:  # Открытие в режиме добавления для mkdir
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