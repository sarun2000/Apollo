"""
Reimagined Apollo Guidance Computer (AGC) Core Logic
Inspired by Margaret Hamilton's fault-tolerant design for Apollo 11 (1969)
"""

import time
import random

class AGCSystem:
    def __init__(self):
        # Each task has a priority (lower = more important)
        self.tasks = {
            "landing_guidance": {"priority": 1, "active": True},
            "radar_tracking": {"priority": 2, "active": True},
            "telemetry": {"priority": 3, "active": True},
            "camera_recording": {"priority": 4, "active": True}
        }
        self.error_flag = False

    def simulate_sensor_load(self):
        # Simulate sensor overload: sometimes returns random spikes
        return random.choice([0.5, 0.7, 1.0, 1.5, 2.0])

    def check_system_load(self):
        load = self.simulate_sensor_load()
        print(f"[SYSTEM] Current CPU load: {load:.1f}x")

        if load > 1.0:
            print("[ALERT] Executive Overflow detected!")
            self.error_flag = True
        else:
            self.error_flag = False

        return load

    def recover_and_prioritize(self):
        if not self.error_flag:
            print("[STATUS] System stable. Continuing normal operations.\n")
            return

        # Graceful degradation: suspend lower priority tasks
        print("[RECOVERY] Reallocating resources to critical tasks...")
        for name, task in sorted(self.tasks.items(), key=lambda t: t[1]["priority"]):
            if task["priority"] > 2:
                task["active"] = False
                print(f"  • Suspended: {name}")
            else:
                print(f"  • Preserved: {name}")

        print("[RECOVERY] Critical operations remain online.\n")

    def run_cycle(self):
        for _ in range(5):  # Simulate 5 control cycles
            load = self.check_system_load()
            self.recover_and_prioritize()
            time.sleep(1)

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    print("🛰️  Apollo Guidance Computer Simulation Start\n")
    agc = AGCSystem()
    agc.run_cycle()
    print("✅  Simulation complete. Mission stable.")

