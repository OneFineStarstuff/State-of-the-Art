import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from governance_engine.zkml_pipeline_verifier import ZKMLPipelineVerifier
from governance_engine.gsri_scoring_engine import GSRIScoringEngine
from governance_engine.asa_drift_monitor import ASADriftMonitor
from infrastructure.pqc_worm_logger import PQCWORMLogger
from infrastructure.tpm_attestation_verifier import TPMAttestationVerifier

def generate():
    # 1. ZK-Fairness
    verifier = ZKMLPipelineVerifier(threshold=0.1)
    # Realistic simulation data
    data = [[0, 0.85], [1, 0.83]]
    proof = verifier.generate_proof(data, 0, 1)

    # 2. ASA Drift
    monitor = ASADriftMonitor("Institutional_Safety_v4")
    drift_report = monitor.monitor_intent("ASA-9", [0.1, 0.1], {"simulated_drift": 0.04})

    # 3. G-SRI
    engine = GSRIScoringEngine()
    gsri_report = engine.calculate_gsri(drift_report["drift_score"], 0.02, proof["value"])

    # 4. WORM Audit
    logger = PQCWORMLogger()
    log_entry = logger.commit_log({"gsri": gsri_report["gsri"], "event": "DAILY_AUDIT_20260625"})

    # 5. TPM
    tpm = TPMAttestationVerifier()
    tpm_status = tpm.verify_quote({"pcr10": tpm.expected_pcr10, "pcr11": tpm.expected_pcr11})

    metrics = {
        "g_sri": gsri_report["gsri"],
        "gsri_status": gsri_report["status"],
        "zk_fairness_bias": proof["value"],
        "zk_status": proof["status"],
        "asa_drift": drift_report["drift_score"],
        "asa_status": drift_report["status"],
        "worm_batch": log_entry["log_id"],
        "pcr_match": tpm_status["status"] == "PASS"
    }

    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    generate()
