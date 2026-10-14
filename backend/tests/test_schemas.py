import pytest
from schemas import SOSCreate, ResponderCreate, LocationUpdate
from db.models import Severity, EmergencyType, ResponderRole


def test_sos_create_extra_fields_ignored():
    # BLE GATT packets or future clients sending extra fields must not fail validation
    payload = {
        "victim_code": "V-9999",
        "lat": 9.9312,
        "lng": 76.2673,
        "severity": "critical",
        "emergency_type": "fire",
        "message": "Trapped on roof",
        "extra_sensor_data": {"rssi": -65, "firmware": "1.2"},
        "unknown_flag": True,
    }
    sos = SOSCreate(**payload)
    assert sos.victim_code == "V-9999"
    assert sos.severity == Severity.critical
    assert sos.emergency_type == EmergencyType.fire


def test_responder_create():
    rc = ResponderCreate(
        code="R-999",
        name="Test Responder",
        role=ResponderRole.medic,
        sector=14,
        lat=9.93,
        lng=76.26,
    )
    assert rc.code == "R-999"
    assert rc.role == ResponderRole.medic


def test_location_update():
    loc = LocationUpdate(lat=9.93, lng=76.26, battery=88, heart_rate=72)
    assert loc.battery == 88
    assert loc.heart_rate == 72
