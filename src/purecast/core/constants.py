"""Domain-level constants for PureCast.

Physics constants, default thresholds, and algorithm parameters.
All values are configurable per tenant/cartridge model; these are
the sensible defaults from RO membrane industry practice.
"""

# ── Temperature correction ────────────────────────────────
TEMPERATURE_COEFFICIENT: float = 0.025
"""Membrane permeate flow changes ~2.5% per degree C."""

REFERENCE_TEMPERATURE_C: float = 25.0
"""Reference temperature for flow normalization (°C)."""

# ── End-of-life thresholds (relative to baseline) ────────
EOL_FLOW_DROP_FRACTION: float = 0.10
"""Normalised permeate flow drop of ~10% signals RO membrane EOL."""

EOL_SALT_PASSAGE_RISE_FRACTION: float = 0.075
"""Salt passage rise of 5-10% (midpoint 7.5%) signals RO membrane EOL."""

EOL_PREFILTER_DP_RISE_FRACTION: float = 0.125
"""Pre-filter pressure drop rise of 10-15% (midpoint 12.5%) signals EOL."""

# ── Sensor sanity limits ─────────────────────────────────
MAX_TDS_PPM: float = 3000.0
"""Maximum plausible TDS reading (ppm)."""

MIN_TDS_PPM: float = 0.0
"""Minimum plausible TDS reading (ppm)."""

MAX_FLOW_LPM: float = 5.0
"""Maximum plausible flow rate (litres per minute)."""

MAX_PRESSURE_BAR: float = 10.0
"""Maximum plausible pressure reading (bar)."""

MIN_PRESSURE_BAR: float = 0.0
"""Minimum plausible pressure reading (bar)."""

MAX_TEMPERATURE_C: float = 50.0
"""Maximum plausible water temperature (°C)."""

MIN_TEMPERATURE_C: float = 2.0
"""Minimum plausible water temperature (°C)."""

MAX_TURBIDITY_NTU: float = 100.0
"""Maximum plausible turbidity reading (NTU)."""

FROZEN_VALUE_WINDOW_SECONDS: int = 300
"""If a sensor reports the same value for this many seconds, flag as frozen."""

FROZEN_VALUE_MIN_READINGS: int = 5
"""Minimum number of identical readings to trigger frozen-value fault."""

SENSOR_DROPOUT_TIMEOUT_SECONDS: int = 180
"""Seconds of no data before flagging sensor dropout."""

# ── Kalman filter defaults ────────────────────────────────
KALMAN_PROCESS_NOISE_HEALTH: float = 0.001
"""Process noise for health state (Q matrix diagonal element)."""

KALMAN_PROCESS_NOISE_RATE: float = 0.0001
"""Process noise for rate-of-fall state (Q matrix diagonal element)."""

KALMAN_MEASUREMENT_NOISE: float = 0.01
"""Measurement noise (R matrix)."""

KALMAN_INITIAL_RATE_PRIOR: float = -0.005
"""Initial health decline rate (per day) — physics prior for new units."""

KALMAN_INITIAL_RATE_VARIANCE: float = 0.01
"""Initial variance on rate — wide band for 'learning your water' period."""

LEARNING_BAND_DAYS: int = 14
"""Days of visibly wide confidence band while the filter learns usage patterns."""

EARLY_WARNING_BIAS: float = 0.85
"""Bias factor toward early warnings (< 1.0 = conservative / early)."""

# ── UV lamp ───────────────────────────────────────────────
UV_LAMP_NOMINAL_LIFE_DAYS: int = 365
"""Nominal UV lamp life (~365 days)."""

UV_LAMP_CURRENT_DRIFT_THRESHOLD: float = 0.15
"""Relative current drift threshold for UV lamp weakening alert."""

# ── Diagnosis hysteresis ──────────────────────────────────
HYSTERESIS_ENTER_THRESHOLD: float = 0.70
"""Normalised indicator value to ENTER a fault state."""

HYSTERESIS_EXIT_THRESHOLD: float = 0.40
"""Normalised indicator value to EXIT a fault state (lower = stickier)."""

DIAGNOSIS_MIN_INDICATORS: int = 2
"""Minimum number of agreeing indicators before firing an alert."""

# ── Signal processing ────────────────────────────────────
MEDIAN_FILTER_WINDOW_SECONDS: int = 60
"""Rolling median filter window applied while pump is running."""

PUMP_OFF_ZERO_PRESSURE_TOLERANCE_BAR: float = 0.05
"""Tolerance for auto-zeroing pressure sensors when pump is off."""

# ── Ingestion ────────────────────────────────────────────
TELEMETRY_BATCH_SIZE: int = 100
"""Number of telemetry rows to batch-insert per DB write."""

REPLAY_PROTECTION_WINDOW_SECONDS: int = 300
"""HMAC replay protection window (5 minutes)."""

MAX_BACKFILL_AGE_HOURS: int = 72
"""Maximum age of backfilled telemetry accepted from offline devices."""

# ── Mode-aware ageing multipliers ────────────────────────
AGEING_MULTIPLIER_RO: float = 1.0
"""Ageing speed multiplier in RO mode (baseline)."""

AGEING_MULTIPLIER_UF_UV: float = 0.3
"""Ageing speed in UF/UV mode is ~30% of RO mode."""

AGEING_MULTIPLIER_VACAY: float = 0.05
"""Minimal ageing during vacation/stagnation mode."""
