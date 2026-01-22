import json
import pytest
from django.test import Client
from .models import Venture
from .factories import VentureFactory


# Create your tests here.
def test_dashboard_view():
    client = Client()
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the dashboard!"}


@pytest.mark.django_db
def test_venture_list_empty():
    client = Client()
    response = client.get("/ventures")
    assert response.status_code == 200
    assert response.json() == {"ventures": []}


@pytest.mark.django_db
def test_venture_list_not_empty():
    VentureFactory.create_batch(3)
    client = Client()
    response = client.get("/ventures")
    assert response.status_code == 200
    response_data = response.json()
    assert "ventures" in response_data
    assert len(response_data["ventures"]) == 3


@pytest.mark.django_db
def test_save_venture():
    client = Client()
    venture_data = {
        "name": "Test Venture",
        "pod": "Test Pod",
        "stage": "Seed",
        "founder": "John Doe",
        "metrics": {"revenue": 1000},
        "status": "Active",
        "last_update": "2024-01-01",
    }
    response = client.post(
        "/add-venture", data=json.dumps(venture_data), content_type="application/json"
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["message"] == "Venture saved successfully!"


@pytest.mark.django_db
def test_generate_random_venture():
    assert Venture.objects.count() == 0
    client = Client()
    response = client.post("/random-ventures?count=5")
    assert response.status_code == 200
    assert response.json() == {"message": "5 random ventures generated successfully!"}

    assert Venture.objects.count() == 5
