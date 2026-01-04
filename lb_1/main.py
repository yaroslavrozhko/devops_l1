from string_ops import print_string, analyze_case, get_uppercase_list
from my_generator import parity_generator

def main():
    print("--- Робота з рядками ---")
    # Тест функцій
    print_string("Привіт, DevOps!")
    analyze_case("HELLO")
    analyze_case("hello")
    analyze_case("HeLLo")
    
    # Тест обробки помилок
    print("\n--- Тест помилки (передача числа) ---")
    analyze_case(12345)

    # List Comprehension
    print("\n--- List Comprehension ---")
    word = "smogtether"
    upper_list = get_uppercase_list(word)
    print(f"Оригінал: {word}, Список: {upper_list}")

    print("\n--- Генератор ---")
    gen = parity_generator()
    # Виведемо перші 4 значення
    for _ in range(4):
        print(next(gen))

if __name__ == "__main__":
    main()