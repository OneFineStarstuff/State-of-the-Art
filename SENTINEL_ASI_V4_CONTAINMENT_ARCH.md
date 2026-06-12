# Sentinel ASI v4.0 Containment Architecture

## 1. Federated Sandbox Model
The v4.0 architecture utilizes a multi-layered federated sandbox approach to isolate Autonomous Supervisory Agents (ASA).

## 2. BIOS-Level OmegaActual Integration
The **OmegaActual** dead-man's switch is integrated at the BIOS/Firmware level to ensure a sub-150ms hard-kill latency.
If the heartbeat is interrupted, all AGI compute clusters are immediately isolated and halted.

## 3. Governance Gates
- **PQC-Signing:** All model updates must be signed with ML-DSA.
- **ZK-Fairness:** All retail expert routing must carry a demographic parity proof.
- **CAE Interpretability:** All interventions must be wrapped in a Contextual Attribution Envelope.
