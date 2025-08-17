import sys, pathlib
current_dir = pathlib.Path(__file__).resolve().parent
root_dir = str(current_dir.parent)
sys.path.append(root_dir)

import pytest
from fastapi.testclient import TestClient

@pytest.fixture(scope='session')
def dpe_api_client():
    # pour faire ceci il faut definir dans les secrets du repos git les env var 
    # car l'app a besoin de redis pour demarrer par exemple (limiter)
    # return TestClient(app, base_url='http://testserver', raise_server_exceptions=True, backend='asyncio')
    # from api_fastapi.main import app
    return 