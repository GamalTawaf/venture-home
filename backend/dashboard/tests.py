import json
import pytest
from django.test import Client
from .models import Venture
from .factories import VentureFactory


# Create your tests here.


def get_jwt_token(client, username="testuser", password="testpass123"):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password)
    response = client.post(
        "/auth/login",
        data=json.dumps({"username": username, "password": password}),
        content_type="application/json",
    )
    assert response.status_code == 200
    return response.json()["access"]

@pytest.mark.django_db
def test_venture_list_empty():
    client = Client()
    token = get_jwt_token(client)
    response = client.get("/ventures/", HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 200
    assert response.json()["results"] == []


@pytest.mark.django_db
def test_venture_list_not_empty():
    VentureFactory.create_batch(3)
    client = Client()
    token = get_jwt_token(client)
    response = client.get("/ventures/", HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 200
    response_data = response.json()
    assert "results" in response_data
    assert len(response_data["results"]) == 3


@pytest.mark.django_db
def test_save_venture():
    client = Client()
    token = get_jwt_token(client)
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
        "/ventures/", data=json.dumps(venture_data), content_type="application/json", HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    assert response.status_code == 201
    response_data = response.json()
    assert "id" in response_data
    assert response_data["name"] == "Test Venture"


@pytest.mark.django_db
def test_generate_random_venture():
    assert Venture.objects.count() == 0
    client = Client()
    token = get_jwt_token(client)
    response = client.post("/ventures/generate_random/", data=json.dumps({"count": 5}), content_type="application/json", HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 201
    assert response.json() == {"message": "5 random ventures generated successfully!"}
    assert Venture.objects.count() == 5
# Add login test for JWT auth
import base64
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_login_jwt():
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpass123")
    client = Client()
    response = client.post(
        "/auth/login",
        data=json.dumps({"username": "testuser", "password": "testpass123"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.json()
    assert "access" in data and "refresh" in data
