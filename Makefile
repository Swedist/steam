.PHONY: help fmt fmt-isort fmt-black fmt-ruff lint test install

SRC = lib/steam

help:
	@echo "🚀 Доступные команды:"
	@echo "  make install     - Установить зависимости через poetry"
	@echo "  make fmt         - Запустить автоформатирование (isort, black, ruff)"
	@echo "  make lint        - Проверить стиль кода без исправлений"

install:
	poetry install

fmt-isort:
	@echo "=== ISORT ==="
	poetry run isort $(SRC)

fmt-black:
	@echo "=== BLACK ==="
	poetry run black $(SRC)

fmt-ruff:
	@echo "=== RUFF ==="
	poetry run ruff check --fix $(SRC)

fmt: fmt-isort fmt-black fmt-ruff

lint:
	@echo "=== LINT ==="
	poetry run isort --check-only $(SRC)
	poetry run black --check $(SRC)
	poetry run ruff check $(SRC)
