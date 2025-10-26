# build.ps1 - PowerShell аналог Makefile

param(
    [string]$Target = "help"
)

switch ($Target) {
    "install" {
        poetry install
    }
    "project" {
        poetry run project
    }
    "build" {
        poetry build
    }
    "publish" {
        poetry publish --dry-run
    }
    "package-install" {
        pip install dist/*.whl
    }
    "lint" {
        poetry run ruff check .
    }
    "help" {
        Write-Host "Доступные команды:"
        Write-Host "  .\build.ps1 install        - установка зависимостей"
        Write-Host "  .\build.ps1 project        - запуск проекта"
        Write-Host "  .\build.ps1 build          - сборка пакета"
        Write-Host "  .\build.ps1 publish        - тест публикации"
        Write-Host "  .\build.ps1 package-install- установка пакета в систему"
        Write-Host "  .\build.ps1 lint           - проверка кода"
    }
}