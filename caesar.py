# Лабораторная работа - шифр Цезаря
# Шифрование и расшифровка текста шифром Цезаря (шифром сдвига).
# Исполнитель: Сурков Владимир Андреевич, группа Фт-250008

import sys

# Ввод и вывод в UTF-8, чтобы русские буквы правильно читались и печатались
# в любой консоли Windows, в том числе в Git Bash
try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stdin.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Алфавит хранится только заглавными буквами: строчные получаются через
# lower(), поэтому регистр каждой буквы сохраняется при шифровании
ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

LINE = "=" * 16 + " ШИФР ЦЕЗАРЯ " + "=" * 16


def letters_word(n):
    # Склонение слова «буква» после числа: 21 буква, 33 буквы, 26 букв
    if n % 10 == 1 and n % 100 != 11:
        return "буква"
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return "буквы"
    return "букв"


def caesar(text, shift, alphabet):
    # Сдвигает каждую букву алфавита на shift позиций вправо по кругу
    # (после последней буквы снова идёт первая). Для расшифровки функция
    # вызывается с отрицательным сдвигом. Заглавные буквы заменяются
    # заглавными, строчные - строчными. Цифры, знаки препинания, пробелы
    # и буквы других алфавитов не входят в алфавит и остаются без изменений
    upper = alphabet
    lower = alphabet.lower()
    n = len(alphabet)
    result = []
    for ch in text:
        if ch in upper:
            result.append(upper[(upper.index(ch) + shift) % n])
        elif ch in lower:
            result.append(lower[(lower.index(ch) + shift) % n])
        else:
            result.append(ch)
    return "".join(result)


def ask_menu(size):
    # Показывает меню и возвращает выбранный пункт. Неверный пункт не
    # приводит к ошибке: программа поясняет, что можно ввести, и спрашивает снова
    print()
    print(LINE)
    print(f"Алфавит: русский ({size} {letters_word(size)})")
    print("  1 - Зашифровать текст")
    print("  2 - Расшифровать текст")
    print("  0 - Выход")
    while True:
        choice = input("Выберите действие: ").strip()
        if choice in ("1", "2", "0"):
            return choice
        if choice == "":
            print("  Ошибка: ничего не введено. Введите 1, 2 или 0.")
        else:
            print(f"  Ошибка: пункта «{choice}» нет в меню. Введите 1, 2 или 0.")


def ask_text(alphabet):
    # Запрашивает строку. Пустая строка и строка без букв алфавита не
    # принимаются: шифрование такой строки ничего бы не изменило
    while True:
        text = input("Введите строку: ")
        if text.strip() == "":
            print("  Ошибка: строка пустая. Введите текст.")
        elif not any(ch.upper() in alphabet for ch in text):
            print("  Ошибка: в строке нет русских букв, сдвигать нечего.")
        else:
            return text


def ask_shift(size):
    # Запрашивает шаг сдвига - целое число от 1 до размера алфавита.
    # Больший шаг запрещён условием задачи, отрицательный не нужен:
    # для сдвига в обратную сторону служит пункт «Расшифровать»
    while True:
        raw = input(f"Введите шаг сдвига (целое число от 1 до {size}): ").strip()
        if raw == "":
            print("  Ошибка: шаг не введён.")
            continue
        try:
            shift = int(raw)
        except ValueError:
            try:
                float(raw.replace(",", "."))
                print(f"  Ошибка: «{raw}» - дробное число, шаг должен быть целым.")
            except ValueError:
                print(f"  Ошибка: «{raw}» не является числом.")
            continue
        if shift < 1:
            print("  Ошибка: шаг должен быть не меньше 1. Для сдвига в обратную "
                  "сторону выберите расшифровку.")
        elif shift > size:
            print(f"  Ошибка: шаг не может быть больше размера алфавита ({size}).")
        else:
            if shift == size:
                print(f"  Внимание: сдвиг на {size} - полный круг, "
                      "текст не изменится.")
            return shift


def run_action(choice):
    # Выполняет шифрование (пункт 1) или расшифровку (пункт 2)
    encrypt = choice == "1"
    print()
    print("ШИФРОВАНИЕ" if encrypt else "РАСШИФРОВКА")
    text = ask_text(ALPHABET)
    shift = ask_shift(len(ALPHABET))
    result = caesar(text, shift if encrypt else -shift, ALPHABET)
    print()
    label = ("Зашифрованная" if encrypt else "Расшифрованная") + " строка:"
    print(f"{'Исходная строка:':<24}{text}")
    print(f"{'Шаг сдвига:':<24}{shift}")
    print(f"{label:<24}{result}")


def main():
    while True:
        choice = ask_menu(len(ALPHABET))
        if choice == "0":
            print("Работа программы завершена.")
            return
        run_action(choice)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C или Ctrl+Z/Ctrl+D - завершаем без длинного сообщения об ошибке
        print("\nРабота программы прервана пользователем.")
