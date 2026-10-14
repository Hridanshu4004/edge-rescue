# EDGE RESCUE — Victim Emergency Mobile App

> **On-Device Multimodal AI & BLE GATT Relay for Zero-Connectivity Disasters**

The EDGE RESCUE Victim App is an offline-first Android application built with **Flutter** and **Kotlin**, powered by **Gemma 4 E2B via Google AI Edge LiteRT**.

When disaster strikes and cell towers fail, the app allows victims to capture voice notes, attach photos, and lock GPS coordinates. Gemma 4 E2B runs entirely on-device, translating regional spoken dialects into structured English triage packets and advertising them to aerial search drones over Bluetooth Low Energy (BLE) GATT without requiring an internet connection.

---

## Key Features

- **Offline Multimodal Triage**: Evaluates voice recordings (Telugu, Hindi, Malayalam, English), photographs (flood levels, collapse, fire), and text directly on device.
- **On-Device Structured Output**: Outputs standardized severity (`critical`, `urgent`, `low`), emergency type, people count, and plain English responder summary.
- **BLE GATT Server Mode**: Turns the phone into a Bluetooth GATT server (Service UUID `5a480001-...`), allowing passing drones or mesh nodes to connect, negotiate MTU 512, and read the triage packet.
- **Relay Acknowledgment**: Search drones write a confirmation byte back to the phone's characteristic, notifying the victim that rescue teams are dispatched.

---

## Build & Installation

### Option 1 — Build from Source (Flutter)
```bash
flutter pub get
flutter build apk --release
adb install build/app/outputs/flutter-apk/app-release.apk
```

### Option 2 — Pushing On-Device Model Weights
The on-device AI uses the Gemma 4 E2B LiteRT weights (`.litertlm` format, ~2.5 GB):
```bash
# 1. Launch the app once to initialize device directories
# 2. Push model weights via ADB:
adb push gemma-4-e2b-it.litertlm /sdcard/Android/data/com.zerohour.zerohour_victim/files/gemma.litertlm
```
On first launch, the app verifies internal storage and displays **"Gemma 4 E2B Ready"**. If weights are not present, the app seamlessly runs using the built-in compact packet relay.

---

## Architecture Flow

```
[Victim Input: Audio/Photo/GPS]
           │
           ▼
[Gemma 4 E2B (LiteRT on-device)]
           │
           ▼
[Structured Triage JSON Packet]
      ┌────┴────────────────────────┐
      ▼                             ▼
[Internet Available]         [No Internet (Disaster)]
Direct HTTP POST to Hub      BLE GATT Server Advertising
                             Search Drone connects & reads (MTU 512)
                             Drone relays to Hub & writes ACK to phone
```

