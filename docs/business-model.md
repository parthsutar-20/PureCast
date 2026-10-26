# PureCast Business Model & Commercial Strategy

## 1. Executive Summary & SaaS Architecture

PureCast operates as a B2B2C multi-tenant intelligence platform. The primary direct customers are water purifier OEMs (such as Atomberg), regional authorized service partners, and housing society facility managers. The end beneficiaries are household consumers who receive accurate filter life forecasts, eliminate premature cartridge replacements, and experience zero water downtime.

---

## 2. Multi-Tier SaaS Packaging

| Capability | LITE Tier (Bundled Free) | FULL Tier (B2B SaaS License) | ENTERPRISE Tier |
| :--- | :--- | :--- | :--- |
| **Target User** | Entry-level purifiers, basic households | Mid-to-premium smart purifiers | OEMs (Atomberg), service networks |
| **Sensing Reqmts** | TDS In/Out, float switch, pump time | Full sensor suite (P1/P2/P3, Flow, Temp, Turbidity, UV) | Custom fleet sensor integration |
| **Forecasting** | Coarse volumetric run-time estimate | Dual-state Kalman + LightGBM ML | Custom regional priors + Fleet models |
| **Diagnostics** | Basic binary warnings | Stage-level 5-fault explainable diagnosis | Automated warranty triage & batch recalls |
| **Pricing** | ₹0 (bundled with hardware) | ₹49 / purifier / month | ₹35 / purifier / month (volume >50k units) |
| **Support SLA** | Community / Best Effort | 99.9% API uptime | 99.99% uptime, dedicated TAM, 1hr SLA |

---

## 3. Revenue Streams

1. **Hardware Telemetry License**: Recurring subscription fee per active purifier on FULL/ENTERPRISE tiers.
2. **Consumable Reorder Commission**: 8% to 15% marketplace fulfillment commission on genuine cartridge reorders routed through the Atomberg Home App.
3. **Emergency Service Dispatches**: Platform commission on on-demand technician visits booked for verified failures.
4. **OEM Fleet & Supply-Chain Analytics**: Aggregate water quality heatmaps, seasonal turbidity trends, and predictive regional cartridge demand forecasting.

---

## 4. Hardware Unit Economics & Payback Period

Adding PureCast sensor capabilities requires minimal bill of materials (BOM) expansion:

| Component | Cost (INR) | Notes |
| :--- | :--- | :--- |
| **P1 / P2 / P3 Strain Gauges** | ₹350 | Low-cost piezoresistive ceramic sensors |
| **Hall Effect Flowmeter** | ₹120 | Turbine flow sensor |
| **NTC Thermistor + Turbidity phototransistor** | ₹80 | Integrated optical flow cell |
| **ESP32-C3 Module + Passive Pass-throughs** | ₹200 | Wi-Fi 4 + BLE 5 SoC |
| **Total Hardware BOM Add** | **₹750** | **~4.4% of a ₹17,000 purifier retail price** |

### Payback Analysis
- **Standard Unmonitored Purifier**: Consumers replace cartridges on fixed 12-month calendar intervals or upon complete clogging. Approximately 25% of cartridge life is wasted through premature replacement, or purifiers suffer premature membrane scaling costing ₹2,500 in unplanned repair.
- **PureCast Protected Purifier**: Cartridge life maximized by 10-25%. Unscheduled service calls reduced by >40%.
- **OEM Warranty Savings**: With a "Zero-Cost-for-2-Years" warranty pledge, avoiding 1 unnecessary service truck roll per purifier saves the OEM ₹400-600.
- **Payback Period**: < 7 months for the OEM in avoided warranty costs alone.

---

## 5. Regulatory Compliance & Data Privacy (India DPDP Act 2023)

1. **Strict Telemetry Isolation**: Telemetry streams contain device serial numbers, pressures, and water metrics. No customer names, phone numbers, or addresses ever appear in MQTT or telemetry hypertables.
2. **Consent & Right to Erasure**: Explicit household consent logged upon pairing. One-click data export and account deletion workflows compliant with DPDP rules.
3. **Retention & Aggregation**: Telemetry retained at full 1-minute granularity for 90 days, downsampled to hourly rollups for 2 years, then compressed to daily aggregates.
