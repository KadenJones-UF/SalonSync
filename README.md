# SalonSync

Structured color-formula notetaking for professional hairstylists.
Stylists record the brand, shades, developer, and timing behind every
client color service — searchable and shareable
to a moderated community feed.

**Course:** CEN 3031 — Fall 2026, Section 10706

## Team Members

- Angela Nano — Product Manager / Developer
- Zachary Bon — Scrum Master / Developer
- Kaden Jones — Developer

## Tech Stack

React · Python/Flask · PostgreSQL · GitHub Actions (CI)

## Project Status

🚧 Iteration 1 — Planning & Design. See the (https://github.com/users/zbon0830/projects/1/views/2).

## Getting Started

You'll need Python 3.12+ and Docker (for Postgres). On Windows, activate the venv with `.venv\Scripts\activate` instead.

```bash
docker compose up -d
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask db upgrade
flask run
```

The API runs at http://localhost:5000 — check http://localhost:5000/api/health to make sure it's up.

Run the tests with `pytest` from the `backend` folder.
