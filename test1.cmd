@echo off
echo ===== ТЕСТ 1: Корректные параметры =====
python CLI.py --package "commons-lang:commons-lang" --repo "https://repo1.maven.org/maven2" --version "2.6" --max-depth 2 --filter "test"
echo.
pause

echo ===== ТЕСТ 2: Тестовый режим =====
python CLI.py --package "A" --repo "./test-data.txt" --test-mode --version "1.0" --max-depth 3 --filter "temp"
echo.
pause

echo ===== ТЕСТ 3: Ошибка - отрицательная глубина =====
python CLI.py --package "test" --repo "repo" --version "1.0" --max-depth -1
echo.
pause

echo ===== ТЕСТ 4: Ошибка - отсутствует версия =====
python CLI.py --package "test" --repo "repo" --max-depth 2
echo.
pause

echo ===== ТЕСТ 5: Справка =====
python CLI.py --help
echo.
pause