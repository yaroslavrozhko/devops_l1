import fire
import sys
import os

# Додаємо поточну директорію в шлях, щоб імпорт utils працював коректно
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import utils

if __name__ == '__main__':
    # Fire автоматично створює CLI з переданого об'єкта або словника
    fire.Fire({
        'greet': utils.greet,
        'goodbye': utils.goodbye
    })