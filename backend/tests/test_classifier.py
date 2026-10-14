from services.classifier import fallback_triage, infer_emergency_type, infer_severity
from db.models import EmergencyType, Severity


def test_classify_emergency_type_keywords():
    assert infer_emergency_type("The river broke its banks and flood water is rising") == EmergencyType.flood
    assert infer_emergency_type("Building is burning with thick smoke and flames") == EmergencyType.fire
    assert infer_emergency_type("A wall collapsed and people are trapped under rubble") == EmergencyType.trapped
    assert infer_emergency_type("Severe chest pain, heart attack and bleeding") == EmergencyType.medical
    assert infer_emergency_type("Random hello test message") == EmergencyType.unknown


def test_classify_severity_levels():
    sev, reason, conf = infer_severity("Victim is unconscious and not breathing", EmergencyType.medical, False, False)
    assert sev == Severity.critical
    assert conf >= 0.85

    sev, reason, conf = infer_severity("Water is rising and we are stranded with elderly", EmergencyType.flood, False, False)
    assert sev == Severity.urgent

    sev, reason, conf = infer_severity("We are safe for now but need supplies and water", EmergencyType.unknown, False, False)
    assert sev == Severity.low


def test_fallback_triage_multilingual_handling():
    # Telugu flood sample
    telugu_text = "వరద నీరు ఇంట్లోకి వచ్చేసింది, సహాయం కావాలి."
    triage = fallback_triage(telugu_text, has_audio=False, has_image=False)
    assert triage["ai_available"] is False
    assert triage["severity"] in ["critical", "urgent", "low"]
    assert "emergency_type" in triage
    assert "victim_statement" in triage


def test_fallback_triage_structured_fields():
    msg = "People needing help: 3\nNeeds: Cannot move\nSituation: Wall collapsed on leg"
    result = fallback_triage(msg, has_audio=True, has_image=True)
    assert result["people_count"] == 3
    assert result["emergency_type"] == "trapped"
    assert result["severity"] in ["critical", "urgent"]
