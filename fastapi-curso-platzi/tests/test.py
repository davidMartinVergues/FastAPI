import pytest
from httpx import AsyncClient
from models import Customer
from fastapi import status
from pprint import pprint

async def test_client_type(client):
    """Test that client fixture works"""
    assert isinstance(client, AsyncClient)

async def test_customer_creation(customer):
    """Test that customer fixture creates a customer"""
    assert isinstance(customer, Customer)
    assert customer.name == "Test Customer"
    assert customer.email == "test@example.com"

async def test_create_customer_endpoint(client):
    """Test creating a customer via API"""
    customer_data = {
        "name": "New Customer",
        "age": 30,
        "email": "new@example.com",  
        "description": "New customer description"
    }
    
    response = await client.post("/v1/customers", json=customer_data)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["name"] == customer_data["name"]
    assert data["email"] == customer_data["email"]

async def test_get_customer_endpoint(client, customer):
    """Test getting a specific customer via API"""
    # First, check if there's a GET endpoint for a specific customer
    response = await client.get(f"/v1/customers/{customer.id}")
    
    # If that endpoint doesn't exist, this test might need to be adjusted
    # based on what endpoints actually exist in your router
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    # The endpoint should work correctly now
    assert response.status_code == 200
    
    # Check the response data
    data = response.json()
    assert data["name"] == customer.name
    assert data["email"] == customer.email
    assert data["id"] == str(customer.id)