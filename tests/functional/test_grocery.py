import pytest


def test_products(_client):
    response = _client.get("/api/grocery/products")
    assert response.status_code == 200
    assert response.json == [
        {
            "brand": "Fresh",
            "description": "Put peanut butter on me!",
            "id": 1,
            "long_name": "Yellow Banana, 1 ct, 4 oz",
            "short_name": "BANANA BAG #3",
            "sku": "00000000040112",
        },
        {
            "brand": "Bowl & Basket",
            "description": "Make a pie with me!",
            "id": 2,
            "long_name": "Bowl & Basket Blueberries, 48 oz",
            "short_name": "SRBB FRZ BLUEBERRI",
            "sku": "00041190410736",
        },
        {
            "brand": None,
            "description": None,
            "id": 3,
            "long_name": None,
            "short_name": "Chock full o'Nuts Medium Original Ground Coffee",
            "sku": None,
        },
    ]


def test_product(_client):
    response = _client.get("/api/grocery/product/1")
    assert response.status_code == 200
    assert response.json == {
        "brand": "Fresh",
        "description": "Put peanut butter on me!",
        "id": 1,
        "long_name": "Yellow Banana, 1 ct, 4 oz",
        "short_name": "BANANA BAG #3",
        "sku": "00000000040112",
    }

    response = _client.get("/api/grocery/product/9999")
    assert response.status_code == 401
    assert response.json.get("message") == "Invalid 'id'"


def test_orders(_client):
    response = _client.get("/api/grocery/orders")
    assert response.status_code == 200
    assert response.json == [
        {"date": "Mon, 12 Jun 2023 00:00:00 GMT", "id": 2, "order_total": "13.09"},
        {"date": "Sun, 30 Apr 2023 00:00:00 GMT", "id": 1, "order_total": "11.70"},
    ]


def test_order(_client):
    response = _client.get("/api/grocery/order/1")
    assert response.status_code == 200
    assert response.json == {"date": "Sun, 30 Apr 2023 00:00:00 GMT", "id": 1, "order_total": "11.70"}

    response = _client.get("/api/grocery/order/9999")
    assert response.status_code == 401
    assert response.json.get("message") == "Invalid 'id'"


def test_transactions(_client):
    response = _client.get("/api/grocery/transactions")
    assert response.status_code == 200
    assert response.json == [
        {
            "date": "Mon, 12 Jun 2023 00:00:00 GMT",
            "discount": "2.00",
            "final": "11.99",
            "id": 4,
            "long_name": None,
            "qty": "1.00",
            "rate": "11.99",
            "rate_type": "PER_QTY",
            "short_name": "Chock full o'Nuts Medium Original Ground Coffee",
            "sku": None,
        },
        {
            "date": "Sun, 30 Apr 2023 00:00:00 GMT",
            "discount": None,
            "final": "9.99",
            "id": 2,
            "long_name": "Bowl & Basket Blueberries, 48 oz",
            "qty": "1.00",
            "rate": "9.99",
            "rate_type": "PER_QTY",
            "short_name": "SRBB FRZ BLUEBERRI",
            "sku": "00041190410736",
        },
        {
            "date": "Sun, 30 Apr 2023 00:00:00 GMT",
            "discount": None,
            "final": "1.71",
            "id": 1,
            "long_name": "Yellow Banana, 1 ct, 4 oz",
            "qty": "2.48",
            "rate": "0.69",
            "rate_type": "PER_LB",
            "short_name": "BANANA BAG #3",
            "sku": "00000000040112",
        },
        {
            "date": "Mon, 12 Jun 2023 00:00:00 GMT",
            "discount": None,
            "final": "1.10",
            "id": 3,
            "long_name": "Yellow Banana, 1 ct, 4 oz",
            "qty": "1.59",
            "rate": "0.69",
            "rate_type": "PER_LB",
            "short_name": "BANANA BAG #3",
            "sku": "00000000040112",
        },
    ]


def test_transaction(_client):
    response = _client.get("/api/grocery/transaction/1")
    assert response.status_code == 200
    assert response.json == {
        "date": "Sun, 30 Apr 2023 00:00:00 GMT",
        "discount": None,
        "final": "1.71",
        "id": 1,
        "long_name": "Yellow Banana, 1 ct, 4 oz",
        "qty": "2.48",
        "rate": "0.69",
        "rate_type": "PER_LB",
        "short_name": "BANANA BAG #3",
        "sku": "00000000040112",
    }

    response = _client.get("/api/grocery/transaction/9999")
    assert response.status_code == 401
    assert response.json.get("message") == "Invalid 'id'"
