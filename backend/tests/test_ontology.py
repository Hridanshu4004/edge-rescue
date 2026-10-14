from services.ontology import get_profile, capability_analysis, EMERGENCY_ONTOLOGY


def test_emergency_profiles_exist():
    for etype in ["medical", "trapped", "flood", "fire", "unknown"]:
        assert etype in EMERGENCY_ONTOLOGY
        profile = get_profile(etype)
        assert profile.required_role in ["medic", "rescue", "fire"]
        assert len(profile.skills) > 0
        assert len(profile.equipment) > 0
        assert profile.max_response_min > 0


def test_team_support_roles():
    medical_prof = get_profile("medical")
    assert "rescue" in medical_prof.team_support_roles

    fire_prof = get_profile("fire")
    assert "medic" in fire_prof.team_support_roles


def test_capability_analysis_exact_match():
    analysis = capability_analysis("medical", "medic")
    assert analysis["role_exact_match"] is True
    assert analysis["skill_coverage"] > 0.0
    assert len(analysis["skills_matched"]) > 0


def test_capability_analysis_incompatible():
    analysis = capability_analysis("medical", "fire")
    assert analysis["role_exact_match"] is False
    assert analysis["role_compatible"] is False
    assert len(analysis["skills_missing"]) > 0
