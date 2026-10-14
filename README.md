# EDGE RESCUE

> **Autonomous AI for a World Without Internet**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev)
[![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL_16-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Redis](https://img.shields.io/badge/Redis_7-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![LiteRT](https://img.shields.io/badge/Google_AI_Edge-LiteRT-orange?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/edge/litert)
[![BLE](https://img.shields.io/badge/BLE-GATT_Relay_512_MTU-8A2BE2?style=for-the-badge)](https://bluetooth.com)

---

## Overview

**EDGE RESCUE** is a production-grade, offline-first disaster response coordination system engineered for catastrophic scenarios where physical telecommunications infrastructure has collapsed. 

By pairing **on-device multimodal AI (Gemma 4 E2B via Google AI Edge LiteRT)** with an **aerial BLE GATT drone relay pipeline** and an **autonomous multi-factor assignment hub (Gemma 4 26B with 100% offline rule fallback)**, EDGE RESCUE bridges the survival gap between trapped victims and field responders when the internet disappears.

---

## Problem

In major natural disasters — such as the 2018 Kerala floods, Cyclone Fani, and severe earthquakes:
1. **Cell towers drown and power grids fail first**: Communications networks collapse within minutes, leaving stranded civilians without cellular service, SMS, or internet access.
2. **Language and literacy barriers paralyze response**: Panicked victims speak regional village dialects (Telugu, Malayalam, Hindi). Incoming national rescue forces often do not share the local language, leading to lost time, misdiagnosis, and communication breakdowns.
3. **No triage and uncoordinated dispatch**: Civilian WhatsApp groups and raw social media screenshots become makeshift dispatch channels. Every distress call is treated identically; responders duplicate efforts while critical life-threatening cases go unnoticed until it is too late.

---

## Solution

EDGE RESCUE deploys a 3-tier resilient mesh architecture:

1. **On-Device Edge Multimodal Triage**: The victim's phone runs Gemma 4 E2B directly on CPU/NPU via Google AI Edge LiteRT. It accepts native voice notes, photographs of rising floodwaters or structural collapse, and typed notes. Without contacting any server, it generates a structured, English-standardized triage packet with classification, severity, and victim summary.
2. **Physical BLE GATT Drone Relay**: When disconnected, the victim's phone becomes a Bluetooth GATT server advertising Service UUID `5a480001-...`. Aerial search drones flying overhead autonomously discover the device, negotiate MTU 512, read the complete 490-byte triage JSON packet, and physically carry the data until they reach a base station uplink. Drones write an ACK byte back to the victim's phone, confirming that rescue is underway.
3. **Autonomous Coordination Hub**: The incident hub ingests relayed packets, eliminates duplicates through a 30-meter spatial-temporal filter, algorithmically ranks available responders (by role match, capability coverage, distance, battery, and sector), and applies Gemma 4 26B context judgment to assign units and dispatch complementary multi-role teams (e.g. Medic + Rescue).

---

## Why Offline AI?

| Requirement | Traditional Cloud LLMs (GPT-4 / Claude) | Generic On-Device GGUF / Whisper | EDGE RESCUE (Gemma 4 E2B via LiteRT) |
|---|---|---|---|
| **Zero Internet Dependency** | ❌ Fails (Requires Cloud API) | ✅ Local | ✅ **Fully On-Device** |
| **Multimodal in One Model** | ❌ Cloud-only | ❌ Requires 2+ models (4GB+ RAM) | ✅ **Text + Vision + Audio in 2B weights** |
| **Commodity Android Speed** | ❌ Inaccessible | ⚠️ 30–60s on mobile CPU | ✅ **< 10s inference on mid-range phone** |
| **Multilingual Native Audio** | ❌ Inaccessible offline | ⚠️ Poor low-resource language accuracy | ✅ **Natively understands regional dialects** |
| **Zero API Operating Cost** | ❌ High per-call cost | ✅ Free | ✅ **100% Free Apache 2.0 open weights** |

LiteRT is Google AI Edge's optimized runtime delivering 2–3× faster execution than generic runtimes on mobile hardware. Gemma 4 E2B's 2B parameter scale fits into standard mobile RAM while delivering structured JSON output (`severity`, `emergency_type`, `people_count`, `victim_statement`).

---

## Target Users

- **Disaster Victims**: Trapped individuals or families with submerged towers and no internet access.
- **Field Responders**: Search and rescue boat crews, paramedics, and firefighters navigating chaotic disaster zones with an offline-capable field tactical interface.
- **Incident Commanders & Supervisors**: Emergency Operations Centers (EOC) managing real-time geospatial triage, dynamic queue management, and team allocation.
- **Aerial Reconnaissance Operators**: Drone operators running autonomous search-and-relay flight grids over isolated sectors.

---

## Key Features

- **Multilingual Spoken Audio Understanding**: Victims speak naturally in their native language; the on-device AI renders a clean, responder-ready English situation summary (`victim_statement`).
- **Visual Damage & Hazard Analysis**: Identifies flood waterlines, structural collapse, smoke/fire, and entrapment from photos taken in the app.
- **Bidirectional BLE GATT Relay**: Rich JSON transmission up to 490 bytes over BLE GATT without device pairing, complete with physical confirmation ACK.
- **Multi-Factor Algorithmic Scoring**: Evaluates responders mathematically before AI review:
  $$\text{Score} = 0.35 \times \text{Role} + 0.25 \times \text{Capability} + 0.25 \times \text{Distance} + 0.10 \times \text{Battery} + 0.05 \times \text{Sector}$$
- **Time-Decay Urgency Multiplier**: Gradually elevates priority of unattended incidents to guarantee no critical case is starved.
- **Dual-Responder Team Dispatch**: Automatically pairs complementary responders (e.g., Rescue Boat + Paramedic) when incidents involve multiple victims or severe hazards.
- **Spatial-Temporal Deduplication**: Automatically clusters reports within a 30-meter radius over 12 hours, merging details rather than dispatching duplicate teams.
- **100% Offline Rule Fallback Guarantee**: If the cloud AI Studio key is unavailable or the hub loses external backhaul, the system seamlessly continues running on its deterministic rule classifier and algorithmic engine without dropping a single SOS.

---

## System Architecture

```mermaid
graph TD
    subgraph VictimPhone["Victim Phone (Edge Node)"]
        UI[Emergency UI\nVoice Note · Photo · GPS]
        E2B[Gemma 4 E2B\nLiteRT On-Device]
        GATT[BLE GATT Server\nUUID: 5a480001-...]
        UI -->|multimodal inputs| E2B
        E2B -->|structured triage JSON| UI
        UI -->|offline path| GATT
        UI -->|online path| API
    end

    subgraph DroneRelay["Aerial Drone / Mesh Node"]
        SCAN[BLE Scanner]
        CLIENT[GATT Client\nMTU 512 Handshake]
        ACK[Write ACK Characteristic]
        SCAN --> CLIENT
        CLIENT --> ACK
    end

    subgraph IncidentHub["Incident Command Hub (FastAPI)"]
        API[POST /sos/]
        DEDUP[Spatial Deduplicator\n30m Cluster Filter]
        SCORER[Multi-Factor Scorer\nRole · Skills · Dist · Battery]
        HUB_AI[Gemma 4 26B Hub Engine\nGoogle AI Studio / Offline Fallback]
        DB[(PostgreSQL 16)]
        CACHE[(Redis 7 Pub/Sub)]
        
        API --> DEDUP --> SCORER --> HUB_AI --> DB
        HUB_AI --> CACHE
    end

    subgraph Dashboards["Real-Time Operations"]
        RESP[Responder Field PWA\nR-114 Tactical Ops]
        SUP[Supervisor Tactical Console\nLive Map · Queue · Teams]
        CACHE -->|WebSocket| RESP
        CACHE -->|WebSocket| SUP
    end

    GATT -.->|BLE Connect| SCAN
    CLIENT -.->|Uplink Relay| API
    ACK -.->|Relay Confirmed| GATT
```

---

## How It Works

### End-to-End Sequence Trace

```mermaid
sequenceDiagram
    autonumber
    actor V as Victim
    participant P as Phone (Gemma 4 E2B)
    participant D as Relay Drone (Bleak)
    participant H as Hub Backend (FastAPI)
    participant R as Field Responder (PWA)

    V->>P: Record Telugu voice note + photo of flood
    P->>P: Gemma 4 E2B classifies criticality & extracts English statement (Offline)
    P->>P: Starts BLE GATT Server (advertising 5a480001-...)
    Note over P,D: Drone flies overhead across search grid
    D->>P: BleakClient connects & negotiates MTU 512
    P-->>D: Transmits 490-byte JSON triage packet
    D->>H: POST /sos/ (upon reaching backhaul uplink)
    H->>H: Spatial deduplication (30m cluster check)
    H->>H: Algorithmic ranking across available units
    H->>H: Hub AI confirms assignment / deploys dual team
    H-->>D: HTTP 201 Created {responder, eta_minutes, reason}
    D->>P: Writes ACK to SOS_ACK_CHAR
    P->>V: Screen updates: "Relay Confirmed — Rescue En Route"
    H->>R: WebSocket push: Instant tactical mission assignment
```

---

## AI / Agent Architecture

EDGE RESCUE implements a partitioned edge-to-hub AI architecture:

### 1. Edge Layer: Gemma 4 E2B (LiteRT)
- **Deployment**: Android CPU / NPU runtime via `com.google.ai.edge.litertlm`.
- **Role**: Fast multimodal perception. Receives high-entropy unstructured signals (audio waveform, camera frames, unstructured text) and transforms them into low-bandwidth structured JSON:
  ```json
  {
    "emergency_type": "flood",
    "severity": "critical",
    "people_count": 2,
    "quick_needs": "evacuation and medical",
    "victim_statement": "Trapped on roof, water entering 2nd floor",
    "image_analysis": "Water level reaching building window line"
  }
  ```

### 2. Hub Layer: Multi-Factor Scorer + Gemma 4 26B
- **Deployment**: FastAPI service orchestrated with Google AI Studio (`gemma-4-26b-a4b-it`) and PostgreSQL.
- **Role**: Tactical decision-making and assignment.
- **Workflow**:
  1. The deterministic algorithmic scorer evaluates all available units and computes normalized capability match, distance score, and battery safety.
  2. The candidate roster and triage reasoning are provided to Gemma 4 26B.
  3. The model reviews contextual nuances, evaluates multi-victim complexity, and either confirms or overrides the top pick with justification.
  4. If multi-specialty intervention is required (e.g. structural trapped + severe bleed), the engine triggers **dual-responder team dispatch** (Medic + Rescue).
- **Offline Fallback**: If external connectivity is lost at the hub, the system automatically runs the deterministic scorer and rule-based classifier (`ai_available: false`), ensuring 100% operational continuity.

---

## Technology Stack

| Layer | Component | Description |
|---|---|---|
| **On-Device AI** | Gemma 4 E2B | 2B parameter multimodal model via Google AI Edge LiteRT |
| **Mobile App** | Flutter & Kotlin | Android app with Background GATT Server & EventChannels |
| **Drone Relay** | Python 3.10+ & Bleak | Asynchronous BLE client, MTU 512 negotiator, and uplink client |
| **Backend API** | FastAPI & Uvicorn | Async ASGI backend with WebSockets, Pydantic v2 schemas |
| **Database** | PostgreSQL 16 | Relational persistence with UUID primary keys & SQLAlchemy 2 Async |
| **Real-Time Pub/Sub**| Redis 7 | Event broadcaster and 30-second TTL responder telemetry cache |
| **Hub AI** | Gemma 4 26B | Contextual assignment model via Google AI Studio API |
| **Web Frontend** | React 18 & Vite | Tactical responder PWA, command supervisor console, and web SOS simulator |
| **Mapping** | Leaflet | Live GPS tactical tracking, CartoDB Dark Matter tiles, responder polylines |
| **Styling** | Vanilla CSS & Tailwind | Ops-dark tactical theme with clear visual hierarchy |
| **Containerization**| Docker & Docker Compose | Multi-stage production container builds |

---

## Local Setup

### Prerequisites

- **Python 3.10+**
- **Node.js 20+**
- **Docker Desktop** (for PostgreSQL & Redis)
- **Flutter 3 SDK** (optional, only if compiling the Android APK)

### 1. Clone & Environment Configuration

```bash
# Clone the repository
git clone https://github.com/your-username/EdgeRescue.git
cd EdgeRescue

# Copy example environment configuration
cp .env.example .env
```

Edit `.env` to configure your settings:
```bash
DATABASE_URL=postgresql+psycopg://zerohour:zerohour@localhost:5432/zerohour
REDIS_URL=redis://localhost:6379
GEMINI_API_KEY=your_google_ai_studio_api_key_here  # Optional: runs offline fallback if empty
```

### 2. Infrastructure via Docker Compose

```bash
docker compose up -d postgres redis
```

### 3. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# or: .\.venv\Scripts\activate   # Windows

pip install -r requirements.txt
uvicorn main:app --reload --port 8001 --host 0.0.0.0
```

Verify backend health at: [http://localhost:8001/health](http://localhost:8001/health)

### 4. Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```

Open the dashboard in your browser: [http://localhost:5173](http://localhost:5173)

---

## Environment Variables

| Variable | Default Value | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+psycopg://zerohour:zerohour@localhost:5432/zerohour` | Async PostgreSQL connection string |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection URL for Pub/Sub & live telemetry |
| `GEMINI_API_KEY` | *(empty)* | Google AI Studio API key for Gemma 4 26B hub model |
| `GEMMA_MODEL` | `gemma-4-26b-a4b-it` | Hub model for contextual assignment |
| `GEMMA_TRIAGE_MODEL` | `gemma-4-e2b-it` | Hub model for fallback triage |
| `VITE_API_URL` | `http://localhost:8001` | Backend URL injected into the frontend |

---

## Running the Application

### Full Stack with Docker Compose

To launch the complete containerized stack in one command:
```bash
docker compose up --build
```
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: [http://localhost:8000](http://localhost:8000) (and [http://localhost:8001](http://localhost:8001))
- Interactive Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Drone BLE Relay Daemon

```bash
cd drone
pip install -r requirements.txt
python ble_relay.py --hub http://localhost:8001
```

### Victim Emergency Mobile App (Android)

```bash
cd victim_app
flutter pub get
flutter run
```

---

## Demo Flow

For evaluators and judges reviewing EDGE RESCUE, follow this 3-minute demonstration:

1. **Open the Landing Page**: Navigate to [http://localhost:5173](http://localhost:5173). Observe the unified **EDGE RESCUE** identity and the system resilience explainer.
2. **Launch the Victim SOS Simulator**: Click **Victim SOS Simulator**. 
   - Record a voice note or type an emergency message (e.g. *"Flood water rising rapidly, 2 people trapped on 2nd floor, one elderly with asthma"*).
   - Drop a map pin or click GPS.
   - Click **Send Rescue Request**. Watch the step-by-step on-device triage and transmission progress.
3. **Open Command Supervisor in Another Tab**:
   - Return to the portal and select **Command Supervisor**.
   - Notice the newly submitted SOS appear immediately on the **Live Tactical Map** with an active assignment line drawn directly to the best-fit responder.
   - View the **Multi-Factor Score Breakdown**, skill coverage analysis, and AI reasoning.
4. **Inspect the Field Tactical Unit**:
   - Open **Field Responder** (unit R-114).
   - View the dispatched mission in the prioritized Triage queue, check distance and turn-by-turn metrics, and click **Mission Complete** to resolve the incident.
5. **Reset State**: Click **Reset Demo** on the landing page to reset the database and run another simulation.

---

## Testing

EDGE RESCUE includes a comprehensive automated test suite covering unit logic, algorithmic scoring, NLP triage, geospatial calculations, and end-to-end API integration.

To run the test suite:
```bash
cd backend
source .venv/bin/activate      # Linux / macOS
# or: .\.venv\Scripts\activate   # Windows

pytest -v
```

### Test Coverage Highlights

- `tests/test_health_and_meta.py`: Validates `/health`, OpenAPI metadata, and app title.
- `tests/test_scorer.py`: Tests role matching, battery health penalties, distance scoring, and candidate sorting.
- `tests/test_classifier.py`: Tests rule-based NLP classification across flood, fire, trapped, and medical scenarios in regional dialects.
- `tests/test_ontology.py`: Validates emergency capability matrices and team support role rules.
- `tests/test_geo.py`: Validates Haversine distance computations and role-specific ETA estimations.
- `tests/test_schemas.py`: Validates forward compatibility with extended BLE GATT packets.
- `tests/test_offline_fallback.py`: Validates zero-crash deterministic offline fallback and automated dual-responder team dispatch.
- `tests/test_api_integration.py`: Tests end-to-end HTTP lifecycle from SOS creation to auto-assignment, queue query, and resolution.

---

## Limitations

- **Physical BLE Range**: Standard Bluetooth Low Energy operates over approximately 50–100 meters line-of-sight. Drones must execute structured grid search flight paths over disaster sectors to establish GATT connections.
- **Power Constraints in Prolonged Blackouts**: While on-device inference is optimized (< 10 seconds), phones in disaster zones must conserve power. The app supports sleep between scheduled advertisement bursts.
- **GATT MTU Negotiation**: While modern Android devices support MTU 512, older legacy Bluetooth 4.0 devices fall back to the compact 17-byte advertising packet mode.

---

## Future Improvements

1. **LoRa & Meshtastic Physical Layer**: Integrating 868/915 MHz LoRa transceivers to extend ground transmission range to 5–15 km without requiring aerial relays.
2. **Satellite Direct-to-Cell Backhaul**: Direct integration with 3GPP Non-Terrestrial Network (NTN) satellite relays for zero-infrastructure hub connectivity.
3. **Drone Swarm Flight Orchestration**: Autonomous multi-drone flight planning algorithm that dynamically prioritizes search grids based on population density and flood velocity maps.
4. **Audio Slicing & Acoustic Triage**: On-device detection of distress acoustics (crying, water rushing, heavy coughing, glass breaking) even before speech parsing.

---

## License

This project is licensed under the terms of the **MIT License**. See the [LICENSE](LICENSE) file for details.

### Acknowledgments

- **Google AI Edge Team** for LiteRT edge inference runtime and the Gemma open model family.
- **Bleak** library maintainers for asynchronous cross-platform Bluetooth Low Energy support.
- **Leaflet & CartoDB** for open-access dark tactical cartography.
