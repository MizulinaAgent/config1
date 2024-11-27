# Задание №1 Индивидуальный вариант №19
## Постановка задачи

Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. 
Эмулятор должен запускаться из реальной командной строки, а файл с виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата **zip**. 
Эмулятор должен работать в режиме **CLI**.

Ключами командной строки задаются:

• Имя компьютера для показа в приглашении к вводу.

• Путь к архиву виртуальной файловой системы.

Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:
1. cal.
2. whoami.
3. mkdir.

## Описание команд для реализации
• ls — отображает список файлов и директорий в текущей директории.

• cd — изменяет текущую рабочую директорию на указанную.

• exit — завершает выполнение текущей оболочки или программы.

• cal — выводит календарь для текущего месяца или заданного месяца и года.

• whoami — отображает имя текущего пользователя.

• mkdir — создает новую директорию с указанным именем.

## Описание функций, используемых для моделирования работы строки

• prompt(username, current_path) — генерирует приглашение командной строки для указанного пользователя и текущего пути. Если текущий путь — это /root, выводится ~, иначе выводится путь без ведущих слэшей.

• parse_args() — парс(парсит,парсирует хз как) аргументы командной строки с помощью argparse. Ожидаются два обязательных аргумента: имя пользователя (--user) и путь к zip-файлу (--zip).

• run_shell(username, zip_path) — запускает эмулятор оболочки, в котором обрабатываются команды пользователя. Команды выполняются циклично: если команда не распознана или передано слишком много/мало аргументов, выводится ошибка. Поддерживаются команды exit, ls, cd, mkdir, cal, whoami.

• exit_shell() — завершает выполнение программы, закрывая оболочку.

• list_directory(current_path, zip_file) — выводит список файлов и каталогов в текущем пути в zip-архиве. Проходит по файлам в архиве и фильтрует их по указанному пути, выводя только имена файлов и директорий на первом уровне вложенности.

• change_directory(current_path, target_directory, zip_file) — изменяет текущую директорию. Если путь относительный, то он интерпретируется относительно текущей директории. Если путь абсолютный, переход происходит в корневую директорию /root. Если путь не существует в архиве, выводится ошибка.

• make_directory(current_path, dir_name, zip_file) — создает новый каталог в указанном месте внутри zip-архива. Для этого записывается пустой файл в архив с именем нового каталога. Внутри создается также файл placeholder.txt для подтверждения создания каталога.

• show_calendar() — выводит календарь текущего месяца с использованием модуля calendar. Для этого определяется текущий год и месяц, после чего выводится соответствующий календарь.

• main() — основной вход в программу. Парсит аргументы командной строки с помощью parse_args. Проверяет существование указанного zip-файла и, если файл существует, запускает оболочку с помощью функции run_shell.

## Запуск программы

Для запуска потребуется подумать головой и написать:

***Python(py,p) emulator.py --user <имя того кто рискнул> --zip <название пакетика>***

## Тестики

**Тестирование ls**

![image](https://github.com/user-attachments/assets/1dcecc35-dbfc-436c-810b-097f2d7fe06c)

**Тестирование cd**

![image](https://github.com/user-attachments/assets/9c6fd8c1-e1b3-43b6-ba28-d0c2b8524ea7)

**Тестирование cal**

![image](https://github.com/user-attachments/assets/59647f2e-54b9-46e9-b30f-5e11e6fbc7b8)

**Тестирование whoami**

![image](https://github.com/user-attachments/assets/1d268726-24ce-46df-a004-0afcd4ed4735)

**Тестирование mkdir**

![image](https://github.com/user-attachments/assets/ff6a9615-e9e1-4d76-95cc-1625a54b2e30)







