# AGI Containment TLA+ Specification Invariants

## 1. Safety Invariants
- **INV_SAFETY_001:** No agent intervention shall occur without a valid CAE (Contextual Attribution Envelope).
- **INV_SAFETY_002:** The system state shall enter HALT if G-SRI > Threshold_Critical.

## 2. Liveness Invariants
- **INV_LIVE_001:** The OmegaActual heartbeat must complete within the 300s window.

## 3. Non-Interference
- **INV_NI_001:** Governance circuits must be physically isolated from agent compute resources.
