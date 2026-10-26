# PureCast MQTT Telemetry Specification & Contract

## 1. Overview & Constraints

The PureCast edge node (ESP32-C3) communicates with the cloud broker using MQTT over TLS (Port 8883) or plain MQTT (Port 1883 in dev).

### Non-Negotiable Safety Invariant
> [!IMPORTANT]
> The PureCast platform is strictly **ADVISORY ONLY**. The MQTT broker and ingestion pipeline **never** accept or transmit commands that actuate valves, cut power, switch off, or modify purifier operation. The `/config` downstream topic only supplies filter telemetry cadence and baseline calibration parameters to the edge.

---

## 2. Topic Hierarchy

All topics are namespaced by tenant and device identifier:

```
purecast/{tenant_id}/{device_id}/telemetry   (QoS 1: Ingest sensor metrics)
purecast/{tenant_id}/{device_id}/status      (QoS 1: LWT / Device connectivity)
purecast/{tenant_id}/{device_id}/events      (QoS 1: Power cycle, mode change)
purecast/{tenant_id}/{device_id}/config      (QoS 1: Downstream advisory parameters)
```

---

## 3. Telemetry Payload Format

Telemetry is published at **1 sample per minute** while active, packaged in a compact JSON format (~60 bytes per minute) with HMAC-SHA256 signature and replay protection.

### JSON Schema (`telemetry_v1.json`)
```json
{
  "v": 1,
  "ts": 1772000000,
  "nonce": "a7b3c9d1",
  "mode": "RO",
  "pump": 1,
  "p1": 2.85,
  "p2": 2.45,
  "p3": 6.20,
  "flow": 0.42,
  "tin": 650.0,
  "tout": 45.0,
  "temp": 26.5,
  "turb": 1.2,
  "uv_i": 340.0,
  "uv_h": 1420,
  "sig": "3f8a4e8d2c9b..."
}
```

### Field Definitions

| Field | Type | Description | Units / Range |
| :--- | :--- | :--- | :--- |
| `v` | integer | Protocol schema version | Fixed `1` |
| `ts` | integer | Unix timestamp (UTC seconds) | $\pm 300\text{ s}$ replay check |
| `nonce` | string | Random 8-character hex string | Idempotency key |
| `mode` | string | Operating mode | `RO`, `UF_UV`, `VACAY` |
| `pump` | integer | Pump motor status | `1` (ON), `0` (OFF) |
| `p1` | float | Inlet pressure | bar ($0.0 - 10.0$) |
| `p2` | float | Pre-filter outlet pressure | bar ($0.0 - 10.0$) |
| `p3` | float | Post-booster pump pressure | bar ($0.0 - 10.0$) |
| `flow` | float | Permeate flow rate | Litres/min ($0.0 - 5.0$) |
| `tin` | float | Raw feed water TDS | ppm ($0 - 3000$) |
| `tout` | float | Permeate treated water TDS | ppm ($0 - 1000$) |
| `temp` | float | Feed water temperature | $^\circ\text{C}$ ($2.0 - 50.0$) |
| `turb` | float | Raw water turbidity | NTU ($0.0 - 100.0$) |
| `uv_i` | float | UV lamp current | mA ($0.0 - 1000.0$) |
| `uv_h` | integer | Cumulative UV lamp on-hours | hours ($0 - 50000$) |
| `sig` | string | HMAC-SHA256 signature | 64 hex characters |

---

## 4. Security & Replay Protection

### 4.1 Signature Computation
The HMAC-SHA256 is computed over the payload string excluding `"sig"`, using the device's shared secret provisioned at factory registration:
$$\text{sig} = \text{HMAC-SHA256}(K_{device}, \text{canonical\_payload})$$

### 4.2 Replay Protection & Drift Window
1. The cloud ingestor inspects $|ts_{packet} - ts_{cloud}|$. If difference $> 300\text{ s}$ (5 minutes) and packet is not flagged as buffered offline backfill, it is rejected.
2. The combination of $(device\_id, ts, nonce)$ is stored in Redis with a 10-minute TTL. Duplicate tuples are discarded as duplicate transmissions without processing overhead.

### 4.3 Offline Buffering & Backfilling
If the purifier loses Wi-Fi connection, the ESP32-C3 buffers up to 72 hours of readings in onboard SPI flash. Once reconnected, messages are published with their original timestamps and an `offline: true` flag. The cloud batch-inserts them into TimescaleDB and flags the forecasting engine for an incremental window catch-up.
