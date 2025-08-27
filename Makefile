setup:
	pip install -e .
	alembic upgrade head

run:
	uvicorn app.main:app --reload

sync-mtg:
	python scripts/sync_mtg.py

sync-pokemon:
	python scripts/sync_pokemon.py

build-index:
	python scripts/build_index.py
