# Sailboat Charter Price Suggestion System

Full-stack web application that suggests weekly charter prices for sailboats in Croatia based on historical charter statistics from the Yacht-Rent website.

The project covers the full workflow:

- Data scraping
- Database creation
- Backend API
- Frontend user interface

---

## Authors

- Jan Antos
- Michał Hacaś
- Adam Radecki

---

## Technologies

- Python 3
- FastAPI
- SQLite
- Requests
- BeautifulSoup4
- HTML, CSS, JavaScript

---

## Project Structure

GroupProject/

- scrapper.py
- main.py
- final_database.db
- requirements.txt
- frontend/
  - index.html
  - style.css
  - script.js

---

## Installation

Install required libraries:

pip install -r requirements.txt

(Optional) Download fresh data:

python scraper.py

Run backend server:

python main.py

---

## Running the application

Backend address:

http://127.0.0.1:8000

Frontend:

http://127.0.0.1:8000/app

Swagger API documentation:

http://127.0.0.1:8000/docs

---

## Database Schema (sailboat_prices)

- id, INTEGER, Primary key
- date, TEXT, Charter start date
- cabins, TEXT, Cabin count category (0-1,2,3,4,5-6,7-9)
- berths, INTEGER, Number of berths (automatically mapped based on cabin count)
- length, INTEGER, Average yacht length in meters (automatically mapped based on cabin count)
- price_euro, INTEGER, Weekly charter price for the yacht
- boat_type, TEXT, Type of the boat (e.g. Catamarans, Sailing yachts or All Boats)
- country, TEXT, Country name (Croatia)
- region, TEXT, Specific location (e.g. Split, Dalmatia or All Regions)

---

## API Endpoints

GET /api/form-options  
Returns available values for form fields.

GET /api/suggest-price

Parameters:

- date (required)
- boat_type (optional)
- region (optional)
- cabins (optional)
- berths (optional)
- length (optional)

Example:

/api/suggest-price?date=2026-07-04&region=Split

Response:

{
"suggested_price_euro": 11742,
"input_data": {
"date": "2026-07-04",
"region": "Split",
"type": null,
"details": {
"cabins": null,
"berths": null,
"length": null
}
}
}

---

## Pricing Logic

The system extracts the month from the selected date, filters database records using selected parameters and calculates the average weekly price from matching results.

If no matching records are found, the system returns no result.

---