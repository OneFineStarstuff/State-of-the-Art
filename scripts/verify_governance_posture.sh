#!/bin/bash
echo "--- Omni-Sentinel Institutional Governance Posture Verification ---"
echo "Timestamp: $(date -u)"

echo -n "1. Directory Structure: "
ls -d src/governance_engine src/infrastructure REPORTS scripts tests k8s deploy > /dev/null 2>&1 && echo "PASS" || echo "FAIL"

echo -n "2. Core Logic Files: "
ls src/governance_engine/zkml_pipeline_verifier.py    src/governance_engine/gsri_scoring_engine.py    src/governance_engine/asa_drift_monitor.py    src/infrastructure/pqc_worm_logger.py    src/infrastructure/omega_actual_switch.py    src/infrastructure/tpm_attestation_verifier.py > /dev/null 2>&1 && echo "PASS" || echo "FAIL"

echo -n "3. Documentation Assets: "
ls REPORTS/GLOBAL_REGULATORY_GAP_ANALYSIS.md    REPORTS/GSIFI_CONFORMITY_EVIDENCE_2026.md    SENTINEL_ASI_V4_CONTAINMENT_ARCH.md    AGI_CONTAINMENT_TLA_SPEC.md > /dev/null 2>&1 && echo "PASS" || echo "FAIL"

echo -n "4. Unit Test Execution: "
python3 -m unittest tests/test_governance.py > /dev/null 2>&1 && echo "PASS" || echo "FAIL"

echo "--- Posture Verification Complete ---"
