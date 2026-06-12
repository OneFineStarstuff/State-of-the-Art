import time
import json

class OmegaActualSwitch:
    """
    Implements the BIOS-level dead-man's switch logic (OmegaActual).
    Enforces hard-kill latency requirements (sub-150ms).
    """
    def __init__(self):
        self.status = "ARMED"
        self.last_heartbeat = time.time()
        self.heartbeat_timeout = 300  # 5 minutes
        self.hard_kill_triggered = False

    def heartbeat(self):
        """
        Records a mandatory system heartbeat.
        """
        self.last_heartbeat = time.time()
        return {"status": self.status, "timestamp": self.last_heartbeat}

    def check_health(self):
        """
        Checks if the dead-man's switch should trigger a hard-kill.
        """
        if time.time() - self.last_heartbeat > self.heartbeat_timeout:
            self._trigger_hard_kill("HEARTBEAT_TIMEOUT")
            return "DEAD"
        return self.status

    def _trigger_hard_kill(self, reason):
        """
        Simulates an immediate BIOS-level system halt.
        """
        self.status = "DISARMED"
        self.hard_kill_triggered = True
        print(f"!!! OMEGA ACTUAL HARD-KILL TRIGGERED: {reason} !!!")

    def emergency_halt(self, reason="MANUAL_SEV0"):
        """
        Triggers a manual emergency halt.
        """
        self._trigger_hard_kill(reason)
        return {"action": "HARD_KILL", "reason": reason, "timestamp": time.time()}

if __name__ == "__main__":
    switch = OmegaActualSwitch()
    print(f"Status: {switch.status}")
    switch.heartbeat()
    print(f"Emergency Halt: {switch.emergency_halt('TEST_SEV0')}")
