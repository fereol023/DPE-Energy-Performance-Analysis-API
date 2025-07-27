import pytest
from fastapi.testclient import TestClient
from api_fastapi.main import app

@pytest.fixture(scope='session')
def dpe_api_client():
    return TestClient(app, base_url='http://testserver', raise_server_exceptions=True, backend='asyncio')