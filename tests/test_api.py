from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#request/response test 
def test_root_endpoint_online():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data

#backend tests 
def test_form_options_returns_keys():
    r = client.get("/api/form-options")
    assert r.status_code == 200
    data = r.json()
    assert "boat_types" in data
    assert "regions" in data
    assert "cabins" in data
    assert "berths" in data
    assert "lengths" in data

def test_price_date_only():
    r = client.get("/api/suggest-price?date=2025-07-15")
    assert r.status_code == 200
    assert "suggested_price_euro" in r.json()

def test_price_region_split():
    r = client.get("/api/suggest-price?date=2025-07-15&region=Split")
    assert r.status_code == 200
    assert "suggested_price_euro" in r.json()

def test_price_boattype_sailingyachts():
    r = client.get("/api/suggest-price?date=2025-07-15&boat_type=Sailing%20yachts")
    assert r.status_code == 200
    assert "suggested_price_euro" in r.json()

def test_price_full_filters_exact_average():
    r = client.get(
        "/api/suggest-price?date=2025-07-15&region=Split&boat_type=Sailing%20yachts&cabins=3&berths=6&length=12"
    )
    assert r.status_code == 200
    assert r.json()["suggested_price_euro"] == 11000

def test_price_returns_integer():
    r = client.get("/api/suggest-price?date=2025-07-15")
    assert r.status_code == 200
    price = r.json()["suggested_price_euro"]
    assert isinstance(price, int)
    assert price > 0

