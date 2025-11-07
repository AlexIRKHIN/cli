@echo off
echo ===== ТЕСТИРОВАНИЕ ЭТАПА 5: ВИЗУАЛИЗАЦИЯ =====

echo.
echo ===== ТЕСТ 1: Визуализация простого графа =====
python CLI.py --package "A" --repo "test_viz1.txt" --test-mode --version "1.0" --max-depth 3 --filter "" --visualize
echo.
pause

echo.
echo ===== ТЕСТ 2: Визуализация с фильтрацией =====
python CLI.py --package "A" --repo "test_viz2.txt" --test-mode --version "1.0" --max-depth 3 --filter "FILTER" --visualize
echo.
pause

echo.
echo ===== ТЕСТ 3: Визуализация сложного графа =====
python CLI.py --package "A" --repo "test_viz3.txt" --test-mode --version "1.0" --max-depth 4 --filter "" --visualize
echo.
echo Тестирование завершено!
pause
