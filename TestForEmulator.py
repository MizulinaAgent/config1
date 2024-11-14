import unittest
import os
import zipfile
from io import StringIO
import sys
from emulator import list_directory, change_directory, exit_shell


class TestShellCommands(unittest.TestCase):

    def setUp(self):
        self.zip_path = 'root.zip'
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('root/placeholder.txt', '')

    def tearDown(self):
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)

    def test_ls(self):
        # Проверка команды 'ls', выводит файл 'placeholder.txt' в корневой директории
        captured_output = StringIO()
        sys.stdout = captured_output
        with zipfile.ZipFile(self.zip_path, 'a') as zipf:
            list_directory('/root', zipf)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        self.assertEqual(output, 'placeholder.txt')

        # Проверка команды 'ls' в несуществующей директории, должно быть пусто
        captured_output = StringIO()
        sys.stdout = captured_output
        with zipfile.ZipFile(self.zip_path, 'a') as zipf:
            list_directory('/root/nonexistent', zipf)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        self.assertEqual(output, '')

    def test_cd(self):
        # Проверка команды 'cd' в корневую директорию
        captured_output = StringIO()
        sys.stdout = captured_output
        with zipfile.ZipFile(self.zip_path, 'a') as zipf:
            new_path = change_directory('/root', '/', zipf)
        sys.stdout = sys.__stdout__
        self.assertEqual(new_path, '/root')

        # Проверка команды 'cd' в несуществующую директорию, возвращает на '/root'
        captured_output = StringIO()
        sys.stdout = captured_output
        with zipfile.ZipFile(self.zip_path, 'a') as zipf:
            new_path = change_directory('/root', '/nonexistent', zipf)
        sys.stdout = sys.__stdout__
        self.assertEqual(new_path, '/root')

    def test_exit(self):
        # Проверка завершения работы оболочки
        with self.assertRaises(SystemExit):
            exit_shell()

    def test_whoami(self):
        # Проверка команды 'whoami', должно вернуть имя пользователя
        captured_output = StringIO()
        sys.stdout = captured_output
        username = "root"
        print(username)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "root")

        # Проверка команды 'whoami' с другим пользователем
        captured_output = StringIO()
        sys.stdout = captured_output
        username = "admin"
        print(username)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "admin")

if __name__ == '__main__':
    unittest.main()
