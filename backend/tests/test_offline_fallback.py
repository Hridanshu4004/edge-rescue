import pytest
from services.gemma import _fallback, triage_and_assign


def test_fallback_assignment_deterministic():
    ranked_candidates = [
        {
            "code": "R-114",
            "name": "Medic One",
            "role": "medic",
            "composite_score": 0.92,
            "distance_m": 450,
            "eta_minutes": 3,
            "ontology": {"skill_coverage": 0.85},
        },
        {
            "code": "R-205",
            "name": "Rescue One",
            "role": "rescue",
            "composite_score": 0.78,
            "distance_m": 1200,
            "eta_minutes": 7,
            "ontology": {"skill_coverage": 0.40},
        },
    ]

    sos = {
        "victim_code": "V-1234",
        "severity": "urgent",
        "emergency_type": "medical",
    }

    result = _fallback(ranked_candidates, sos)
    assert result["assign"] == "R-114"
    assert result["ai_available"] is False
    assert result["eta_minutes"] == 3
    assert result["confidence"] == 0.92


def test_fallback_team_dispatch_on_critical_low_coverage():
    # If severity is critical and primary responder has low skill coverage, team dispatch is recommended
    ranked_candidates = [
        {
            "code": "R-205",
            "name": "Rescue One",
            "role": "rescue",
            "composite_score": 0.80,
            "distance_m": 300,
            "eta_minutes": 2,
            "ontology": {"skill_coverage": 0.50},  # < 0.70
        },
        {
            "code": "R-114",
            "name": "Medic One",
            "role": "medic",
            "composite_score": 0.75,
            "distance_m": 600,
            "eta_minutes": 4,
            "ontology": {"skill_coverage": 0.60},
        },
    ]

    sos = {
        "victim_code": "V-5555",
        "severity": "critical",
        "emergency_type": "trapped",  # trapped has team_support_roles=("medic",)
    }

    result = _fallback(ranked_candidates, sos)
    assert result["assign"] == "R-205"
    assert "team_codes" in result
    assert "R-114" in result["team_codes"]
    assert "team_reason" in result


@pytest.mark.asyncio
async def test_triage_and_assign_without_api_key():
    # When GEMINI_API_KEY is empty string, triage_and_assign must seamlessly invoke _fallback without throwing
    candidates = [
        {
            "code": "R-114",
            "name": "Medic",
            "role": "medic",
            "composite_score": 0.88,
            "distance_m": 500,
            "eta_minutes": 3,
            "ontology": {"skill_coverage": 1.0},
        }
    ]
    sos = {"victim_code": "V-100", "severity": "low", "emergency_type": "medical"}
    res = await triage_and_assign(sos, candidates)
    assert res["assign"] == "R-114"
    assert res["ai_available"] is False
