import unittest
from string_ops import analyze_case, get_uppercase_list
from my_generator import parity_generator

class TestDevOpsTasks(unittest.TestCase):

    def test_analyze_case(self):
        self.assertEqual(analyze_case("ABC"), "Всі літери великі")
        self.assertEqual(analyze_case("abc"), "Всі літери малі")
        self.assertEqual(analyze_case("AbC"), "Змішаний регістр")
        self.assertEqual(analyze_case(123), "Error") # Тест на помилку

    def test_list_comprehension(self):
        result = get_uppercase_list("smogtether")
        expected = ['S', 'M', 'O', 'G', 'T', 'E', 'T', 'H', 'E', 'R']
        self.assertEqual(result, expected)

    def test_generator(self):
        gen = parity_generator()
        self.assertEqual(next(gen), "Парне")
        self.assertEqual(next(gen), "Непарне")
        self.assertEqual(next(gen), "Парне")

if __name__ == '__main__':
    unittest.main()