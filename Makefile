.PHONY: help setup install test lint format type-check pre-commit \
         db-up db-down db-status docker-up docker-down clean run

help:
	@echo "Wallet API - Available commands:"
	@echo ""
	@echo "    make setup      - Full development setup"
	@echo "    make install    - Install main dependencies"
	@echo ""
	@echo "    make lint       - Code style check (flake8)"
	@echo "    make format     - Format code (black + isort)"
	@echo "    make type-check - Type checking (mypy)"
	@echo "    make pre-commit - Run all pre-commit checks"
	@echo "    make test       - Run tests"
	@echo ""
	@echo "    make db-up      - Start DB in Docker"
	@echo "    make db-down    - Stop DB"
	@echo "    make db-status  - Check DB status"
	@echo "    make db-migrate - Apply migrations"
	@echo ""
	@echo "    make docker-up   - Start all services (DB + app)"
	@echo "    make docker-down - Stop all services"
	@echo ""
	@echo "    make run        - Run app locally"
	@echo "    make clean      - Clear cache and temp files"
	@echo "    make all-checks - Run all checks before commit"

setup:
	poetry install --with dev
	poetry run pre-commit install --hook-type pre-commit
	poetry run pre-commit install --hook-type commit-msg
	@poetry run pre-commit run --all-files

install:
	poetry install --no-interaction --no-ansi

lint:
	poetry run flake8 app/ --config .flake8

format:
	poetry run black app/ --config pyproject.toml
	poetry run isort app/ --settings-path pyproject.toml

type-check:
	poetry run mypy app/ --config-file pyproject.toml

pre-commit:
	poetry run pre-commit run --all-files

#test:
#	@echo "Запуск тестов..."
#	poetry run pytest -v

db-up:
	docker-compose up -d db
	@echo "Ожидание готовности БД..."
	@sleep 3
	@docker-compose ps db | grep "healthy" && echo " БД запущена и готова" || echo "БД запущена, но проверка здоровья не пройдена"

db-down:
	@echo "🛑 Остановка БД..."
	docker-compose stop db
	@echo "✅ БД остановлена"

db-status:
	@docker-compose ps db

db-migrate:
	poetry run alembic upgrade head

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	@docker-compose logs -f app

run:
	@echo "Запуск Wallet API..."
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf htmlcov/ 2>/dev/null || true
	@echo "✅ Очистка завершена"

all-checks: lint type-check test pre-commit
	@echo "✅ Все проверки пройдены!"
