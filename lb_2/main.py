import json
import csv
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

# ---------------------------------------------------------
# 1. Клас СТУДЕНТ (Інкапсуляція)
# ---------------------------------------------------------
class Student:
    def __init__(self, full_name, group, birth_date):
        # Приватні поля
        self.__full_name = full_name
        self.__group = group
        self.__birth_date = birth_date

    # Гетери (Getters)
    @property
    def full_name(self):
        return self.__full_name

    @property
    def group(self):
        return self.__group

    @property
    def birth_date(self):
        return self.__birth_date

    # Сетери (Setters) - приклад валідації
    @full_name.setter
    def full_name(self, value):
        if isinstance(value, str) and value:
            self.__full_name = value
        else:
            raise ValueError("Ім'я повинно бути непорожнім рядком")

# ---------------------------------------------------------
# 2. Клас УСПІШНІСТЬ (Абстракція)
# ---------------------------------------------------------
class Performance(ABC):
    def __init__(self, subjects: list, scores: list):
        self._subjects = subjects
        self._scores = scores

    @abstractmethod
    def average_score(self):
        pass

    def get_details(self):
        return dict(zip(self._subjects, self._scores))

# Реальна успішність (не вимагалася явно, але потрібна логічно для "Реальної успішності")
class RealPerformance(Performance):
    def average_score(self):
        if not self._scores:
            return 0.0
        return round(sum(self._scores) / len(self._scores), 2)

# ---------------------------------------------------------
# 3. Клас БАЖАНА_УСПІШНІСТЬ (Спадкування)
# ---------------------------------------------------------
class DesiredPerformance(Performance):
    def __init__(self, subjects, scores, target_average):
        super().__init__(subjects, scores)
        self.__target_average = target_average

    def average_score(self):
        # Повертає бажаний бал, введений студентом (як в умові)
        return self.__target_average

# ---------------------------------------------------------
# 4. Клас ДАНІ_СТУДЕНТА (Агрегація)
# ---------------------------------------------------------
class StudentData:
    def __init__(self, student: Student, real_perf: RealPerformance, desired_perf: DesiredPerformance):
        self.student = student
        self.real_perf = real_perf
        self.desired_perf = desired_perf

    def get_consolidated_dict(self):
        """Збирає дані з усіх об'єктів у єдиний словник"""
        return {
            "Student_Info": {
                "Full_Name": self.student.full_name,
                "Group": self.student.group,
                "Birth_Date": self.student.birth_date
            },
            "Real_Performance": {
                "Subjects": self.real_perf.get_details(),
                "Average_Score": self.real_perf.average_score()
            },
            "Desired_Performance": {
                "Desired_Scores": self.desired_perf.get_details(),
                "Target_Average_Score": self.desired_perf.average_score()
            }
        }

# ---------------------------------------------------------
# 5. Абстрактний клас ЗБЕРЕЖЕННЯ_ДАНИХ (Стратегія)
# ---------------------------------------------------------
class DataSaver(ABC):
    @abstractmethod
    def save(self, data_dict, filename_prefix, work_number):
        pass

    def _generate_filename(self, data_dict, work_number, extension):
        # Формат: ПІБ_ГРУПА_НОМЕР-РОБОТИ.ФОРМАТ
        # Прибираємо пробіли з імені для назви файлу
        name_slug = data_dict['Student_Info']['Full_Name'].replace(" ", "_")
        group_slug = data_dict['Student_Info']['Group']
        return f"{name_slug}_{group_slug}_{work_number}.{extension}"

# ---------------------------------------------------------
# 6. Класи збереження у конкретні формати
# ---------------------------------------------------------
class JsonSaver(DataSaver):
    def save(self, data_dict, work_number):
        filename = self._generate_filename(data_dict, work_number, "json")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=4)
            print(f"[OK] Дані збережено у файл: {filename}")
        except IOError as e:
            print(f"[Error] Помилка запису JSON: {e}")

class XmlSaver(DataSaver):
    def save(self, data_dict, work_number):
        filename = self._generate_filename(data_dict, work_number, "xml")
        
        # Створення кореневого елемента
        root = ET.Element("StudentData")

        # Рекурсивна функція для перетворення dict в XML
        def build_xml(parent_el, data):
            for key, value in data.items():
                # Замінюємо пробіли в ключах, бо XML теги не можуть мати пробіли
                tag_name = str(key).replace(" ", "_")
                if isinstance(value, dict):
                    child = ET.SubElement(parent_el, tag_name)
                    build_xml(child, value)
                else:
                    child = ET.SubElement(parent_el, tag_name)
                    child.text = str(value)

        build_xml(root, data_dict)
        
        tree = ET.ElementTree(root)
        try:
            # indent додано в Python 3.9+, для старіших версій потрібен інший підхід
            ET.indent(tree, space="    ", level=0) 
            tree.write(filename, encoding="utf-8", xml_declaration=True)
            print(f"[OK] Дані збережено у файл: {filename}")
        except Exception as e:
            print(f"[Error] Помилка запису XML: {e}")

class CsvSaver(DataSaver):
    def save(self, data_dict, work_number):
        filename = self._generate_filename(data_dict, work_number, "csv")
        
        # Для CSV потрібно "сплющити" вкладений словник
        flat_data = {}
        
        flat_data['Full_Name'] = data_dict['Student_Info']['Full_Name']
        flat_data['Group'] = data_dict['Student_Info']['Group']
        flat_data['Birth_Date'] = data_dict['Student_Info']['Birth_Date']
        
        # Додаємо реальні оцінки (як рядок)
        flat_data['Real_Subjects'] = str(data_dict['Real_Performance']['Subjects'])
        flat_data['Real_Average'] = data_dict['Real_Performance']['Average_Score']
        
        # Додаємо бажані
        flat_data['Desired_Scores'] = str(data_dict['Desired_Performance']['Desired_Scores'])
        flat_data['Desired_Average'] = data_dict['Desired_Performance']['Target_Average_Score']

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=flat_data.keys())
                writer.writeheader()
                writer.writerow(flat_data)
            print(f"[OK] Дані збережено у файл: {filename}")
        except IOError as e:
             print(f"[Error] Помилка запису CSV: {e}")

# ---------------------------------------------------------
# MAIN - Демонстрація роботи
# ---------------------------------------------------------
if __name__ == "__main__":
    # 1. Створення студента
    student = Student("Петренко Олександр Петрович", "IP-11", "2006-05-20")

    # 2. Створення реальної успішності
    subjects = ["DevOps", "Python", "Linux", "Databases"]
    real_scores = [85, 90, 78, 88]
    real_perf = RealPerformance(subjects, real_scores)

    # 3. Створення бажаної успішності
    # Студент хоче мати вищі бали і середній бал 95.0
    desired_scores = [95, 95, 95, 95]
    desired_perf = DesiredPerformance(subjects, desired_scores, target_average=95.0)

    # 4. Агрегація даних (Паттерн Facade/Builder)
    student_data_manager = StudentData(student, real_perf, desired_perf)
    
    # Отримуємо єдиний словник з усіма даними
    final_data = student_data_manager.get_consolidated_dict()
    
    # Виведення в консоль для перевірки
    print("--- Зібрані дані ---")
    print(final_data)
    print("--------------------")

    # 5. Збереження даних (Вибір стратегії)
    work_num = "PR5"
    
    # Збереження в JSON
    json_saver = JsonSaver()
    json_saver.save(final_data, work_num)

    # Збереження в XML
    xml_saver = XmlSaver()
    xml_saver.save(final_data, work_num)

    # Збереження в CSV
    csv_saver = CsvSaver()
    csv_saver.save(final_data, work_num)