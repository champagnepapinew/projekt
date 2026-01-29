import requests
from bs4 import BeautifulSoup
import sqlite3
import re


def clean_value(text):
    if not text:
        return 0
    text = text.replace('€', '').replace(' ', '').replace(',', '')
    try:
        return int(float(text))
    except:
        return 0


def get_mappings(cabin):
    mapping = {
        "0-1": {"berths": 2, "length": 8},
        "2": {"berths": 4, "length": 10},
        "3": {"berths": 6, "length": 12},
        "4": {"berths": 8, "length": 14},
        "5-6": {"berths": 12, "length": 16},
        "7-9": {"berths": 16, "length": 20}
    }

    return mapping.get(cabin, None)


def setup_database():
    conn = sqlite3.connect('final_database.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS sailboat_prices')
    cursor.execute('''
        CREATE TABLE sailboat_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            cabins TEXT,
            berths INTEGER,
            length INTEGER,
            price_euro INTEGER,
            boat_type TEXT,
            country TEXT,
            region TEXT
        )
    ''')

    conn.commit()
    return conn


def scrape_data(url, boat_type, region, cursor):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200: return
        soup = BeautifulSoup(res.text, 'html.parser')

        price_graphs = [g for g in soup.find_all('g', class_='data', id=re.compile(r'^graphPRICE'))
                        if "PER" not in g.get('id', '')]

        for graph in price_graphs:
            cabin_val = graph.get('id').replace('graphPRICE', '')
            maps = get_mappings(cabin_val)
            if maps is None:
                continue
            price_points = graph.find_all('text', class_='label-text')

            for p in price_points:
                try:
                    price = clean_value(p.get_text(strip=True).split('€')[0])
                    date = p.find('tspan', class_='label').get_text(strip=True)
                    cursor.execute('''
                        INSERT INTO sailboat_prices (date, cabins, berths, length, price_euro, boat_type, country, region)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (date, cabin_val, maps['berths'], maps['length'], price, boat_type, "Croatia", region))
                except:
                    continue
    except:
        pass


def run_scraper():
    conn = setup_database()
    cursor = conn.cursor()
    base_url = "https://www.yacht-rent.com/yacht-charter-statistics-charts?country_id=1"

    YEARS = [2020, 2021, 2022, 2023, 2024, 2025]

    BOAT_TYPES = [
        {"name": "Catamarans", "id": "7"},
        {"name": "Motor Yachts", "id": "6"},
        {"name": "Motorsailers", "id": "8"},
        {"name": "Sailing yachts", "id": "5"},
        {"name": "Gulets / Schooners", "id": "247"}
    ]

    REGIONS = [
        {"name": "Biograd na moru", "id": "13"},
        {"name": "Dubrovnik", "id": "14"},
        {"name": "Jezera", "id": "226"},
        {"name": "Kaštela", "id": "15"},
        {"name": "Krk", "id": "16"},
        {"name": "Lošinj", "id": "17"},
        {"name": "Makarska", "id": "18"},
        {"name": "Marina", "id": "19"},
        {"name": "Murter", "id": "20"},
        {"name": "Novi Vinodolski", "id": "238"},
        {"name": "Opatija", "id": "21"},
        {"name": "Pirovac", "id": "222"},
        {"name": "Primošten", "id": "23"},
        {"name": "Pula", "id": "24"},
        {"name": "Rijeka", "id": "25"},
        {"name": "Rogoznica", "id": "26"},
        {"name": "Rovinj", "id": "27"},
        {"name": "Split", "id": "30"},
        {"name": "Sukošan", "id": "31"},
        {"name": "Trogir", "id": "32"},
        {"name": "Vodice", "id": "34"},
        {"name": "Vrsar", "id": "35"},
        {"name": "Zadar", "id": "36"},
        {"name": "Šibenik", "id": "28"},
        {"name": "Šolta", "id": "29"}
    ]

    for year in YEARS:
        print(f"Starting to download data from the year: {year}")

        for b in BOAT_TYPES:
            print(f"Processing type: {b['name']}")
            url = f"{base_url}&group_id={b['id']}&year={year}"
            scrape_data(url, b['name'], "All Regions", cursor)

        for r in REGIONS:
            print(f"Region processing: {r['name']}")
            region_url_name = r['name'].replace(' ', '+')
            url = f"{base_url}&group={region_url_name}&group_id={r['id']}&year={year}"
            scrape_data(url, "All Boats", r['name'], cursor)

        conn.commit()

    conn.close()
    print("The database is ready.")


if __name__ == "__main__":
    run_scraper()