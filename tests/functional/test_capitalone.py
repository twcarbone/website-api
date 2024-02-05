from api.models.capitalone import TransactionType


def test_transactions(_client):
    response = _client.get("/api/capitalone/transactions")
    assert response.status_code == 200
    assert response.json == [
        {
            "amount": "58.92",
            "card_name": "Foo",
            "card_number": "1234",
            "category": "Dining",
            "date": "Mon, 18 May 2020 00:00:00 GMT",
            "id": 1,
            "merchant": "Lindys",
            "post_date": "Mon, 18 May 2020 00:00:00 GMT",
            "transaction_type": "Debit",
        },
        {
            "amount": "101.47",
            "card_name": "Bar",
            "card_number": "5678",
            "category": "Entertainment",
            "date": "Fri, 12 Feb 2021 00:00:00 GMT",
            "id": 2,
            "merchant": "AMC",
            "post_date": "Sat, 13 Feb 2021 00:00:00 GMT",
            "transaction_type": "Debit",
        },
        {
            "amount": "1356.83",
            "card_name": "Bar",
            "card_number": "5678",
            "category": "Payment",
            "date": "Wed, 01 Jan 1997 00:00:00 GMT",
            "id": 3,
            "merchant": "Bank",
            "post_date": "Thu, 02 Jan 1997 00:00:00 GMT",
            "transaction_type": "Credit",
        },
    ]


def test_transaction(_client):
    response = _client.get("/api/capitalone/transactions/1")
    assert response.status_code == 200
    assert response.json == {
        "amount": "58.92",
        "card_name": "Foo",
        "card_number": "1234",
        "category": "Dining",
        "date": "Mon, 18 May 2020 00:00:00 GMT",
        "id": 1,
        "merchant": "Lindys",
        "post_date": "Mon, 18 May 2020 00:00:00 GMT",
        "transaction_type": "Debit",
    }

    response = _client.get("/api/capitalone/transactions/0")
    assert response.status_code == 401
    assert response.json == {"message": "Invalid 'id'"}
