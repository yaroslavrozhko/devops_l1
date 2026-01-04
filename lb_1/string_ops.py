def print_string(text):
    """Приймає рядок і виводить його."""
    if not isinstance(text, str):
        print(f"Помилка: Очікувався рядок, отримано {type(text).__name__}")
        return
    print(text)

def analyze_case(text):
    """Аналізує регістр літер у рядку."""
    if not isinstance(text, str):
        print(f"Помилка: Очікувався рядок, отримано {type(text).__name__}")
        return "Error"

    if text.isupper():
        info = "Всі літери великі"
    elif text.islower():
        info = "Всі літери малі"
    else:
        info = "Змішаний регістр"
    
    print(f"Інформація про рядок '{text}': {info}")
    return info

def get_uppercase_list(word):
    """Повертає список великих літер (List Comprehension)."""
    if not isinstance(word, str):
        print("Помилка: вхідні дані мають бути рядком")
        return []
    return [char.upper() for char in word]