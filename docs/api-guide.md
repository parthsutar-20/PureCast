# PureCast REST API Guide

The PureCast API is versioned at `/api/v1` and follows RFC 7807 (Problem Details for HTTP APIs) for error handling.

## Interactive Documentation
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Schema**: [http://localhost:8000/api/openapi.json](http://localhost:8000/api/openapi.json)

---

## 1. Authentication Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/auth/login` | `POST` | OAuth2 password flow returning JWT access & refresh tokens |
| `/api/v1/auth/refresh` | `POST` | Rotate refresh token and issue new access token |
| `/api/v1/auth/logout` | `POST` | Revoke active refresh token in Redis |
| `/api/v1/auth/api-keys` | `POST` | Create a tenant API key for machine-to-machine integrations |

---

## 2. Device Management

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/devices` | `GET` | List devices belonging to the authenticated tenant (paginated) |
| `/api/v1/devices` | `POST` | Provision new purifier (generates MQTT credentials & signing key) |
| `/api/v1/devices/{id}` | `GET` | Retrieve device state, installed cartridges, and current baselines |
| `/api/v1/devices/{id}/baseline` | `POST` | Trigger baseline recalibration for a replaced cartridge |
| `/api/v1/devices/{id}/replace-cartridge` | `POST` | Record cartridge replacement (resets priors, feeds ML loop) |

---

## 3. Filter Health & Forecasts

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/devices/{id}/health-card` | `GET` | "Filter Health Card" payload for the Atomberg Home App |
| `/api/v1/devices/{id}/forecasts` | `GET` | Historical forecasts with confidence intervals per cartridge |
| `/api/v1/devices/{id}/diagnoses` | `GET` | Current diagnoses, reason codes, and physical evidence data |

### Filter Health Card Payload Example
```json
{
  "device_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "cartridge_type": "RO_MEMBRANE",
  "health_percent": 68.5,
  "remaining_days": 62,
  "confidence_band_days": 10,
  "is_estimated": false,
  "learning_phase": false,
  "status_text": "Good condition. Expected replacement in ~2 months.",
  "reason_code": "NORMAL_DEGRADATION",
  "can_reorder": true
}
```

---

## 4. Commerce & Service Automation

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/orders/reorder` | `POST` | One-tap cartridge reorder with address & payment intent |
| `/api/v1/service-requests` | `POST` | Dispatch technician visit for diagnosed hardware fault |
| `/api/v1/diy-guides/{cartridge_type}` | `GET` | Step-by-step cartridge replacement guide with media assets |

---

## 5. B2B Analytics & Fleet Insights

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/analytics/fleet-overview` | `GET` | Aggregated fleet health, active count, failure breakdown |
| `/api/v1/analytics/water-quality-heatmap`| `GET` | Regional TDS and turbidity distribution |
| `/api/v1/analytics/roi-calculator` | `GET` | Avoided warranty costs, reduced emergency visits, savings |

---

## 6. Real-Time Streaming

- **WebSocket**: `/ws/devices/{id}/live`  
  Streams live 1-second sampled telemetry, real-time health adjustments, and instant fault notifications.
