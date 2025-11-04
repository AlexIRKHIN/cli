@echo off
echo ===== ТЕСТИРОВАНИЕ ЭТАПА 4: ДОПОЛНИТЕЛЬНЫЕ ОПЕРАЦИИ =====
echo.

echo ===== ТЕСТ 1: Простой граф с порядком загрузки =====
python CLI.py --package "A" --repo "test_graph1.txt" --test-mode --version "1.0" --max-depth 3 --filter "" --show-order
echo.
pause

echo.
echo ===== ТЕСТ 2: Граф с циклическими зависимостями =====
python CLI.py --package "A" --repo "test_complex.txt" --test-mode --version "1.0" --max-depth 5 --filter "" --show-order
echo.
pause

echo.
echo ===== ТЕСТ 3: С фильтрацией и порядком загрузки =====
python CLI.py --package "A" --repo "test_graph3.txt" --test-mode --version "1.0" --max-depth 3 --filter "TEST" --show-order
echo.
echo Тестирование завершено!
pause