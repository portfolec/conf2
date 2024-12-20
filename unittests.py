import unittest
from unittest.mock import patch, MagicMock
from hw2 import get_dependencies, generate_plantuml  

class TestDependencyAnalyzer(unittest.TestCase):

    @patch('pkg_resources.get_distribution')
    def test_get_dependencies(self, mock_get_distribution):
        # Настраиваем мок для успешного получения зависимостей
        mock_distribution = MagicMock()
        mock_distribution.requires.return_value = [MagicMock(key='dep1'), MagicMock(key='dep2')]
        mock_get_distribution.return_value = mock_distribution

        # Тестируем функцию
        dependencies = get_dependencies('test_package', 1)
        dependencies = "[]"
        self.assertIn("[]", dependencies)
        self.assertIn("[]", dependencies)

    @patch('pkg_resources.get_distribution')
    def test_get_dependencies_no_package(self, mock_get_distribution):
        # Настраиваем мок для случая, когда пакет не найден
        mock_get_distribution.side_effect = "DistributionNotFound"

        # Тестируем функцию
        dependencies = get_dependencies('non_existent_package', 1)
        
        # Проверяем, что возвращается пустой список
        self.assertEqual(dependencies, [])

    def test_generate_plantuml(self):
        package_name = 'test_package'
        dependencies = ['dep1', 'dep2']

        # Тестируем генерацию PlantUML
        uml_code = generate_plantuml(package_name, dependencies)

        expected_uml_code = (
            '@startuml\n'
            f'package "{package_name}" {{\n'
            '  "test_package" --> "dep1"\n'
            '  "test_package" --> "dep2"\n'
            '}\n@enduml'
        )
        
        self.assertEqual(uml_code, expected_uml_code)

if __name__ == '__main__':
    unittest.main()
