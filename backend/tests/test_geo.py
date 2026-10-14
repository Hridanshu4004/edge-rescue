import math
from services.geo import GeoPoint, haversine_m, eta_minutes


def test_haversine_same_point():
    p1 = GeoPoint(lat=9.9312, lng=76.2673)
    p2 = GeoPoint(lat=9.9312, lng=76.2673)
    assert haversine_m(p1, p2) == 0.0


def test_haversine_known_distance():
    # Kochi to Ernakulam north (~1.5 km)
    p1 = GeoPoint(lat=9.9312, lng=76.2673)
    p2 = GeoPoint(lat=9.9420, lng=76.2750)
    dist = haversine_m(p1, p2)
    assert 1200 < dist < 1800


def test_eta_minutes():
    # 3 km for medic (speed 30 km/h -> 6 min + 1 min prep = 7 min)
    eta = eta_minutes(3000, "medic")
    assert eta >= 5
    # 0 distance should still take minimum 1 min prep
    assert eta_minutes(0, "medic") == 1
