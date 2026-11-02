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

# Поддерживаемые алфавиты: ключ - пункт меню, значение - (название, буквы).
# Буквы хранятся только заглавными: строчные получаются из них через lower(),
# поэтому регистр каждой буквы сохраняется при шифровании
ALPHABETS = {
    "1": ("русский", "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"),
    "2": ("английский", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
}

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


def ask_menu(alphabet_name, size):
    # Показывает меню и возвращает выбранный пункт. Неверный пункт не
    # приводит к ошибке: программа поясняет, что можно ввести, и спрашивает снова
    print()
    print(LINE)
    print(f"Алфавит: {alphabet_name} ({size} {letters_word(size)})")
    print("  1 - Зашифровать текст")
    print("  2 - Расшифровать текст")
    print("  3 - Сменить алфавит")
    print("  0 - Выход")
    while True:
        choice = input("Выберите действие: ").strip()
        if choice in ("1", "2", "3", "0"):
            return choice
        if choice == "":
            print("  Ошибка: ничего не введено. Введите 1, 2, 3 или 0.")
        else:
            print(f"  Ошибка: пункта «{choice}» нет в меню. Введите 1, 2, 3 или 0.")


def ask_alphabet(current):
    # Выбор алфавита. Enter оставляет текущий алфавит, чтобы случайный
    # заход в этот пункт ничего не менял
    print()
    print("Доступные алфавиты:")
    for key, (name, letters) in ALPHABETS.items():
        print(f"  {key} - {name} ({len(letters)} {letters_word(len(letters))}: "
              f"{letters[0]}...{letters[-1]})")
    while True:
        choice = input("Выберите алфавит (Enter - оставить текущий): ").strip()
        if choice == "":
            return current
        if choice in ALPHABETS:
            return choice
        print(f"  Ошибка: алфавита «{choice}» нет. Введите "
              + " или ".join(ALPHABETS) + ".")


def ask_text(alphabet, alphabet_name):
    # Запрашивает строку. Пустая строка не принимается. Если в строке нет
    # ни одной буквы выбранного алфавита, шифрование её не изменит, -
    # программа сообщает об этом и просит ввести текст ещё раз. Если текст
    # написан буквами другого алфавита, подсказывает, как его сменить.
    # Ввод 0 возвращает в меню (возвращается None)
    while True:
        text = input("Введите строку (0 - вернуться в меню): ")
        if text.strip() == "0":
            return None
        if text.strip() == "":
            print("  Ошибка: строка пустая. Введите текст.")
            continue
        if any(ch.upper() in alphabet for ch in text):
            return text
        print(f"  Ошибка: в строке нет букв алфавита ({alphabet_name}), "
              "сдвигать нечего.")
        for name, letters in ALPHABETS.values():
            if letters != alphabet and any(ch.upper() in letters for ch in text):
                print(f"  Похоже, текст написан буквами алфавита «{name}». "
                      "Введите 0 и смените алфавит в меню (пункт 3).")
                break


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


def run_action(choice, key):
    # Выполняет шифрование (пункт 1) или расшифровку (пункт 2)
    name, alphabet = ALPHABETS[key]
    encrypt = choice == "1"
    print()
    print("ШИФРОВАНИЕ" if encrypt else "РАСШИФРОВКА")
    text = ask_text(alphabet, name)
    if text is None:
        return                      # пользователь вернулся в меню
    shift = ask_shift(len(alphabet))
    result = caesar(text, shift if encrypt else -shift, alphabet)
    print()
    label = ("Зашифрованная" if encrypt else "Расшифрованная") + " строка:"
    print(f"{'Исходная строка:':<24}{text}")
    print(f"{'Шаг сдвига:':<24}{shift}")
    print(f"{label:<24}{result}")


def main():
    key = "1"                       # по умолчанию русский алфавит
    while True:
        name, alphabet = ALPHABETS[key]
        choice = ask_menu(name, len(alphabet))
        if choice == "0":
            print("Работа программы завершена.")
            return
        if choice == "3":
            key = ask_alphabet(key)
            print(f"Выбран алфавит: {ALPHABETS[key][0]}.")
        else:
            run_action(choice, key)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C или Ctrl+Z/Ctrl+D - завершаем без длинного сообщения об ошибке
        print("\nРабота программы прервана пользователем.")
