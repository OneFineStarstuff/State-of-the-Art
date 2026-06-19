import time
import json
import os
import hashlib
import logging
import sys

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("omni-sentinel-monitor")

class OmniSentinel24hMonitor:
    """
    Implements 24-hour background telemetry and hourly checkpointing
    for Incident ALPHA-TRADE-V9-2026-001.
    """
    def __init__(self):
        # Read config from environment variables with defaults
        self.interval = int(os.environ.get("MONITOR_INTERVAL", 300))
        self.checkpoint_interval = int(os.environ.get("CHECKPOINT_INTERVAL", 3600))
        self.incident_id = os.environ.get("INCIDENT_ID", "ALPHA-TRADE-V9-2026-001")
        self.log_path = os.environ.get("LOG_PATH", "/var/log/sentinel")

        self.start_time = time.time()
        self.last_checkpoint = self.start_time

        # Ensure log directory exists
        if not os.path.exists(self.log_path):
            try:
                os.makedirs(self.log_path, exist_ok=True)
            except Exception as e:
                logger.warning(f"Could not create log path {self.log_path}: {e}. Falling back to current directory.")
                self.log_path = "."

        logger.info(f"Monitor initialized for incident {self.incident_id}")
        logger.info(f"Interval: {self.interval}s, Checkpoint: {self.checkpoint_interval}s, Log Path: {self.log_path}")

    def log_telemetry(self, data):
        timestamp = time.time()
        entry = {
            "timestamp": timestamp,
            "data": data,
            "incident": self.incident_id
        }

        # Persist telemetry to disk
        log_file = os.path.join(self.log_path, f"telemetry_{self.incident_id}.jsonl")
        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
            logger.info(f"Telemetry logged for {self.incident_id}")
        except Exception as e:
            logger.error(f"Failed to persist telemetry: {e}")

        if timestamp - self.last_checkpoint >= self.checkpoint_interval:
            self.create_checkpoint()

    def create_checkpoint(self):
        timestamp = time.time()
        checkpoint_id = hashlib.sha3_512(f"checkpoint_{timestamp}".encode()).hexdigest()[:12]
        checkpoint = {
            "checkpoint_id": checkpoint_id,
            "timestamp": timestamp,
            "incident": self.incident_id,
            "status": "SECURE"
        }

        # Persist checkpoint to disk
        checkpoint_file = os.path.join(self.log_path, f"checkpoints_{self.incident_id}.jsonl")
        try:
            with open(checkpoint_file, "a") as f:
                f.write(json.dumps(checkpoint) + "\n")
            self.last_checkpoint = timestamp
            logger.info(f"Hourly checkpoint created: {checkpoint_id}")
        except Exception as e:
            logger.error(f"Failed to persist checkpoint: {e}")

        return checkpoint

if __name__ == "__main__":
    monitor = OmniSentinel24hMonitor()
    # Simulated run for verification
    monitor.log_telemetry({"g_sri": 0.42, "status": "NOMINAL"})
    monitor.create_checkpoint()
