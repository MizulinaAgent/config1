import argparse


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