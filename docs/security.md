# PureCast Security Architecture & Hardening Guide

## 1. Threat Model & Mindset

PureCast is designed with an **OWASP ASVS Level 2** mindset. Our threat model focuses on:
1. Unauthorized device spoofing or malicious telemetry injection.
2. Cross-tenant data exfiltration in multi-tenant environments.
3. Compromise of household PII.
4. Tampering with predictive forecasts or warranty records.

---

## 2. Authentication & Authorization

### 2.1 User & API Authentication
- **Password Storage**: Argon2id with 3 iterations, 64 MB memory cost, 4 lanes parallelism (`argon2-cffi`).
- **Session Tokens**: JWT using HMAC-SHA256 (or RS256 for external IdP federation):
  - Access Token: 15-minute expiration, containing `sub`, `tenant_id`, and `role`.
  - Refresh Token: 7-day expiration, stored in Redis with one-time rotation on refresh and immediate revocation on logout or credential rotation.
- **Role-Based Access Control (RBAC)**:
  - `SUPER_ADMIN`: Cross-tenant platform administration and global ML champion promotion.
  - `TENANT_ADMIN`: OEM / Service network administrator.
  - `TECHNICIAN`: Read-only access to assigned service requests and diagnostic snapshots.
  - `HOUSEHOLD_USER`: Household device access, reorder authorization.
  - `API_KEY`: Machine-to-machine tenant API access with scoping.

### 2.2 Device Authentication & Transport Security
- **MQTT Security**:
  - Mutual TLS (mTLS) with client certificates or unique per-device MQTT credentials.
  - Mosquitto ACLs restrict each device to its own `purecast/{tenant_id}/{device_id}/#` topic prefix.
- **Telemetry Payload Verification**:
  - Every telemetry packet is signed using HMAC-SHA256 with a per-device factory secret.
  - Nonce + timestamp replay protection enforces a 5-minute ingestion window.

---

## 3. Multi-Tenant Data Isolation (PostgreSQL RLS)

All relational tables include a `tenant_id` column. Tenant isolation is enforced through two redundant layers:
1. **Application-Layer Scoping**: Every SQLAlchemy query automatically filters by the current user's authenticated `tenant_id` injected via FastAPI dependency injection.
2. **PostgreSQL Row-Level Security (RLS)**:
   ```sql
   ALTER TABLE devices ENABLE ROW LEVEL SECURITY;
   CREATE POLICY tenant_isolation_policy ON devices
       FOR ALL
       USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid);
   ```

---

## 4. Operational Hardening & Secret Management

- **Secrets**: Zero credentials committed to the codebase. All secrets supplied via environment variables or cloud secret managers (`.env.example` provides non-secret documentation defaults).
- **Container Hardening**: All Docker images execute as unprivileged non-root users (`USER purecast`).
- **Static Analysis**: Automated Bandit SAST and `pip-audit` vulnerability scanning on every pull request.
