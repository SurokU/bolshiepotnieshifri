# Лабораторная работа - шифр Цезаря
# Шифрование и расшифровка текста шифром Цезаря (шифром сдвига).
# Исполнитель: Сурков Владимир Андреевич, группа Фт-250008

ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def caesar(text, shift, alphabet):
    # Сдвигает каждую букву алфавита на shift позиций вправо по кругу.
    # Для расшифровки функция вызывается с отрицательным сдвигом.
    # Заглавные буквы заменяются заглавными, строчные - строчными,
    # остальные символы остаются без изменений
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


def main():
    while True:
        print()
        print("ШИФР ЦЕЗАРЯ")
        print("  1 - Зашифровать текст")
        print("  2 - Расшифровать текст")
        print("  0 - Выход")
        choice = input("Выберите действие: ")
        if choice == "0":
            return
        if choice not in ("1", "2"):
            print("Нет такого пункта меню.")
            continue
        text = input("Введите строку: ")
        shift = int(input("Введите шаг сдвига: "))
        if choice == "1":
            print("Зашифрованная строка:", caesar(text, shift, ALPHABET))
        else:
            print("Расшифрованная строка:", caesar(text, -shift, ALPHABET))


main()
