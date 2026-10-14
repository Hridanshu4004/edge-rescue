from datetime import datetime, timezone
from services.scorer import (
    _role_score,
    _distance_score,
    _battery_score,
    _sector_score,
    rank_candidates,
    SEARCH_RADIUS_M,
)


def test_role_score():
    assert _role_score("medical", "medic") == 1.0
    assert _role_score("fire", "fire") == 1.0
    assert _role_score("trapped", "rescue") == 1.0
    # Compatible roles
    assert _role_score("trapped", "fire") == 0.55
    # Incompatible roles
    assert _role_score("medical", "fire") == 0.10


def test_distance_score():
    assert _distance_score(0) == 1.0
    assert _distance_score(SEARCH_RADIUS_M) == 0.0
    assert _distance_score(SEARCH_RADIUS_M / 2) == 0.5
    assert _distance_score(SEARCH_RADIUS_M * 2) == 0.0


def test_battery_score():
    assert _battery_score(100) == 1.0
    assert _battery_score(50) == 1.0
    assert _battery_score(49) == 0.5
    assert _battery_score(20) == 0.5
    assert _battery_score(19) == 0.1


def test_sector_score():
    assert _sector_score(14, 14) == 1.0
    assert _sector_score(14, 15) == 0.6
    assert _sector_score(None, 14) == 0.5


def test_rank_candidates():
    candidates = [
        {
            "code": "R-114",
            "name": "Medic One",
            "role": "medic",
            "sector": 14,
            "status": "available",
            "battery": 100,
            "distance_m": 500,
            "eta_minutes": 3,
        },
        {
            "code": "R-205",
            "name": "Rescue One",
            "role": "rescue",
            "sector": 14,
            "status": "available",
            "battery": 90,
            "distance_m": 600,
            "eta_minutes": 4,
        },
        {
            "code": "R-312",
            "name": "Fire One",
            "role": "fire",
            "sector": 15,
            "status": "available",
            "battery": 15,
            "distance_m": 4500,
            "eta_minutes": 25,
        },
    ]

    ranked = rank_candidates(
        emergency_type="medical",
        severity="critical",
        sos_sector=14,
        created_at=datetime.now(timezone.utc),
        candidates=candidates,
    )

    assert len(ranked) == 3
    # R-114 is a medic located 500m away in sector 14 with 100% battery - must be #1
    assert ranked[0]["code"] == "R-114"
    assert ranked[0]["composite_score"] > ranked[1]["composite_score"]
    assert "ontology" in ranked[0]
    assert "score_breakdown" in ranked[0]
