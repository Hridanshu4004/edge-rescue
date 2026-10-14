# EDGE RESCUE — Quick Command Reference

### 1. Backend Service (FastAPI)
```bash
uvicorn main:app --reload --port 8001 --host 0.0.0.0
```

### 2. Drone BLE Relay Daemon
```bash
python ble_relay.py --hub http://localhost:8001
```

### 3. Victim Emergency App (Flutter Android)
```bash
flutter run
```