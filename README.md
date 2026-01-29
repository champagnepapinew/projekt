# Sailboat Charter Price Suggestion System

Full-stack web application that suggests weekly charter prices for sailboats in Croatia based on historical charter statistics from the Yacht-Rent website.

The project covers the full workflow:
- Data scraping
- Database creation
- Backend API
- Frontend user interface

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
- scraper.py
- main.py
- charter_data.db
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

- id (INTEGER, primary key)
- date (TEXT)
- cabins (TEXT)
- berths (INTEGER)
- length (INTEGER)
- price_euro (INTEGER)
- boat_type (TEXT)
- country (TEXT)
- region (TEXT)

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

/api/suggest-price?date=2025-07-15&region=Split

Response:

{
  "suggested_price_euro": 11742
}

---

## Pricing Logic

The system extracts the month from the selected date, filters database records using selected parameters and calculates the average weekly price from matching results.

If no matching records are found, the system returns no result.

---

## Authors

Group project – Web Programming course
