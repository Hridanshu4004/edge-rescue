import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from main import app
from db.database import get_db, SessionLocal, engine, Base
from db.models import Responder, ResponderRole, ResponderStatus, SOSPacket, SOSStatus
from sqlalchemy import select


@pytest.mark.asyncio
async def test_create_sos_and_auto_assign(test_db):
    transport = ASGITransport(app=app)

    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Post a new emergency SOS
        sos_payload = {
            "victim_code": f"V-{uuid.uuid4().hex[:4].upper()}",
            "lat": 9.9315,
            "lng": 76.2675,
            "message": "People needing help: 2\nSituation: Trapped on 2nd floor, flood water rising fast",
            "has_audio": False,
            "has_image": False,
            "hops": 1,
        }
        resp = await client.post("/sos/", json=sos_payload)
        assert resp.status_code == 201
        data = resp.json()

        # Verify SOS fields
        assert "sos" in data
        assert data["sos"]["victim_code"] == sos_payload["victim_code"]
        assert data["sos"]["emergency_type"] in ["flood", "trapped"]

        # Verify Triage details
        assert "triage" in data
        assert data["triage"]["severity"] in ["critical", "urgent"]

        # Verify Assignment was automatically generated even without Gemini key (offline resilience)
        assert "assignment" in data
        assignment = data["assignment"]
        assert assignment is not None
        assert assignment["responder_code"] in ["R-114", "R-205"]
        assert assignment["eta_minutes"] is not None

        # 2. Query queue
        q_resp = await client.get("/sos/queue")
        assert q_resp.status_code == 200
        queue = q_resp.json()
        assert len(queue) >= 1

        # 3. List Responders
        r_resp = await client.get("/responders/")
        assert r_resp.status_code == 200
        responders = r_resp.json()
        assert len(responders) >= 2

        # 4. Resolve SOS
        sos_id = data["sos"]["id"]
        resolve_resp = await client.patch(f"/sos/{sos_id}/resolve")
        assert resolve_resp.status_code == 200
        assert resolve_resp.json()["status"] == "resolved"

    app.dependency_overrides.clear()
