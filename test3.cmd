@echo off
echo.
echo ===== ТЕСТ 1: Простой граф (макс. глубина 3) =====
python CLI.py --package "A" --repo "test_graph1.txt" --test-mode --version "1.0" --max-depth 3 --filter ""
echo.
pause

echo.
echo ===== ТЕСТ 2: Циклические зависимости =====
python CLI.py --package "A" --repo "test_graph2.txt" --test-mode --version "1.0" --max-depth 5 --filter ""
echo.
pause

echo.
echo ===== ТЕСТ 3: Фильтрация пакетов =====
python CLI.py --package "A" --repo "test_graph3.txt" --test-mode --version "1.0" --max-depth 3 --filter "TEST"
echo.
pause

echo.
echo ===== ТЕСТ 4: Ограничение глубины (глубина 1) =====
python CLI.py --package "A" --repo "test_graph1.txt" --test-mode --version "1.0" --max-depth 1 --filter ""
echo.
pause

echo.
echo ===== ТЕСТ 5: Фильтрация пакетов (исключить EXAM) =====
python CLI.py --package "A" --repo "test_graph3.txt" --test-mode --version "1.0" --max-depth 3 --filter "EXAM"
echo.
pause

echo.
echo ===== ТЕСТ 6: Полный граф без фильтров =====
python CLI.py --package "A" --repo "test_graph1.txt" --test-mode --version "1.0" --max-depth 10 --filter ""
echo.
echo Тестирование завершено!
pause