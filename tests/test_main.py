import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport
from main import app

# Create a test client using FastAPI's TestClient
client = TestClient(app)

# Sample valid and invalid payloads
valid_payload = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "message": "Hello, this is a test email."
}

invalid_payload_missing_fields = {
    "name": "John Doe",
    "message": "Hello, this is a test email."
}

invalid_payload_invalid_email = {
    "name": "John Doe",
    "email": "invalid-email",
    "message": "Hello, this is a test email."
}


@pytest.mark.asyncio
async def test_send_email_valid():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with patch("main.send_email") as mock_send_email:
            mock_send_email.return_value = None  # Mocking the send_email function
            response = await ac.post("/send-email/", json=valid_payload)
            assert response.status_code == 200
            assert response.json() == {
                "status": "success", "message": "Email sent successfully"}
            mock_send_email.assert_called_once()


@pytest.mark.asyncio
async def test_send_email_invalid_missing_fields():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/send-email/", json=invalid_payload_missing_fields)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_email_invalid_email_format():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/send-email/", json=invalid_payload_invalid_email)
        assert response.status_code == 422
