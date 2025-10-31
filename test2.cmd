@echo off
echo ===== ТЕСТ 1: Apache Commons Lang =====
python CLI.py --package "org.apache.commons:commons-lang3" --repo "https://repo1.maven.org/maven2" --version "3.12.0" --max-depth 1 --filter ""
echo.
pause

echo ===== ТЕСТ 2: JUnit =====
python CLI.py --package "junit:junit" --repo "https://repo1.maven.org/maven2" --version "4.13.2" --max-depth 1 --filter ""
echo.
pause

echo ===== ТЕСТ 3: Mockito =====
python CLI.py --package "org.mockito:mockito-core" --repo "https://repo1.maven.org/maven2" --version "4.11.0" --max-depth 1 --filter ""
echo.
pause

echo ===== ТЕСТ 4: Несуществующий пакет =====
python CLI.py --package "com.nonexistent:fake-package" --repo "https://repo1.maven.org/maven2" --version "1.0.0" --max-depth 1 --filter ""
echo.
pause

echo ===== ТЕСТ 5: Неправильный формат пакета =====
python CLI.py --package "invalid-format" --repo "https://repo1.maven.org/maven2" --version "1.0.0" --max-depth 1 --filter ""
echo.
pause