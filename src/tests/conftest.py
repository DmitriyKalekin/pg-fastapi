import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app as application
from asyncio import get_event_loop, get_running_loop




@pytest.fixture(scope="function")
def api_app():
    yield application


@pytest_asyncio.fixture(scope="function")
async def testclient(api_app):
    headers = {"Connection": "close", "X-TESTING": "1"}
    async with AsyncClient(base_url="http://test", headers=headers, app=api_app) as client:
        yield client
