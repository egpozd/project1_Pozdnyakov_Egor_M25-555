install:
	poetry install

project:
	poetry run project

run:
	poetry run python labyrinth_game/main.py

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python -m pip install dist/*.whl

lint:
	poetry run ruff check labyrinth_game/

clean:
	rm -rf __pycache__
	rm -rf labyrinth_game/__pycache__
	rm -rf .pytest_cache