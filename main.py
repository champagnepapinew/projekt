import sqlite3
from datetime import datetime
from fastapi import FastAPI, Query
from typing import Optional
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
app = FastAPI(title="Yacht Valuation")

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/app")
def open_frontend():
    return FileResponse("frontend/index.html")

# --- DATABASE LOGIC ---

def get_smart_average_price(
        query_date: str,
        boat_type: Optional[str] = None,
        region: Optional[str] = None,
        cabins: Optional[int] = None,
        berths: Optional[int] = None,
        length: Optional[int] = None
):
    conn = sqlite3.connect('final_database.db')
    cursor = conn.cursor()

    # 1. Month extraction
    try:
        dt = datetime.strptime(query_date, "%Y-%m-%d")
        month_str = dt.strftime("-%m-")
    except ValueError:
        month_str = "-07-"

    # 2. Building SQL query
    query = """
            SELECT price_euro
            FROM sailboat_prices
            WHERE date LIKE ?
              AND price_euro > 0
            """
    params = [f"%{month_str}%"]

    # 3. DYNAMIC FILTERS

    #boat_type filter
    if boat_type and boat_type != "All Boats":
        query += " AND boat_type = ?"
        params.append(boat_type)

    #region filter
    if region and region != "All Regions":
        query += " AND region = ?"
        params.append(region)

    # 4. TECHNICAL FILTERS

    #cabins filter
    if cabins is not None:
        query += " AND cabins = ?"
        params.append(str(cabins))

    #berths filter
    if berths is not None:
        query += " AND berths = ?"
        params.append(berths)

    #length filter
    if length is not None:
        query += " AND length = ?"
        params.append(length)

    print(f"DEBUG SQL: {query} | Params: {params}")

    cursor.execute(query, params)
    results = cursor.fetchall()

    # 5. RETURNING THE AVERAGE
    if results:
        prices = [r[0] for r in results]
        conn.close()
        return int(sum(prices) / len(prices))

    # 6. PLAN B
    # If we searched for specific cabins/lengths and didn't find anything
    # we loosen up our criteria and look for a general price for that boat type (and region, if specified).

        # 6. PLAN B (fallback: loosen criteria)
    print("No accurate results. Activating Plan B...")

    fallback_query = """
        SELECT price_euro
        FROM sailboat_prices
        WHERE date LIKE ?
          AND price_euro > 0
    """
    fallback_params = [f"%{month_str}%"]

    if boat_type and boat_type != "All Boats":
        fallback_query += " AND boat_type = ?"
        fallback_params.append(boat_type)

    if region and region != "All Regions":
        fallback_query += " AND region = ?"
        fallback_params.append(region)

    print(f"DEBUG FALLBACK SQL: {fallback_query} | Params: {fallback_params}")

    cursor.execute(fallback_query, fallback_params)
    results = cursor.fetchall()
    conn.close()

    if results:
        prices = [r[0] for r in results]
        return int(sum(prices) / len(prices))
    else:
        return None


# --- API ---

@app.get("/")
def read_root():
    return {"status": "Online", "msg": "Use /api/suggest-price or api/form-options"}


@app.get("/api/form-options")
def get_form_options():
    """
    Returns all available options to dropdown lists.
    The frontend can retrieve this once and build the entire form.
    """
    conn = sqlite3.connect('final_database.db')
    cursor = conn.cursor()

    options = {}

    # 1. boat_type
    cursor.execute("SELECT DISTINCT boat_type FROM sailboat_prices ORDER BY boat_type ASC")
    options["boat_types"] = [r[0] for r in cursor.fetchall() if r[0]]

    # 2. regions
    cursor.execute("SELECT DISTINCT region FROM sailboat_prices ORDER BY region ASC")
    region_results = [r[0] for r in cursor.fetchall() if r[0] is not None]
    options["regions"] = ["All Regions"] + region_results

    # 3. berths
    cursor.execute("SELECT DISTINCT berths FROM sailboat_prices ORDER BY berths ASC")
    options["berths"] = [r[0] for r in cursor.fetchall() if r[0] is not None]

    # 4. cabins
    cursor.execute("SELECT DISTINCT cabins FROM sailboat_prices ORDER BY cabins ASC")
    options["cabins"] = [r[0] for r in cursor.fetchall() if r[0]]

    # 5. length
    cursor.execute("SELECT DISTINCT length FROM sailboat_prices ORDER BY length ASC")
    options["lengths"] = [r[0] for r in cursor.fetchall() if r[0] is not None]

    conn.close()
    return options

# -------------------------------

@app.get("/api/suggest-price")
def suggest_price(
        date: str,
        boat_type: Optional[str] = Query(None),
        region: Optional[str] = Query(None),
        cabins: Optional[int] = Query(None),
        berths: Optional[int] = Query(None),
        length: Optional[int] = Query(None)
):

    """
    Calculates the suggested charter price based on historical data statistics.
    """

    price= get_smart_average_price(date, boat_type, region, cabins, berths, length)

    return {
        "suggested_price_euro": price,
        "input_data": {
            "date": date,
            "region": region if region else "All Regions",
            "type": boat_type if region else "All Boats",
            "details": {"cabins": cabins, "berths": berths, "length": length}
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)