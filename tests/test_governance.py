import unittest
import json
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from governance_engine.zkml_pipeline_verifier import ZKMLPipelineVerifier
from governance_engine.gsri_scoring_engine import GSRIScoringEngine
from governance_engine.asa_drift_monitor import ASADriftMonitor
from infrastructure.pqc_worm_logger import PQCWORMLogger
from infrastructure.omega_actual_switch import OmegaActualSwitch
from infrastructure.tpm_attestation_verifier import TPMAttestationVerifier

class TestOmniSentinelGovernance(unittest.TestCase):

    def test_zkml_fairness_pass(self):
        verifier = ZKMLPipelineVerifier(threshold=0.2)
        # Data with demographic parity within threshold
        data = [[0, 1], [0, 1], [1, 1], [1, 1]]
        proof = verifier.generate_proof(data, 0, 1)
        self.assertEqual(proof["status"], "PASS")
        self.assertEqual(proof["value"], 0.0)

    def test_zkml_fairness_fail(self):
        verifier = ZKMLPipelineVerifier(threshold=0.1)
        # Data with large demographic gap
        data = [[0, 1], [0, 1], [1, 0], [1, 0]]
        proof = verifier.generate_proof(data, 0, 1)
        self.assertEqual(proof["status"], "FAIL")
        self.assertEqual(proof["value"], 1.0)

    def test_gsri_calculation(self):
        engine = GSRIScoringEngine()
        score = engine.calculate_gsri(0.05, 0.1, 0.05)
        self.assertEqual(score["gsri"], 26.5)
        self.assertEqual(score["status"], "GREEN")

    def test_asa_drift_cae(self):
        monitor = ASADriftMonitor("Safety_v1")
        report = monitor.monitor_intent("ASA-9", [1, 0], {"simulated_drift": 0.05})
        self.assertEqual(report["status"], "HEALTHY")
        self.assertIn("cae", report)
        self.assertTrue(report["cae"]["hkma_ethics_verified"])

    def test_pqc_worm_integrity(self):
        logger = PQCWORMLogger()
        logger.commit_log({"event": "test"})
        self.assertTrue(logger.verify_integrity())
        self.assertEqual(len(logger.logs), 1)

    def test_omega_actual_halt(self):
        switch = OmegaActualSwitch()
        self.assertEqual(switch.status, "ARMED")
        switch.emergency_halt("UNIT_TEST")
        self.assertEqual(switch.status, "DISARMED")
        self.assertTrue(switch.hard_kill_triggered)

    def test_tpm_attestation(self):
        verifier = TPMAttestationVerifier()
        quote = {
            "pcr10": verifier.expected_pcr10,
            "pcr11": verifier.expected_pcr11
        }
        result = verifier.verify_quote(quote)
        self.assertEqual(result["status"], "PASS")

if __name__ == "__main__":
    unittest.main()
