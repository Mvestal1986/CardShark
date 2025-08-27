# TCGScan

A Python-first web app to scan and identify MTG & Pokémon cards, fetch metadata, manage collections, and build virtual decks.

## Features
- Upload card photos → auto-identify card with OpenCV + FAISS recognizer.
- Metadata from [Scryfall API](https://scryfall.com/docs/api) (MTG) and [Pokémon TCG API](https://docs.pokemontcg.io/).
- Daily pricing snapshots (Scryfall for MTG, TCGplayer for Pokémon).
- Weekly legality sync.
- Collection and deck management with FastAPI + Jinja2 templates.

## Repo Structure
```
app/                # FastAPI application code
├─ main.py
├─ config.py
├─ models.py
├─ schemas.py
├─ services/        # recognition, catalog sync, pricing, legality
├─ routes/          # API routes
├─ templates/       # Jinja2 templates
├─ static/          # CSS/JS
├─ workers/         # schedulers and background jobs
scripts/            # one-off sync/build scripts
data/               # cached images, uploads
alembic/            # migrations
tests/              # pytest unit tests
```

## Quickstart
```bash
# Install dependencies
pip install -e .

# Run DB migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

## License
MIT License
