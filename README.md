# Cannabis Data Scraper

A simple Python project to scrape cannabis strain data (terpenes, effects) from Leafly, store it in SQLite, and display it via a Flask web UI.

## Files
- `scraper.py`: Scrapes strain data using Selenium.
- `app.py`: Flask app to display data at `http://localhost:5000/strains`.
- `templates/strains.html`: HTML template for the UI.
- `requirements.txt`: Dependencies.
- `cannabis_data.db`: SQLite database (not in GitHub due to `.gitignore`).

## Setup
1. **Clone the Repo**:
   ```bash
   git clone https://github.com/Glargod/cannabis-data.git
   cd cannabis-data
