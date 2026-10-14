import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


def test_api_title_and_version():
    assert app.title == "EDGE RESCUE API"
    assert app.version == "1.0.0"
    assert "Autonomous AI for a World Without Internet" in app.description


def test_openapi_schema_tags():
    openapi = app.openapi()
    assert openapi["info"]["title"] == "EDGE RESCUE API"
    paths = openapi["paths"]
    assert "/health" in paths
    assert "/sos/" in paths
    assert "/responders/" in paths
    assert "/ontology/hotspots" in paths
