.PHONY: test refresh_db smoke migrate dummy_data


refresh_db: migrate dummy_data

test:
	@echo "\n⭐ Running unit tests\n"
	python -m unittest

smoke: refresh_db
	@echo "\n⭐ Running smoke test\n"
	./smoke_test.sh

migrate:
	@echo "\n⭐ Running migrations\n"
	./migrate.py

dummy_data:
	@echo "\n⭐ Populating database with dummy data\n"
	./populate_db_with_dummy_data.sh
