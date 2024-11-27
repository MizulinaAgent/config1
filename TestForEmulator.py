import unittest
import zipfile
import os
from io import StringIO
from contextlib import redirect_stdout
from emulator import list_directory, change_directory, create_directory, show_calendar

class TestShellCommands(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Открывает загруженный ZIP-файл перед тестами.
        """
        cls.zip_path = 'root.zip'
        cls.zip_file = zipfile.ZipFile(cls.zip_path, "a")
        cls.current_path = "/root"

    @classmethod
    def tearDownClass(cls):
        """
        Закрывает ZIP-файл после выполнения тестов.
        """
        cls.zip_file.close()

    # Тесты для mkdir
    def test_mkdir_new_directory(self):
        """
        Тест команды mkdir: создание новой директории.
        """
        create_directory(self.current_path, "new_dir", self.zip_file)
        self.assertIn("root/new_dir/", self.zip_file.namelist())

    def test_mkdir_existing_directory(self):
        """
        Тест команды mkdir: попытка создать уже существующую директорию.
        """
        with StringIO() as buf, redirect_stdout(buf):
            create_directory(self.current_path, "dir1", self.zip_file)
            output = buf.getvalue().strip()
        self.assertIn("mkdir: директория 'dir1' уже существует", output)

    # Тесты для ls
    def test_ls_root_directory(self):
        """
        Тест команды ls для корневой директории.
        """
        with StringIO() as buf, redirect_stdout(buf):
            create_directory(self.current_path, "dir1", self.zip_file)
            output = buf.getvalue().strip()
        self.assertIn("mkdir: директория 'dir1' уже существует", output)

    def test_ls_subdirectory(self):
        """
        Тест команды ls для поддиректории.
        """
        with StringIO() as buf, redirect_stdout(buf):
            create_directory(self.current_path, "dir1", self.zip_file)
            output = buf.getvalue().strip()
        self.assertIn("mkdir: директория 'dir1' уже существует", output)

    # Тесты для cd
    def test_cd_to_existing_directory(self):
        """
        Тест команды cd для перехода в существующую директорию.
        """
        new_path = change_directory(self.current_path, "home", self.zip_file)
        self.assertEqual(new_path, "/root/home")

    def test_cd_to_parent_directory(self):
        """
        Тест команды cd для перехода в родительскую директорию.
        """
        current_path = "/root/dir1"
        new_path = change_directory(current_path, "..", self.zip_file)
        self.assertEqual(new_path, "/root")

    # Тест для whoami
    def test_whoami(self):
        """
        Тест команды whoami.
        """
        username = "test_user"
        with StringIO() as buf, redirect_stdout(buf):
            print(username)
            output = buf.getvalue().strip()
        self.assertEqual(output, username)

    # Тест для cal
    def test_cal(self):
        """
        Тест команды cal.
        """
        with StringIO() as buf, redirect_stdout(buf):
            show_calendar()
            output = buf.getvalue().strip()
        self.assertFalse(output.startswith("   "))

    # Тест для exit
    def test_exit_shell(self):
        """
        Тест команды exit.
        """
        with self.assertRaises(SystemExit):
            from emulator import exit_shell
            exit_shell()


if __name__ == "__main__":
    unittest.main()
