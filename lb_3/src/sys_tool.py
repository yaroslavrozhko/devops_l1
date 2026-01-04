import sys

def main():
    # Перевірка на наявність аргументу --help
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Довідка: Цей скрипт демонструє роботу з sys.argv.")
        print("Використання: python src/sys_tool.py")
        return

    print("командна строка")

# Цей блок виконується тільки якщо файл запущено напряму,
# а не імпортовано як модуль
if __name__ == "__main__":
    main()